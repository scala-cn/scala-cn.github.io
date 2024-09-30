from enum import Enum
import common.mlx_resdump.mstresourcedump as mstresourcedump
from common.mlx_resdump.segments.Segment import Segment
from typing import Dict, List
import struct
from abc import ABC, abstractmethod

class HeadersL2to4():
    def __init__(self) -> None:
        self.smac_47_16: int = None
        self.smac_15_0: int = None
        self.ethertype: int = None
        self.dmac_47_16: int = None
        self.dmac_15_0: int = None
        self.first_prio: int = None
        self.first_cfi: int = None
        self.first_vid: int = None
        self.ip_protocol: int = None
        self.ip_dscp: int = None
        self.ip_ecn: int = None
        self.cvlan_tag: int = None
        self.svlan_tag: int = None
        self.frag: int = None
        self.ip_version: int = None
        self.tcp_flags: int = None
        self.tcp_sport: int = None
        self.tcp_dport: int = None
        self.ip_ttl_hoplimit: int = None
        self.udp_sport: int = None
        self.udp_dport: int = None
        self.src_ipv4_or_ipv6: int = None
        self.dst_ipv4_or_ipv6: int = None

class MiscParameters():
    def __init__(self) -> None:
        self.source_sqn: int = None
        self.source_vhca_port: int = None
        self.gre_s_present: int = None
        self.gre_k_present: int = None
        self.gre_c_present: int = None
        self.source_port: int = None
        self.source_eswitch_owner_vhca_id: int = None
        self.inner_second_vid: int = None
        self.inner_second_cfi: int = None
        self.inner_second_prio: int = None
        self.outer_second_vid: int = None
        self.outer_second_cfi: int = None
        self.outer_second_prio: int = None
        self.gre_protocol: int = None
        self.outer_emd_tag: int = None
        self.inner_second_svlan_tag: int = None
        self.outer_second_svlan_tag: int = None
        self.inner_second_cvlan_tag: int = None
        self.outer_second_cvlan_tag: int = None
        self.gre_key_l: int = None
        self.gre_key_h: int = None
        self.vxlan_vni: int = None
        self.geneve_oam: int = None
        self.geneve_tlv_option_0_exist: int = None
        self.geneve_vni: int = None
        self.outer_ipv6_flow_label: int = None
        self.inner_ipv6_flow_label: int = None
        self.geneve_protocol_type: int = None
        self.geneve_opt_len: int = None
        self.geneve_c: int = None
        self.geneve_ver: int = None
        self.inner_ipv6_extension: int = None
        self.outer_ipv6_extension: int = None
        self.bth_dst_qp: int = None
        self.inner_esp_spi: int = None
        self.outer_esp_spi: int = None
        self.outer_emd_tag_data_0: int = None
        self.outer_emd_tag_data_1: int = None
        self.outer_emd_tag_data_2: int = None
        self.outer_emd_tag_data_3: int = None
        self.outer_emd_tag_data_4: int = None
        self.outer_emd_tag_data_5: int = None

class MiscParameters2():
    def __init__(self) -> None:
        self.outer_first_mpls_ttl: int = None
        self.outer_first_mpls_s_bos: int = None
        self.outer_first_mpls_exp: int = None
        self.outer_first_mpls_label: int = None
        self.inner_first_mpls_ttl: int = None
        self.inner_first_mpls_s_bos: int = None
        self.inner_first_mpls_exp: int = None
        self.inner_first_mpls_label: int = None
        self.outer_first_mpls_over_gre_ttl: int = None
        self.outer_first_mpls_over_gre_s_bos: int = None
        self.outer_first_mpls_over_gre_exp: int = None
        self.outer_first_mpls_over_gre_label: int = None
        self.outer_first_mpls_over_udp_ttl: int = None
        self.outer_first_mpls_over_udp_s_bos: int = None
        self.outer_first_mpls_over_udp_exp: int = None
        self.outer_first_mpls_over_udp_label: int = None
        self.metadata_reg_c_7: int = None
        self.metadata_reg_c_6: int = None
        self.metadata_reg_c_5: int = None
        self.metadata_reg_c_4: int = None
        self.metadata_reg_c_3: int = None
        self.metadata_reg_c_2: int = None
        self.metadata_reg_c_1: int = None
        self.metadata_reg_c_0: int = None
        self.metadata_reg_c_a: int = None
        self.ipsec_next_header: int = None
        self.ipsec_syndrome: int = None

