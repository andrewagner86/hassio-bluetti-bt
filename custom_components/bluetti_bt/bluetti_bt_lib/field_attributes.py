"""Field attributes for device fields."""

from enum import Enum, auto, unique

from .field_enums import (
    AutoSleepMode,
    ChargingMode,
    EcoShutdown,
    LedMode,
    OutputMode,
    SplitPhaseMachineType,
    UpsMode,
    TimeScheduleMode,
)


@unique
class FieldType(Enum):
    NUMERIC = auto()
    BOOL = auto()
    ENUM = auto()
    CHARACTER = auto()


class FieldAttributes:
    def __init__(
        self,
        type: FieldType = FieldType.NUMERIC,
        setter: bool = False,
        name: str = "",
        unit_of_measurement: str | None = None,
        device_class: str | None = None,
        state_class: str | None = None,
        options: Enum | None = None,
    ):
        self.type = type
        self.setter = setter
        self.name = name
        self.unit_of_measurement = unit_of_measurement
        self.device_class = device_class
        self.state_class = state_class
        self.options = options


class PowerFieldAttributes(FieldAttributes):
    def __init__(
        self,
        name: str = "",
    ):
        super().__init__(
            name=name,
            unit_of_measurement="W",
            device_class="power",
            state_class="measurement",
        )


class VoltageFieldAttributes(FieldAttributes):
    def __init__(
        self,
        name: str = "",
    ):
        super().__init__(
            name=name,
            unit_of_measurement="V",
            device_class="voltage",
            state_class="measurement",
        )


class CurrentFieldAttributes(FieldAttributes):
    def __init__(
        self,
        name: str = "",
    ):
        super().__init__(
            name=name,
            unit_of_measurement="A",
            device_class="current",
            state_class="measurement",
        )


class EnergyFieldAttributes(FieldAttributes):
    def __init__(
        self,
        name: str = "",
    ):
        super().__init__(
            name=name,
            unit_of_measurement="kWh",
            device_class="energy",
            state_class="total_increasing",
        )


class FrequencyFieldAttributes(FieldAttributes):
    def __init__(
        self,
        name: str = "",
    ):
        super().__init__(
            name=name,
            unit_of_measurement="Hz",
            device_class="frequency",
            state_class="measurement",
        )


class OutletFieldAttributes(FieldAttributes):
    def __init__(
        self,
        name: str = "",
        setter: bool = False,
    ):
        super().__init__(
            type=FieldType.BOOL,
            name=name,
            setter=setter,
            device_class="outlet",
        )


class TextFieldAttributes(FieldAttributes):
    def __init__(
        self,
        name: str = "",
        setter: bool = False,
    ):
        super().__init__(
            type=FieldType.CHARACTER,
            name=name,
            setter=setter
        )


