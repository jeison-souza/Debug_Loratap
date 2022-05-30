# """LoraTap Garage Door Opener with Door Sensor."""
# from zigpy.profiles import zha
# from zigpy.zcl.clusters.general import Basic, Groups, Ota, Scenes, Time, GreenPowerProxy

# from zhaquirks.const import (
#     DEVICE_TYPE,
#     ENDPOINTS,
#     INPUT_CLUSTERS,
#     MODELS_INFO,
#     OUTPUT_CLUSTERS,
#     PROFILE_ID,
# )

from typing import Any, Callable, Dict, Optional, Tuple, Union
import zigpy.types as t
from zigpy.zcl import foundation
from zigpy.zcl.clusters.general import LevelControl, OnOff

# from zhaquirks.tuya import TuyaSwitch, PowerOnState
# from zhaquirks.tuya.mcu import MoesSwitchManufCluster, TuyaOnOff, TuyaOnOffManufCluster, TuyaMCUCluster, DPToAttributeMapping, MoesBacklight, TuyaDPType

# class TuyaBostaCluster(TuyaOnOffManufCluster):
#     """On/Off Tuya cluster with extra device attributes."""

#     attributes = {
#         0x8001: ("backlight_mode", MoesBacklight),
#         0x8002: ("power_on_state", PowerOnState),
#     }

#     dp_to_attribute: Dict[
#         int, DPToAttributeMapping
#     ] = TuyaOnOffManufCluster.dp_to_attribute.copy()
#     dp_to_attribute.update(
#         {
#             14: DPToAttributeMapping(
#                 TuyaMCUCluster.ep_attribute,
#                 "power_on_state",
#                 dp_type=TuyaDPType.ENUM,
#                 converter=lambda x: PowerOnState(x),
#             )
#         }
#     )
#     dp_to_attribute.update(
#         {
#             15: DPToAttributeMapping(
#                 TuyaMCUCluster.ep_attribute,
#                 "backlight_mode",
#                 dp_type=TuyaDPType.ENUM,
#                 converter=lambda x: MoesBacklight(x),
#             ),
#         }
#     )

#     data_point_handlers = TuyaOnOffManufCluster.data_point_handlers.copy()
#     data_point_handlers.update({14: "_dp_2_attr_update"})
#     data_point_handlers.update({15: "_dp_2_attr_update"})


# class GDC311ZBQ1(TuyaSwitch):
#     """LoraTap Garage Door Opener with Door Sensor."""
#     # {
#     #   "node_descriptor": "NodeDescriptor(logical_type=<LogicalType.Router: 1>, complex_descriptor_available=0, user_descriptor_available=0, reserved=0, aps_flags=0, frequency_band=<FrequencyBand.Freq2400MHz: 8>, mac_capability_flags=<MACCapabilityFlags.AllocateAddress|RxOnWhenIdle|MainsPowered|FullFunctionDevice: 142>, manufacturer_code=4417, maximum_buffer_size=66, maximum_incoming_transfer_size=66, server_mask=10752, maximum_outgoing_transfer_size=66, descriptor_capability_field=<DescriptorCapability.NONE: 0>, *allocate_address=True, *is_alternate_pan_coordinator=False, *is_coordinator=False, *is_end_device=False, *is_full_function_device=True, *is_mains_powered=True, *is_receiver_on_when_idle=True, *is_router=True, *is_security_capable=False)",
#     #   "endpoints": {
#     #     "1": {
#     #       "profile_id": 260,
#     #       "device_type": "0x0051",
#     #       "in_clusters": [
#     #         "0x0000",
#     #         "0x0004",
#     #         "0x0005",
#     #         "0xef00"
#     #       ],
#     #       "out_clusters": [
#     #         "0x000a",
#     #         "0x0019"
#     #       ]
#     #     },
#     #     "242": {
#     #       "profile_id": 41440,
#     #       "device_type": "0x0061",
#     #       "in_clusters": [],
#     #       "out_clusters": [
#     #         "0x0021"
#     #       ]
#     #     }
#     #   },
#     #   "manufacturer": "_TZE200_wfxuhoea",
#     #   "model": "TS0601",
#     #   "class": "zigpy.device.Device"
#     # }
#     signature = { 
#         MODELS_INFO: [
#             ("_TZE200_wfxuhoea", "TS0601"),
#         ],
#         ENDPOINTS: {
#             1: {
#                 PROFILE_ID: zha.PROFILE_ID,
#                 DEVICE_TYPE: zha.DeviceType.SMART_PLUG,
#                 INPUT_CLUSTERS: [
#                     Basic.cluster_id,
#                     Groups.cluster_id,
#                     Scenes.cluster_id,
#                     TuyaOnOffManufCluster.cluster_id
#                 ],
#                 OUTPUT_CLUSTERS: [
#                     Time.cluster_id, 
#                     Ota.cluster_id
#                 ]
#             },
#             242: {
#                 PROFILE_ID: 41440,
#                 DEVICE_TYPE: 97,
#                 INPUT_CLUSTERS: [],
#                 OUTPUT_CLUSTERS: [GreenPowerProxy.cluster_id]
#             }
#         }
#     }
#     replacement = {
#         ENDPOINTS: {
#             1: {
#                 DEVICE_TYPE: zha.DeviceType.ON_OFF_LIGHT,
#                 INPUT_CLUSTERS: [
#                     Basic.cluster_id,
#                     Groups.cluster_id,
#                     Scenes.cluster_id,
#                     TuyaOnOffManufCluster,
#                     TuyaOnOff,
#                 ],
#                 OUTPUT_CLUSTERS: [Time.cluster_id, Ota.cluster_id],
#             },
#             3: {
#                 PROFILE_ID: zha.PROFILE_ID,
#                 DEVICE_TYPE: zha.DeviceType.ON_OFF_LIGHT,
#                 INPUT_CLUSTERS: [
#                     TuyaOnOffManufCluster,
#                     TuyaOnOff,
#                 ],
#                 OUTPUT_CLUSTERS: [],
#             }
#         }
#     }

