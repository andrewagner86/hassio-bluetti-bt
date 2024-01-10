"""Coordinator for Bluetti integration."""

from __future__ import annotations
from typing import List, cast

import asyncio
from datetime import timedelta
import logging
import async_timeout

from bleak import BleakClient, BleakError

from homeassistant.components import bluetooth
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from bluetti_mqtt.bluetooth.client import BluetoothClient
from bluetti_mqtt.bluetooth import (
    BadConnectionError,
    ModbusError,
    ParseError,
    build_device,
)
from bluetti_mqtt.core.devices.bluetti_device import BluettiDevice
from bluetti_mqtt.core.commands import ReadHoldingRegisters

from bluetti_bt_api.client import BluettiClient

from .const import DATA_POLLING_RUNNING, DOMAIN
from .utils import mac_loggable

_LOGGER = logging.getLogger(__name__)


class DummyDevice(BluettiDevice):
    """Dummy device used to add more fields to existing devices.

    Changes made here are only temporary and should also be
    contributed to https://github.com/warhammerkid/bluetti_mqtt
    """

    def __init__(self, device: BluettiDevice):
        """Init dummy device with real device."""
        self.struct = device.struct

        if device.type == "EP600":
            # DC Solar Input (copied from PR https://github.com/warhammerkid/bluetti_mqtt/pull/87 by KM011092)
            self.struct.add_uint_field('pv_input_power1', 1212)  # MPP 1 in - value * 0.1
            #self.struct.add_uint_field('pv_input_voltage1', 1213)  # MPP 1 in  - value * 0.1
            #self.struct.add_uint_field('pv_input_current1', 1214)  # MPP 1 in
            self.struct.add_uint_field('pv_input_power2', 1220)  # MPP 2 in  - value * 0.1
            #self.struct.add_uint_field('pv_input_voltage2', 1221)  # MPP 2 in  - value * 0.1
            #self.struct.add_uint_field('pv_input_current2', 1222)  # MPP 2 in
            # ADL400 Smart Meter for AC Solar
            self.struct.add_uint_field("adl400_ac_input_power_phase1", 1228)
            self.struct.add_uint_field("adl400_ac_input_power_phase2", 1236)
            self.struct.add_uint_field("adl400_ac_input_power_phase3", 1244)
            self.struct.add_decimal_field("adl400_ac_input_voltage_phase1", 1229, 1)
            self.struct.add_decimal_field("adl400_ac_input_voltage_phase2", 1237, 1)
            self.struct.add_decimal_field("adl400_ac_input_voltage_phase3", 1245, 1)
            # Grid Input
            self.struct.add_decimal_field("grid_input_frequency", 1300, 1)
            self.struct.add_uint_field("grid_input_power_phase1", 1313)
            self.struct.add_uint_field("grid_input_power_phase2", 1319)
            self.struct.add_uint_field("grid_input_power_phase3", 1325)
            self.struct.add_decimal_field("grid_input_voltage_phase1", 1314, 1)
            self.struct.add_decimal_field("grid_input_voltage_phase2", 1320, 1)
            self.struct.add_decimal_field("grid_input_voltage_phase3", 1326, 1)
            self.struct.add_decimal_field("grid_input_current_phase1", 1315, 1)
            self.struct.add_decimal_field("grid_input_current_phase2", 1321, 1)
            self.struct.add_decimal_field("grid_input_current_phase3", 1327, 1)
            # EP600 AC Output
            self.struct.add_decimal_field("ac_output_frequency", 1500, 1)
            self.struct.add_uint_field("ac_output_power_phase1", 1510)
            self.struct.add_uint_field("ac_output_power_phase2", 1517)
            self.struct.add_uint_field("ac_output_power_phase3", 1524)
            self.struct.add_decimal_field("ac_output_voltage_phase1", 1511, 1)
            self.struct.add_decimal_field("ac_output_voltage_phase2", 1518, 1)
            self.struct.add_decimal_field("ac_output_voltage_phase3", 1525, 1)
            self.struct.add_decimal_field("ac_output_current_phase1", 1512, 1)
            self.struct.add_decimal_field("ac_output_current_phase2", 1519, 1)
            self.struct.add_decimal_field("ac_output_current_phase3", 1526, 1)

        super().__init__(device.address, device.type, device.sn)
        self._parent = device

    @property
    def pack_num_max(self):
        return self._parent.pack_num_max

    @property
    def polling_commands(self) -> List[ReadHoldingRegisters]:
        if self.type == "EP600":
            return [
                ReadHoldingRegisters(100, 62),
                ReadHoldingRegisters(1228, 19),
                ReadHoldingRegisters(1300, 28),
                ReadHoldingRegisters(1500, 27),
                ReadHoldingRegisters(2022, 6),
                ReadHoldingRegisters(2213, 4),
                ReadHoldingRegisters(1212, 11),
                # Battery
                ReadHoldingRegisters(6101, 7),
                ReadHoldingRegisters(6175, 11),
            ]

        return self._parent.polling_commands

    @property
    def pack_polling_commands(self) -> List[ReadHoldingRegisters]:
        if self.type == "EP600":
            return []
        return self._parent.pack_polling_commands

    @property
    def logging_commands(self) -> List[ReadHoldingRegisters]:
        return self._parent.logging_commands

    @property
    def pack_logging_commands(self) -> List[ReadHoldingRegisters]:
        return self._parent.pack_logging_commands

    @property
    def writable_ranges(self) -> List[range]:
        return self._parent.writable_ranges


class PollingCoordinator(DataUpdateCoordinator):
    """Polling coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        address: str,
        device_name: str,
        polling_interval: int,
        persistent_conn: bool,
        polling_timeout: int,
        max_retries: int,
    ):
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Bluetti polling coordinator",
            update_interval=timedelta(seconds=polling_interval),
        )
        bluetti_device = build_device(address, device_name)

        # Add or modify device fields
        self.bluetti_device = DummyDevice(bluetti_device)

        # Create client
        self.logger.debug("Creating client")
        device = bluetooth.async_ble_device_from_address(hass, address)
        if device is None:
            self.logger.error("Device %s not available", mac_loggable(address))
            return None
        self.client = BleakClient(device)

        # polling mutex to guard against switches
        self.polling_lock = asyncio.Lock()

        # Create API client
        self.api_client = BluettiClient(
            self.client,
            self.bluetti_device,
            self.hass.loop.create_future,
            self.polling_lock,
            persistent_conn,
            polling_timeout,
            max_retries,
        )

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        self.hass.data[DOMAIN][self.config_entry.entry_id][DATA_POLLING_RUNNING] = True

        parsed_data = await self.api_client.readDevice()
        
        self.hass.data[DOMAIN][self.config_entry.entry_id][DATA_POLLING_RUNNING] = False

        # Pass data back to sensors
        return parsed_data