FIELD_ATTRIBUTES: dict[str, FieldAttributes] = {
    # Base device fields
    "dc_input_power": PowerFieldAttributes("DC Input Power"),
    "ac_input_power": PowerFieldAttributes("AC Input Power"),
    "ac_output_power": PowerFieldAttributes("AC Output Power"),
    "dc_output_power": PowerFieldAttributes("DC Output Power"),
    "power_generation": EnergyFieldAttributes("Total Power Generation"),
    "total_battery_percent": FieldAttributes(
        type=FieldType.NUMERIC,
        name="Total Battery Percent",
        unit_of_measurement="%",
        device_class="battery",
        state_class="measurement",
    ),
    "total_battery_voltage": VoltageFieldAttributes("Total Battery Voltage"),
    "ac_output_on": OutletFieldAttributes("AC Output"),
    "dc_output_on": OutletFieldAttributes("DC Output"),
    # Controls
    "ac_output_on_switch": OutletFieldAttributes(
        name="AC Output",
        setter=True,
    ),
    "dc_output_on_switch": OutletFieldAttributes(
        name="DC Output",
        setter=True,
    ),
    # Device specific fields
    "ac_output_mode": FieldAttributes(
        type=FieldType.ENUM,
        name="AC Output Mode",
        options=OutputMode,
    ),
    "internal_ac_voltage": VoltageFieldAttributes("Internal AC Voltage"),
    "internal_current_one": CurrentFieldAttributes("Internal Current Sensor 1"),
    "internal_power_one": PowerFieldAttributes("Internal Power Sensor 1"),
    "internal_ac_frequency": FrequencyFieldAttributes("Internal AC Frequency"),
    "internal_current_two": CurrentFieldAttributes("Internal Current Sensor 2"),
    "internal_power_two": PowerFieldAttributes("Internal Power Sensor 2"),
    "ac_input_voltage": VoltageFieldAttributes("AC Input Voltage"),
    "internal_current_three": CurrentFieldAttributes("Internal Current Sensor 3"),
    "internal_power_three": PowerFieldAttributes("Internal Power Sensor 3"),
    "ac_input_frequency": FrequencyFieldAttributes("AC Input Frequency"),
    "internal_dc_input_voltage": VoltageFieldAttributes("Internal DC Input Voltage"),
    "internal_dc_input_power": PowerFieldAttributes("Internal DC Input Power"),
    "internal_dc_input_current": CurrentFieldAttributes("Internal DC Input Current"),
    "pv_input_power1": PowerFieldAttributes("Solar Input Power 1"),
    "pv_input_power2": PowerFieldAttributes("Solar Input Power 2"),
    "pv_input_voltage1": VoltageFieldAttributes("Solar Input Voltage 1"),
    "pv_input_voltage2": VoltageFieldAttributes("Solar Input Voltage 2"),
    "pv_input_current1": CurrentFieldAttributes("Solar Input Current 1"),
    "pv_input_current2": CurrentFieldAttributes("Solar Input Current 2"),
    "adl400_ac_input_power_phase1": PowerFieldAttributes(
        "AC Solar Input Power Phase 1"
    ),
    "adl400_ac_input_power_phase2": PowerFieldAttributes(
        "AC Solar Input Power Phase 2"
    ),
    "adl400_ac_input_power_phase3": PowerFieldAttributes(
        "AC Solar Input Power Phase 3"
    ),
    "adl400_ac_input_voltage_phase1": VoltageFieldAttributes(
        "AC Solar Input Voltage Phase 1"
    ),
    "adl400_ac_input_voltage_phase2": VoltageFieldAttributes(
        "AC Solar Input Voltage Phase 2"
    ),
    "adl400_ac_input_voltage_phase3": VoltageFieldAttributes(
        "AC Solar Input Voltage Phase 3"
    ),
    "adl400_ac_input_current_phase1": CurrentFieldAttributes(
        "AC Solar Input Current Phase 1"
    ),
    "adl400_ac_input_current_phase2": CurrentFieldAttributes(
        "AC Solar Input Current Phase 2"
    ),
    "adl400_ac_input_current_phase3": CurrentFieldAttributes(
        "AC Solar Input Current Phase 3"
    ),
    "grid_frequency": FrequencyFieldAttributes("Grid Frequency"),
    "grid_power_phase1": PowerFieldAttributes("Grid Power Phase 1"),
    "grid_power_phase2": PowerFieldAttributes("Grid Power Phase 2"),
    "grid_power_phase3": PowerFieldAttributes("Grid Power Phase 3"),
    "grid_voltage_phase1": VoltageFieldAttributes("Grid Voltage Phase 1"),
    "grid_voltage_phase2": VoltageFieldAttributes("Grid Voltage Phase 2"),
    "grid_voltage_phase3": VoltageFieldAttributes("Grid Voltage Phase 3"),
    "grid_current_phase1": CurrentFieldAttributes("Grid Current Phase 1"),
    "grid_current_phase2": CurrentFieldAttributes("Grid Current Phase 2"),
    "grid_current_phase3": CurrentFieldAttributes("Grid Current Phase 3"),
    "ac_output_frequency": FrequencyFieldAttributes("AC Output Frequency"),
    "ac_output_power_phase1": PowerFieldAttributes("AC Output Power Phase 1"),
    "ac_output_power_phase2": PowerFieldAttributes("AC Output Power Phase 2"),
    "ac_output_power_phase3": PowerFieldAttributes("AC Output Power Phase 3"),
    "ac_output_voltage_phase1": VoltageFieldAttributes("AC Output Voltage Phase 1"),
    "ac_output_voltage_phase2": VoltageFieldAttributes("AC Output Voltage Phase 2"),
    "ac_output_voltage_phase3": VoltageFieldAttributes("AC Output Voltage Phase 3"),
    "total_ac_consumption": EnergyFieldAttributes("Total Load Consumption"),
    "total_grid_consumption": EnergyFieldAttributes("Total Grid Consumption"),
    "total_grid_feed": EnergyFieldAttributes("Total Grid Feed"),
    # Device specific controls
    "power_off": FieldAttributes(
        type=FieldType.BOOL,
        setter=True,
        name="Power Off",
    ),
    "auto_sleep_mode": FieldAttributes(
        type=FieldType.ENUM,
        setter=True,
        name="Screen Auto Sleep Mode",
        options=AutoSleepMode,
    ),
    "ups_mode": FieldAttributes(
        type=FieldType.ENUM,
        setter=False,  # Disabled for safety reasons
        name="UPS Working Mode",
        options=UpsMode,
    ),
    "split_phase_on": FieldAttributes(
        type=FieldType.BOOL,
        setter=False,  # Disabled for safety reasons
        name="Split Phase",
    ),
    "split_phase_machine_mode": FieldAttributes(
        type=FieldType.ENUM,
        setter=False,  # Disabled for safety reasons
        name="Split Phase Machine Type",
        options=SplitPhaseMachineType,
    ),
    "grid_charge_on": FieldAttributes(
        type=FieldType.BOOL,
        setter=False,  # Disabled for safety reasons
        name="Grid Charge",
    ),
    "time_control_on": FieldAttributes(
        type=FieldType.BOOL,
        setter=False,  # Disabled for safety reasons
        name="Time Control",
    ),
    "battery_range_start": FieldAttributes(
        type=FieldType.NUMERIC,
        setter=False,  # Disabled
        name="Battery Range Start",
        unit_of_measurement="%",
    ),
    "battery_range_end": FieldAttributes(
        type=FieldType.NUMERIC,
        setter=False,  # Disabled
        name="Battery Range End",
        unit_of_measurement="%",
    ),
    "led_mode": FieldAttributes(
        type=FieldType.ENUM,
        setter=True,
        name="LED Mode",
        options=LedMode,
    ),
    "eco_on": FieldAttributes(
        type=FieldType.BOOL,
        setter=True,
        name="Eco Mode",
    ),
    "eco_shutdown": FieldAttributes(
        type=FieldType.ENUM,
        setter=True,
        name="Eco Shutdown",
        options=EcoShutdown,
    ),
    "charging_mode": FieldAttributes(
        type=FieldType.ENUM,
        setter=True,
        name="Charging Mode",
        options=ChargingMode,
    ),
    "power_lifting_on": FieldAttributes(
        type=FieldType.BOOL,
        setter=True,
        name="Power Lifting",
    ),

    'total_battery_soc':FieldAttributes(
        type=FieldType.NUMERIC,
        name="Total Battery Percent",
        unit_of_measurement="%",
        device_class="battery",
        state_class="measurement",
    ),
    'device_type':TextFieldAttributes('device_type'),
    'device_sn':TextFieldAttributes('device_sn'),
    'output_power':PowerFieldAttributes('output_power'),
    'input_power':PowerFieldAttributes('input_power'),
    'grid_power':PowerFieldAttributes('grid_power'),
    'unknown_power':PowerFieldAttributes('unknown_power'),
    'total_consumption':EnergyFieldAttributes('total_consumption'),
    'total_feed':EnergyFieldAttributes('total_feed'),
    'total_grid_consumption':EnergyFieldAttributes('total_grid_consumption'),
    'total_grid_feed':EnergyFieldAttributes('total_grid_feed'),
    'system_arm_version':TextFieldAttributes('system_arm_version'),
    'system_dsp_version':TextFieldAttributes('system_dsp_version'),
    'dc_input1_power':PowerFieldAttributes('dc_input1_power'),
    'dc_input1_voltage':VoltageFieldAttributes('dc_input1_voltage'),
    'dc_input1_current':CurrentFieldAttributes('dc_input1_current'),
    'dc_input2_power':PowerFieldAttributes('dc_input2_power'),
    'dc_input2_voltage':VoltageFieldAttributes('dc_input2_voltage'),
    'dc_input2_current':CurrentFieldAttributes('dc_input2_current'),
    'ac_input_phase1_power':PowerFieldAttributes('ac_input_phase1_power'),
    'ac_input_phase1_voltage':VoltageFieldAttributes('ac_input_phase1_voltage'),
    'ac_input_phase1_current':CurrentFieldAttributes('ac_input_phase1_current'),
    'ac_input_phase2_power':PowerFieldAttributes('ac_input_phase2_power'),
    'ac_input_phase2_voltage':VoltageFieldAttributes('ac_input_phase2_voltage'),
    'ac_input_phase2_current':CurrentFieldAttributes('ac_input_phase2_current'),
    'ac_input_phase3_power':PowerFieldAttributes('ac_input_phase3_power'),
    'ac_input_phase3_voltage':VoltageFieldAttributes('ac_input_phase3_voltage'),
    'ac_input_phase3_current':CurrentFieldAttributes('ac_input_phase3_current'),
    'grid_frequency':FrequencyFieldAttributes('grid_frequency'),
    'grid_phase1_power':PowerFieldAttributes('grid_phase1_power'),
    'grid_phase1_voltage':VoltageFieldAttributes('grid_phase1_voltage'),
    'grid_phase1_current':CurrentFieldAttributes('grid_phase1_current'),
    'grid_phase2_power':PowerFieldAttributes('grid_phase2_power'),
    'grid_phase2_voltage':VoltageFieldAttributes('grid_phase2_voltage'),
    'grid_phase2_current':CurrentFieldAttributes('grid_phase2_current'),
    'grid_phase3_power':PowerFieldAttributes('grid_phase3_power'),
    'grid_phase3_voltage':VoltageFieldAttributes('grid_phase3_voltage'),
    'grid_phase3_current':CurrentFieldAttributes('grid_phase3_current'),
    'ac_output_phase1_power':PowerFieldAttributes('ac_output_phase1_power'),
    'ac_output_phase1_voltage':VoltageFieldAttributes('ac_output_phase1_voltage'),
    'ac_output_phase1_current':CurrentFieldAttributes('ac_output_phase1_current'),
    'ac_output_phase2_power':PowerFieldAttributes('ac_output_phase2_power'),
    'ac_output_phase2_voltage':VoltageFieldAttributes('ac_output_phase2_voltage'),
    'ac_output_phase2_current':CurrentFieldAttributes('ac_output_phase2_current'),
    'ac_output_phase3_power':PowerFieldAttributes('ac_output_phase3_power'),
    'ac_output_phase3_voltage':VoltageFieldAttributes('ac_output_phase3_voltage'),
    'ac_output_phase3_current':CurrentFieldAttributes('ac_output_phase3_current'),
    'unknown_frequency':FrequencyFieldAttributes('unknown_frequency'),
    'unknown_phase1_power':PowerFieldAttributes('unknown_phase1_power'),
    'unknown_phase1_voltage':VoltageFieldAttributes('unknown_phase1_voltage'),
    'unknown_phase1_current':CurrentFieldAttributes('unknown_phase1_current'),
    'unknown_phase2_power':PowerFieldAttributes('unknown_phase2_power'),
    'unknown_phase2_voltage':VoltageFieldAttributes('unknown_phase2_voltage'),
    'unknown_phase2_current':CurrentFieldAttributes('unknown_phase2_current'),
    'unknown_phase3_power':PowerFieldAttributes('unknown_phase3_power'),
    'unknown_phase3_voltage':VoltageFieldAttributes('unknown_phase3_voltage'),
    'unknown_phase3_current':CurrentFieldAttributes('unknown_phase3_current'),
    'datetime_year':TextFieldAttributes('datetime_year'),
    'datetime_month':TextFieldAttributes('datetime_month'),
    'datetime_day':TextFieldAttributes('datetime_day'),
    'datetime_hour':TextFieldAttributes('datetime_hour'),
    'datetime_minute':TextFieldAttributes('datetime_minute'),
    'datetime_second':TextFieldAttributes('datetime_second'),
    'main_switch':OutletFieldAttributes(
        name='main_switch',
        setter=True,
    ),
    'min_battery_soc':FieldAttributes(
        type=FieldType.NUMERIC,
        setter=True,
        name='min_battery_soc',
        unit_of_measurement='%',
    ),
    'max_battery_soc':FieldAttributes(
        type=FieldType.NUMERIC,
        setter=True,
        name='max_battery_soc',
        unit_of_measurement='%',
    ),
    'time_control_switch':OutletFieldAttributes(
        name='time_control_switch',
        setter=True,
    ),
    'time_schedule1_mode':FieldAttributes(
        type=FieldType.ENUM,
        setter=True,
        name='time_schedule1_mode',
        options=TimeScheduleMode,
    ),
    'time_schedule1_start_hour':TextFieldAttributes('time_schedule1_start_hour'),
    'time_schedule1_start_minute':TextFieldAttributes('time_schedule1_start_minute'),
    'time_schedule1_end_hour':TextFieldAttributes('time_schedule1_end_hour'),
    'time_schedule1_end_minute':TextFieldAttributes('time_schedule1_end_minute'),
    'time_schedule2_mode':FieldAttributes(
        type=FieldType.ENUM,
        setter=True,
        name='time_schedule2_mode',
        options=TimeScheduleMode,
    ),
    'time_schedule2_start_hour':TextFieldAttributes('time_schedule2_start_hour'),
    'time_schedule2_start_minute':TextFieldAttributes('time_schedule2_start_minute'),
    'time_schedule2_end_hour':TextFieldAttributes('time_schedule2_end_hour'),
    'time_schedule2_end_minute':TextFieldAttributes('time_schedule2_end_minute'),
    'time_schedule3_mode':FieldAttributes(
        type=FieldType.ENUM,
        setter=True,
        name='time_schedule3_mode',
        options=TimeScheduleMode,
    ),
    'time_schedule3_start_hour':TextFieldAttributes('time_schedule3_start_hour'),
    'time_schedule3_start_minute':TextFieldAttributes('time_schedule3_start_minute'),
    'time_schedule3_end_hour':TextFieldAttributes('time_schedule3_end_hour'),
    'time_schedule3_end_minute':TextFieldAttributes('time_schedule3_end_minute'),
    'time_schedule4_mode':FieldAttributes(
        type=FieldType.ENUM,
        setter=True,
        name='time_schedule4_mode',
        options=TimeScheduleMode,
    ),
    'time_schedule4_start_hour':TextFieldAttributes('time_schedule4_start_hour'),
    'time_schedule4_start_minute':TextFieldAttributes('time_schedule4_start_minute'),
    'time_schedule4_end_hour':TextFieldAttributes('time_schedule4_end_hour'),
    'time_schedule4_end_minute':TextFieldAttributes('time_schedule4_end_minute'),
    'time_schedule5_mode':FieldAttributes(
        type=FieldType.ENUM,
        setter=True,
        name='time_schedule5_mode',
        options=TimeScheduleMode,
    ),
    'time_schedule5_start_hour':TextFieldAttributes('time_schedule5_start_hour'),
    'time_schedule5_start_minute':TextFieldAttributes('time_schedule5_start_minute'),
    'time_schedule5_end_hour':TextFieldAttributes('time_schedule5_end_hour'),
    'time_schedule5_end_minute':TextFieldAttributes('time_schedule5_end_minute'),
    'time_schedule6_mode':FieldAttributes(
        type=FieldType.ENUM,
        setter=True,
        name='time_schedule6_mode',
        options=TimeScheduleMode,
    ),
    'time_schedule6_start_hour':TextFieldAttributes('time_schedule6_start_hour'),
    'time_schedule6_start_minute':TextFieldAttributes('time_schedule6_start_minute'),
    'time_schedule6_end_hour':TextFieldAttributes('time_schedule6_end_hour'),
    'time_schedule6_end_minute':TextFieldAttributes('time_schedule6_end_minute'),
    'buzzer_switch':OutletFieldAttributes(
        name='buzzer_switch',
        setter=True,
    ),
    'charge_from_grid':OutletFieldAttributes(
        name='charge_from_grid',
        setter=True,
    ),
    'feed_to_grid':OutletFieldAttributes(
        name='feed_to_grid',
        setter=True,
    ),
    'max_input_power_per_phase':PowerFieldAttributes('max_input_power_per_phase'),
    'max_input_current_per_phase':CurrentFieldAttributes('max_input_current_per_phase'),
    'max_output_power_per_phase':PowerFieldAttributes('max_output_power_per_phase'),
    'max_output_current_per_phase':CurrentFieldAttributes('max_output_current_per_phase'),
    'grid_self_adjustment':OutletFieldAttributes(
        name='grid_self_adjustment',
        setter=True,
    ),
    'restore_system_switch':OutletFieldAttributes(
        name='restore_system_switch',
        setter=True,
    ),
    'battery_heater':OutletFieldAttributes(
        name='battery_heater',
        setter=True,
    ),
    'iot_version':TextFieldAttributes('iot_version'),
    'wifi_name':TextFieldAttributes('wifi_name'),
    'wifi_password':TextFieldAttributes('wifi_password'),
}


def PACK_FIELD_ATTRIBUTES(pack: int):
    return {
        "pack_voltage": VoltageFieldAttributes(
            name=f"Battery Pack {pack} Voltage",
        ),
        "pack_battery_percent": FieldAttributes(
            type=FieldType.NUMERIC,
            name=f"Battery Pack {pack} Percent",
            unit_of_measurement="%",
            device_class="battery",
            state_class="measurement",
        ),
        "pack_bms_version": FieldAttributes(
            type=FieldType.NUMERIC,
            name=f"Battery Pack {pack} BMS Version",
        ),
    }