class MiscParameters3():
    def __init__(self) -> None:
        self.inner_tcp_seq_num: int = None
        self.outer_tcp_seq_num: int = None
        self.inner_tcp_ack_num: int = None
        self.outer_tcp_ack_num: int = None
        self.outer_vxlan_gpe_vni: int = None
        self.outer_vxlan_gpe_flags: int = None
        self.outer_vxlan_gpe_next_protocol: int = None
        self.icmp_header_data: int = None
        self.icmpv6_header_data: int = None
        self.icmpv6_code: int = None
        self.icmpv6_type: int = None
        self.icmp_code: int = None
        self.icmp_type: int = None
        self.geneve_tlv_option_0_data: int = None
        self.gtpu_teid: int = None
        self.gtpu_msg_flags: int = None
        self.gtpu_msg_type: int = None

class VLANTag():
    def __init__(self) -> None:
        self.vid: int = None
        self.dei: int = None
        self.pcp: int = None
        self.tpid: int = None

class RDMAFlowMatcher():
    def __init__(self) -> None:
        self.outer_headers: HeadersL2to4 = HeadersL2to4()
        self.misc_parameters: MiscParameters = MiscParameters()
        self.inner_headers: HeadersL2to4 = HeadersL2to4()
        self.misc_parameters2: MiscParameters2 = MiscParameters2()
        self.misc_parameters3: MiscParameters3 = MiscParameters3()

class RDMAFlowContext():
    def __init__(self) -> None:
        self.vlan_tag: VLANTag = VLANTag()
        self.group_id: int = None
        self.flow_tag: int = None
        self.action: int = None
        self.destination_list_size: int = None
        self.flow_source: int = None
        self.extended_destination: int = None
        self.flow_counter_list_size: int = None
        self.packet_reformat_id: int = None
        self.modify_header_id: int = None
        self.vlan_2_tag: VLANTag = VLANTag()
        self.ipsec_obj_id: int = None
        self.match_value: RDMAFlowMatcher = RDMAFlowMatcher()
        self.basic_and_extended_destination_and_counter_list: bytes = None

class RDMAFlowTableContext():
    def __init__(self) -> None:
        self.log_size: int = None
        self.level: int = None
        self.table_type: int = None
        self.valid: int = None
        self.table_miss_action: int = None # i.e., table_miss_mode
        self.termination_table: int = None
        self.sw_owner: int = None
        # self.table_miss_mode: int = None
        self.table_miss_id: int = None
        self.reformat_en: int = None
        self.decap_en: int = None
        self.lag_master_next_table_id: int = None
        self.vport_num: int = None
        self.sw_owner_icm_root_1: int = None
        self.sw_owner_icm_root_0: int = None