"""Tuya based cover and blinds."""
from typing import Dict

from zigpy.profiles import zha
from zigpy.quirks import CustomDevice
import zigpy.types as t
from zigpy.zcl.clusters.general import Basic, GreenPowerProxy, Groups, Ota, Scenes, Time
from zigpy.zcl.clusters.security import IasZone

from zhaquirks.const import (
    DEVICE_TYPE,
    ENDPOINTS,
    INPUT_CLUSTERS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
)
from zhaquirks.tuya import TuyaLocalCluster, ATTR_ON_OFF
from zhaquirks.tuya.mcu import (
    DPToAttributeMapping,
    TuyaDPType,
    TuyaMCUCluster,
    TuyaOnOff,
)

ZONE_TYPE = 0x0001

class TuyaZoneStatus(IasZone, TuyaLocalCluster):
    """Tuya MCU OnOff cluster."""

    attributes = {
        ATTR_ON_OFF: ("zone_status", t.Bool),
    }

    async def command(
        self,
        command_id: Union[foundation.GeneralCommand, int, t.uint8_t],
        *args,
        manufacturer: Optional[Union[int, t.uint16_t]] = None,
        expect_reply: bool = True,
        tsn: Optional[Union[int, t.uint8_t]] = None,
    ):
        """Override the default Cluster command."""

        self.debug(
            "Sending Tuya Cluster Command... Cluster Command is %x, Arguments are %s",
            command_id,
            args,
        )

        # (off, on)
        if command_id in (0x0000, 0x0001):
            cluster_data = TuyaClusterData(
                endpoint_id=self.endpoint.endpoint_id,
                cluster_attr="zone_status",
                attr_value=command_id,
                expect_reply=expect_reply,
                manufacturer=manufacturer,
            )
            self.endpoint.device.command_bus.listener_event(
                TUYA_MCU_COMMAND,
                cluster_data,
            )
            return foundation.GENERAL_COMMANDS[
                foundation.GeneralCommand.Default_Response
            ].schema(command_id=command_id, status=foundation.Status.SUCCESS)

        self.warning("Unsupported command_id: %s", command_id)
        return foundation.GENERAL_COMMANDS[
            foundation.GeneralCommand.Default_Response
        ].schema(command_id=command_id, status=foundation.Status.UNSUP_CLUSTER_COMMAND)