class RDMAParsable(ABC):
    _RAW_DATA_START_PARSE_OFFSET = 0x10 # 16 bytes

    @abstractmethod
    def parse_from_resource_dump(self, raw_data: bytes):
        pass

    def __parse_misc_parameters_3(self, ptr: bytes) -> MiscParameters3:
        misc_parameters3 = MiscParameters3()
        misc_parameters3.inner_tcp_seq_num = struct.unpack('I', ptr[0x0:0x4])[0]
        misc_parameters3.outer_tcp_seq_num = struct.unpack('I', ptr[0x4:0x8])[0]
        misc_parameters3.inner_tcp_ack_num = struct.unpack('I', ptr[0x8:0xC])[0]
        misc_parameters3.outer_tcp_ack_num = struct.unpack('I', ptr[0xC:0x10])[0]
        misc_parameters3.outer_vxlan_gpe_vni = struct.unpack('I', ptr[0x10:0x14])[0] & 0x00FFFFFF
        misc_parameters3.outer_vxlan_gpe_flags, misc_parameters3.outer_vxlan_gpe_next_protocol = struct.unpack('xxBB', ptr[0x14:0x18])
        misc_parameters3.icmp_header_data = struct.unpack('I', ptr[0x18:0x1C])[0]
        misc_parameters3.icmpv6_header_data = struct.unpack('I', ptr[0x1C:0x20])[0]
        misc_parameters3.icmpv6_code, misc_parameters3.icmpv6_type, \
        misc_parameters3.icmp_code, misc_parameters3.icmp_type = struct.unpack('BBBB', ptr[0x20:0x24])
        misc_parameters3.geneve_tlv_option_0_data = struct.unpack('I', ptr[0x24:0x28])[0]
        misc_parameters3.gtpu_teid = struct.unpack('I', ptr[0x28:0x2C])[0]
        misc_parameters3.gtpu_msg_flags, misc_parameters3.gtpu_msg_type = struct.unpack('xxBB', ptr[0x2C:0x30])
        return misc_parameters3

    def __parse_misc_parameters_2(self, ptr: bytes):
        misc_parameters2 = MiscParameters2()
        tmp_word = struct.unpack('I', ptr[0x0:0x4])[0]
        misc_parameters2.outer_first_mpls_ttl = tmp_word & 0x000000FF
        misc_parameters2.outer_first_mpls_s_bos = (tmp_word & 0x00000100) >> 8
        misc_parameters2.outer_first_mpls_exp = (tmp_word & 0x00000E00) >> 9
        misc_parameters2.outer_first_mpls_label = (tmp_word & 0xFFFFF000) >> 12
        tmp_word = struct.unpack('I', ptr[0x4:0x8])[0]
        misc_parameters2.inner_first_mpls_ttl = tmp_word & 0x000000FF
        misc_parameters2.inner_first_mpls_s_bos = (tmp_word & 0x00000100) >> 8
        misc_parameters2.inner_first_mpls_exp = (tmp_word & 0x00000E00) >> 9
        misc_parameters2.inner_first_mpls_label = (tmp_word & 0xFFFFF000) >> 12
        tmp_word = struct.unpack('I', ptr[0x8:0xC])[0]
        misc_parameters2.outer_first_mpls_over_gre_ttl = tmp_word & 0x000000FF
        misc_parameters2.outer_first_mpls_over_gre_s_bos = (tmp_word & 0x00000100) >> 8
        misc_parameters2.outer_first_mpls_over_gre_exp = (tmp_word & 0x00000E00) >> 9
        misc_parameters2.outer_first_mpls_over_gre_label = (tmp_word & 0xFFFFF000) >> 12
        tmp_word = struct.unpack('I', ptr[0xC:0x10])[0]
        misc_parameters2.outer_first_mpls_over_udp_ttl = tmp_word & 0x000000FF
        misc_parameters2.outer_first_mpls_over_udp_s_bos = (tmp_word & 0x00000100) >> 8
        misc_parameters2.outer_first_mpls_over_udp_exp = (tmp_word & 0x00000E00) >> 9
        misc_parameters2.outer_first_mpls_over_udp_label = (tmp_word & 0xFFFFF000) >> 12
        misc_parameters2.metadata_reg_c_7 = struct.unpack('I', ptr[0x10:0x14])[0]
        misc_parameters2.metadata_reg_c_6 = struct.unpack('I', ptr[0x14:0x18])[0]
        misc_parameters2.metadata_reg_c_5 = struct.unpack('I', ptr[0x18:0x1C])[0]
        misc_parameters2.metadata_reg_c_4 = struct.unpack('I', ptr[0x1C:0x20])[0]
        misc_parameters2.metadata_reg_c_3 = struct.unpack('I', ptr[0x20:0x24])[0]
        misc_parameters2.metadata_reg_c_2 = struct.unpack('I', ptr[0x24:0x28])[0]
        misc_parameters2.metadata_reg_c_1 = struct.unpack('I', ptr[0x28:0x2C])[0]
        misc_parameters2.metadata_reg_c_0 = struct.unpack('I', ptr[0x2C:0x30])[0]
        misc_parameters2.metadata_reg_c_a = struct.unpack('I', ptr[0x30:0x34])[0]
        tmp_word = struct.unpack('I', ptr[0x34:0x38])[0]
        misc_parameters2.ipsec_next_header = tmp_word & 0x000000FF
        misc_parameters2.ipsec_syndrome = (tmp_word & 0x0000FF00) >> 8
        return misc_parameters2

    def __parse_headers_l2_to_4(self, ptr: bytes) -> HeadersL2to4:
        headers = HeadersL2to4()
        headers.smac_47_16 = struct.unpack('I', ptr[0x0:0x4])[0]
        tmp_word = struct.unpack('I', ptr[0x4:0x8])[0]
        headers.smac_15_0 = (tmp_word & 0xFFFF0000) >> 16
        headers.ethertype = tmp_word & 0x0000FFFF
        headers.dmac_47_16 = struct.unpack('I', ptr[0x8:0xC])[0]
        tmp_word = struct.unpack('I', ptr[0xC:0x10])[0]
        headers.first_vid = tmp_word & 0x00000FFF
        headers.first_cfi = (tmp_word & 0x00001000) >> 12
        headers.first_prio = (tmp_word & 0x00006000) >> 13
        headers.dmac_15_0 = (tmp_word & 0xFFFF0000) >> 16
        tmp_word = struct.unpack('I', ptr[0x10:0x14])[0]
        headers.tcp_flags = tmp_word & 0x000001FF
        headers.ip_version = (tmp_word & 0x00001E00) >> 9
        headers.frag = (tmp_word & 0x00002000) >> 13
        headers.svlan_tag = (tmp_word & 0x00004000) >> 14
        headers.cvlan_tag = (tmp_word & 0x00008000) >> 15
        headers.ip_ecn = (tmp_word & 0x00030000) >> 16
        headers.ip_dscp = (tmp_word & 0x00FC0000) >> 18
        headers.ip_protocol = (tmp_word & 0xFF000000) >> 24
        tmp_word = struct.unpack('I', ptr[0x14:0x18])[0]
        headers.tcp_dport = tmp_word & 0x0000FFFF
        headers.tcp_sport = (tmp_word & 0xFFFF0000) >> 16
        headers.ip_ttl_hoplimit = struct.unpack('B', ptr[0x18:0x19])[0]
        tmp_word = struct.unpack('I', ptr[0x1C:0x20])[0]
        headers.udp_dport = tmp_word & 0x0000FFFF
        headers.udp_sport = (tmp_word & 0xFFFF0000) >> 16
        headers.src_ipv4_or_ipv6 = struct.unpack('Q', ptr[0x20:0x28])[0] << 64
        headers.src_ipv4_or_ipv6 += struct.unpack('Q', ptr[0x28:0x30])[0]
        headers.dst_ipv4_or_ipv6 = struct.unpack('Q', ptr[0x30:0x38])[0] << 64
        headers.dst_ipv4_or_ipv6 += struct.unpack('Q', ptr[0x38:0x40])[0]
        return headers

    def __parse_misc_parameters(self, ptr: bytes) -> MiscParameters:
        misc_parameters = MiscParameters
        tmp_word = struct.unpack('I', ptr[0x0:0x4])[0]
        misc_parameters.source_sqn = tmp_word & 0x00FFFFFF
        misc_parameters.source_vhca_port = (tmp_word & 0x0F000000) >> 24
        misc_parameters.gre_s_present = (tmp_word & 0x10000000) >> 28
        misc_parameters.gre_k_present = (tmp_word & 0x20000000) >> 29
        misc_parameters.gre_c_present = (tmp_word & 0x80000000) >> 31
        tmp_word = struct.unpack('I', ptr[0x4:0x8])[0]
        misc_parameters.source_port = tmp_word & 0x0000FFFF
        misc_parameters.source_eswitch_owner_vhca_id = (tmp_word & 0xFFFF0000) >> 16
        tmp_word = struct.unpack('I', ptr[0x8:0xC])[0]
        misc_parameters.inner_second_vid = tmp_word & 0x00000FFF
        misc_parameters.inner_second_cfi = (tmp_word & 0x00001000) >> 12
        misc_parameters.inner_second_prio = (tmp_word & 0x0000E000) >> 13
        misc_parameters.outer_second_vid = (tmp_word & 0x0FFF0000) >> 16
        misc_parameters.outer_second_cfi = (tmp_word & 0x10000000) >> 28
        misc_parameters.outer_second_prio = (tmp_word & 0xE0000000) >> 29
        tmp_word = struct.unpack('I', ptr[0xC:0x10])[0]
        misc_parameters.gre_protocol = tmp_word & 0x0000FFFF
        misc_parameters.outer_emd_tag = (tmp_word & 0x08000000) >> 27
        misc_parameters.inner_second_svlan_tag = (tmp_word & 0x10000000) >> 28
        misc_parameters.outer_second_svlan_tag = (tmp_word & 0x20000000) >> 29
        misc_parameters.inner_second_cvlan_tag = (tmp_word & 0x40000000) >> 30
        misc_parameters.outer_second_cvlan_tag = (tmp_word & 0x80000000) >> 31
        tmp_word = struct.unpack('I', ptr[0x10:0x14])[0]
        misc_parameters.gre_key_l = (tmp_word & 0x0000000F) >> 29
        misc_parameters.gre_key_h = (tmp_word & 0xFFFFFFF0) >> 8
        tmp_word = struct.unpack('I', ptr[0x14:0x18])[0]
        misc_parameters.vxlan_vni = (tmp_word & 0xFFFFFFF0) >> 8
        tmp_word = struct.unpack('I', ptr[0x18:0x1C])[0]
        misc_parameters.geneve_oam = tmp_word & 0x00000001
        misc_parameters.geneve_tlv_option_0_exist = (tmp_word & 0x00000002) >> 1
        misc_parameters.vxlan_vni = (tmp_word & 0xFFFFFFF0) >> 8
        tmp_word = struct.unpack('I', ptr[0x1C:0x20])[0]
        misc_parameters.outer_ipv6_flow_label = tmp_word & 0x000FFFFF
        tmp_word = struct.unpack('I', ptr[0x20:0x24])[0]
        misc_parameters.inner_ipv6_flow_label = tmp_word & 0x000FFFFF
        tmp_word = struct.unpack('I', ptr[0x24:0x28])[0]
        misc_parameters.geneve_protocol_type = tmp_word & 0x0000FFFF
        misc_parameters.geneve_opt_len = (tmp_word & 0x003F0000) >> 16
        misc_parameters.geneve_c = (tmp_word & 0x00800000) >> 23
        misc_parameters.geneve_ver = (tmp_word & 0x03000000) >> 24
        misc_parameters.inner_ipv6_extension = (tmp_word & 0x4000000) >> 30
        misc_parameters.outer_ipv6_extension = (tmp_word & 0x80000000) >> 31
        tmp_word = struct.unpack('I', ptr[0x28:0x2C])[0]
        misc_parameters.inner_ipv6_flow_label = tmp_word & 0x00FFFFFF
        misc_parameters.inner_esp_spi = struct.unpack('I', ptr[0x2C:0x30])[0]
        misc_parameters.outer_esp_spi = struct.unpack('I', ptr[0x30:0x34])[0]
        misc_parameters.outer_emd_tag_data_3, misc_parameters.outer_emd_tag_data_2, \
        misc_parameters.outer_emd_tag_data_1, misc_parameters.outer_emd_tag_data_0 = struct.unpack('BBBB', ptr[0x38:0x3C])
        misc_parameters.outer_emd_tag_data_5, misc_parameters.outer_emd_tag_data_4 = struct.unpack('xxBB', ptr[0x3C:0x40])
        return misc_parameters

    def _parse_flow_matcher(self, ptr: bytes) -> RDMAFlowMatcher:
        matcher = RDMAFlowMatcher()
        matcher.outer_headers = self.__parse_headers_l2_to_4(ptr[0x0:0x40])
        matcher.misc_parameters = self.__parse_misc_parameters(ptr[0x40:0x80])
        matcher.inner_headers = self.__parse_headers_l2_to_4(ptr[0x80:0xC0])
        matcher.misc_parameters2 = self.__parse_misc_parameters_2(ptr[0xC0:0x100])
        matcher.misc_parameters3 = self.__parse_misc_parameters_3(ptr[0x100:0x140])
        return matcher

    def __parse_vlan_tag(self, ptr: bytes) -> VLANTag:
        vlan_tag: VLANTag = VLANTag()
        tmp_word = struct.unpack('I', ptr)[0]
        vlan_tag.vid = tmp_word & 0x00000FFF
        vlan_tag.dei = (tmp_word & 0x00001000) >> 12
        vlan_tag.pcp = (tmp_word & 0x0000E000) >> 13
        vlan_tag.tpid = (tmp_word & 0xFFFF0000) >> 16
        return vlan_tag

    def _parse_flow_context(self, ptr: bytes) -> RDMAFlowContext:
        flow_context: RDMAFlowContext = RDMAFlowContext()
        flow_context.vlan_tag = self.__parse_vlan_tag(ptr[0x0:0x4])
        flow_context.group_id = struct.unpack('I', ptr[0x4:0x8])[0]
        flow_context.action = struct.unpack('I', ptr[0x8:0xC])[0] & 0x0000FFFF
        tmp_word = struct.unpack('I', ptr[0x10:0x14])[0]
        flow_context.destination_list_size = tmp_word & 0x00FFFFFF
        flow_context.flow_source = (tmp_word & 0x30000000) >> 28
        flow_context.extended_destination = (tmp_word & 0x80000000) >> 32
        flow_context.flow_counter_list_size = struct.unpack('I', ptr[0x14:0x18])[0] & 0x00FFFFFF
        flow_context.packet_reformat_id = struct.unpack('I', ptr[0x18:0x1C])[0]
        flow_context.modify_header_id = struct.unpack('I', ptr[0x1C:0x20])[0]
        flow_context.vlan_2_tag = self.__parse_vlan_tag(ptr[0x20:0x24])
        flow_context.ipsec_obj_id = struct.unpack('I', ptr[0x24:0x28])[0]
        flow_context.match_value = self._parse_flow_matcher(ptr[0x40:0x240])
        flow_context.basic_and_extended_destination_and_counter_list = ptr[0x300:]
        return flow_context

    def _parse_flow_table_context(self, ptr: bytes) -> RDMAFlowTableContext:
        flow_table_context: RDMAFlowTableContext = RDMAFlowTableContext()
        flow_table_context.log_size, flow_table_context.level, tmp_byte = struct.unpack('BxBB', ptr[0x0:0x4])
        flow_table_context.table_miss_action = tmp_byte & 0xF
        flow_table_context.termination_table = (tmp_byte >> 4) & 0x1
        flow_table_context.sw_owner = (tmp_byte >> 5) & 0x1
        flow_table_context.decap_en = (tmp_byte >> 6) & 0x1
        flow_table_context.reformat_en = (tmp_byte >> 7) & 0x1
        flow_table_context.table_miss_id = struct.unpack('I', ptr[0x4:0x8])[0] & 0x0FFF
        flow_table_context.lag_master_next_table_id = struct.unpack('I', ptr[0x8:0xC])[0] & 0x0FFF
        flow_table_context.sw_owner_icm_root_1 = struct.unpack('Q', ptr[0x18:0x20])[0]
        flow_table_context.sw_owner_icm_root_0 = struct.unpack('Q', ptr[0x20:0x28])[0]
        flow_table_context.table_type, flow_table_context.vport_num = struct.unpack('BB', ptr[0x28:0x2A])
        return flow_table_context


class RDMACommandResource(Enum):
    QUERY_FT_ALL = 'QUERY_FT_ALL'
    QUERY_FT = 'QUERY_FT'
    QUERY_FG_ALL = 'QUERY_FG_ALL'
    QUERY_FG = 'QUERY_FG'
    QUERY_FTE_ALL = 'QUERY_FTE_ALL'
    QUERY_FTE = 'QUERY_FTE'

class RDMACommandRequestType(Enum):
    QUERY = 'query'
    DUMP = 'dump'

class RDMACommandRequest():
    
    @staticmethod
    def query_all_ft_id(dev_id: str) -> List[Segment]:
        cmd = [RDMACommandRequestType.DUMP.value, '--device', dev_id, '--segment', RDMACommandResource.QUERY_FT_ALL.value]
        return mstresourcedump.dump_request(cmd)
    
    @staticmethod
    def query_all_ft_id_context(dev_id: str) -> List[Segment]:
        cmd = [RDMACommandRequestType.DUMP.value, '--device', dev_id, '--segment', RDMACommandResource.QUERY_FT_ALL.value, '--depth', '1']
        return mstresourcedump.dump_request(cmd)
    
    @staticmethod
    def query_ft_by_id(dev_id: str, table_id: int) -> List[Segment]:
        cmd = [RDMACommandRequestType.DUMP.value, '--device', dev_id, '--segment', RDMACommandResource.QUERY_FT.value, '--index1', str(table_id)]
        return mstresourcedump.dump_request(cmd)

    @staticmethod
    def query_all_fg_id(dev_id: str, table_id: int) -> List[Segment]:
        cmd = [RDMACommandRequestType.DUMP.value, '--device', dev_id, '--segment', RDMACommandResource.QUERY_FG_ALL.value, '--index1', str(table_id)]
        return mstresourcedump.dump_request(cmd)
    
    @staticmethod
    def query_all_fg_id_content(dev_id: str, table_id: int) -> List[Segment]:
        cmd = [RDMACommandRequestType.DUMP.value, '--device', dev_id, '--segment', RDMACommandResource.QUERY_FG_ALL.value, '--index1', str(table_id), '--depth', '1']
        return mstresourcedump.dump_request(cmd)
    
    @staticmethod
    def query_fg_by_id(dev_id: str, table_id: int, group_id: int) -> List[Segment]:
        cmd = [RDMACommandRequestType.DUMP.value, '--device', dev_id, '--segment', RDMACommandResource.QUERY_FG.value, '--index1', str(table_id), '--index2', str(group_id)]
        return mstresourcedump.dump_request(cmd)

    @staticmethod
    def query_all_fte_id(dev_id: str, table_id: int) -> List[Segment]:
        cmd = [RDMACommandRequestType.DUMP.value, '--device', dev_id, '--segment', RDMACommandResource.QUERY_FTE_ALL.value, '--index1', str(table_id)]
        return mstresourcedump.dump_request(cmd)

    @staticmethod
    def query_all_fte_id_context(dev_id: str, table_id: int) -> List[Segment]:
        cmd = [RDMACommandRequestType.DUMP.value, '--device', dev_id, '--segment', RDMACommandResource.QUERY_FTE_ALL.value, '--index1', str(table_id), '--depth', '1']
        return mstresourcedump.dump_request(cmd)
    
    @staticmethod
    def query_fte_by_id(dev_id: str, table_id: int, flow_index: int) -> List[Segment]:
        cmd = [RDMACommandRequestType.DUMP.value, '--device', dev_id, '--segment', RDMACommandResource.QUERY_FTE.value, '--index1', str(table_id), '--index2', str(flow_index)]
        return mstresourcedump.dump_request(cmd)