class ContactSwitchCluster(IasZone, TuyaLocalCluster):
    """Tuya ContactSwitch Sensor."""

    _CONSTANT_ATTRIBUTES = {ZONE_TYPE: IasZone.ZoneType.Contact_Switch}

    def _update_attribute(self, attrid, value):
        self.debug("_update_attribute '%s': %s", attrid, value)
        super()._update_attribute(attrid, value)


class TuyaGarageManufCluster(TuyaMCUCluster):
    """Tuya garage door opener."""

    attributes = TuyaMCUCluster.attributes.copy()
    attributes.update(
        {
            # ramdom attribute IDs
            0xEF02: ("dp_2", t.uint32_t, True),
            0xEF04: ("dp_4", t.uint32_t, True),
            0xEF05: ("dp_5", t.uint32_t, True),
            0xEF0B: ("dp_11", t.Bool, True),
            0xEF0C: ("dp_12", t.enum8, True),
        }
    )

    dp_to_attribute: Dict[int, DPToAttributeMapping] = {
        # garage door trigger ¿on movement, on open, on closed?
        1: DPToAttributeMapping(
            TuyaOnOff.ep_attribute,
            "on_off",
            dp_type=TuyaDPType.BOOL,
        ),
        2: DPToAttributeMapping(
            TuyaMCUCluster.ep_attribute,
            "dp_2",
            dp_type=TuyaDPType.VALUE,
        ),
        3: DPToAttributeMapping(
            TuyaZoneStatus.ep_attribute,
            "on_off",
            dp_type=TuyaDPType.BOOL,
            endpoint_id=2,
        ),
        4: DPToAttributeMapping(
            TuyaMCUCluster.ep_attribute,
            "dp_4",
            dp_type=TuyaDPType.VALUE,
        ),
        5: DPToAttributeMapping(
            TuyaMCUCluster.ep_attribute,
            "dp_5",
            dp_type=TuyaDPType.VALUE,
        ),
        11: DPToAttributeMapping(
            TuyaMCUCluster.ep_attribute,
            "dp_11",
            dp_type=TuyaDPType.BOOL,
        ),
        # garage door status (open, closed, ...)
        12: DPToAttributeMapping(
            TuyaMCUCluster.ep_attribute,
            "dp_12",
            dp_type=TuyaDPType.ENUM,
        ),
    }

    data_point_handlers = {
        1: "_dp_2_attr_update",
        2: "_dp_2_attr_update",
        3: "_dp_2_attr_update",
        4: "_dp_2_attr_update",
        5: "_dp_2_attr_update",
        11: "_dp_2_attr_update",
        12: "_dp_2_attr_update",
    }


class TuyaGarageSwitchTO(CustomDevice):
    """Tuya Garage switch."""

    signature = {
        MODELS_INFO: [
            ("_TZE200_nklqjk62", "TS0601"),
            ("_TZE200_wfxuhoea", "TS0601"),
        ],
        ENDPOINTS: {
            # <SimpleDescriptor endpoint=1 profile=260 device_type=0x0051
            # input_clusters=[0, 4, 5, 61184]
            # output_clusters=[10, 25]>
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.SMART_PLUG,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    TuyaGarageManufCluster.cluster_id,
                ],
                OUTPUT_CLUSTERS: [Time.cluster_id, Ota.cluster_id],
            },
            # <SimpleDescriptor endpoint=242 profile=41440 device_type=97
            # input_clusters=[]
            # output_clusters=[33]
            242: {
                PROFILE_ID: 41440,
                DEVICE_TYPE: 97,
                INPUT_CLUSTERS: [],
                OUTPUT_CLUSTERS: [GreenPowerProxy.cluster_id],
            },
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                DEVICE_TYPE: zha.DeviceType.ON_OFF_LIGHT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    TuyaGarageManufCluster,
                    TuyaOnOff,
                ],
                OUTPUT_CLUSTERS: [Time.cluster_id, Ota.cluster_id],
            },
            2: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.IAS_ZONE,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    TuyaZoneStatus,
                ],
                OUTPUT_CLUSTERS: [],
            },
            242: {
                PROFILE_ID: 0xA1E0,
                DEVICE_TYPE: 0x0061,
                INPUT_CLUSTERS: [],
                OUTPUT_CLUSTERS: [0x0021],
            },
        },
    }