class RDMAFlowTable(RDMAParsable):
    __FLOW_TABLE_CONTEXT_OFFSET = 0x18 # 24 bytes
    
    def parse_from_resource_dump(self, raw_data: bytes):
        # Reference: Internal Mellanox Adapters PRM rev 0.52 Draft P1947
        ptr: bytes = raw_data[super()._RAW_DATA_START_PARSE_OFFSET: ]
        self.flow_table_context = super()._parse_flow_table_context(ptr[RDMAFlowTable.__FLOW_TABLE_CONTEXT_OFFSET: ])
    
    def __init__(self, table_id: int) -> None:
        super().__init__()
        self.table_id: int = table_id
        self.flow_table_context: RDMAFlowTableContext = None

        self.flow_groups: Dict[int, RDMAFlowGroup] = {}
        self.flow_table_entries: Dict[int, RDMAFlowTableEntry] = {}

class RDMAFlowTableEntry(RDMAParsable):
    __FLOW_CONTEXT_OFFSET = 0x40

    def parse_from_resource_dump(self, raw_data: bytes):
        # Reference: Internal Mellanox Adapters PRM rev 0.52 Draft P1947
        ptr: bytes = raw_data[super()._RAW_DATA_START_PARSE_OFFSET: ]
        self.flow_context = super()._parse_flow_context(ptr[RDMAFlowTableEntry.__FLOW_CONTEXT_OFFSET: ])

    def __init__(self, flow_index: int) -> None:
        super().__init__()
        self.flow_index: int = flow_index
        self.flow_context: RDMAFlowContext = RDMAFlowContext()

class RDMAFlowGroup(RDMAParsable):
    __MATCH_CRITERIA_OFFSET = 0x40

    def parse_from_resource_dump(self, raw_data: bytes):
        # Reference: Internal Mellanox Adapters PRM rev 0.52 Draft P1947
        ptr: bytes = raw_data[super()._RAW_DATA_START_PARSE_OFFSET: ]
        tmp_word = struct.unpack('I', ptr[0x18:0x1C])[0]
        self.outer_ip_type = tmp_word & 0x03
        self.inner_ip_type = (tmp_word & 0x0C) >> 2
        self.start_flow_index = struct.unpack('I', ptr[0x1C:0x20])[0]
        self.end_flow_index = struct.unpack('I', ptr[0x24:0x28])[0]
        self.match_criteria_enable = struct.unpack('B', ptr[0x3C:0x3D])[0]
        self.match_criteria = super()._parse_flow_matcher(ptr[RDMAFlowGroup.__MATCH_CRITERIA_OFFSET: ])
        
    def __init__(self, group_id: int) -> None:
        super().__init__()
        self.group_id: int = group_id
        self.table_id: int = None
        self.inner_ip_type: int = None
        self.outer_ip_type: int = None
        self.start_flow_index: int = None
        self.end_flow_index: int = None
        self.match_criteria_enable: int = None
        self.match_criteria: RDMAFlowMatcher = RDMAFlowMatcher()
    

