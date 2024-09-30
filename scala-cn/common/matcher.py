
from common.ovs_flow import *
from common.tc import *

class FlowEthType(Enum):
    ARP = 0x0806
    IPv4 = 0x0800
    IPv6 = 0x86DD

def tc_cookie_to_hex(cookie: str) -> str:
    cookie_chunks = ''
    for i in range(0, 32, 8):
        chunk = cookie[i: i+8]
        cookie_chunks += (chunk[6:8] + chunk[4:6] + chunk[2:4] + chunk[0:2])
    return cookie_chunks

def ufid_to_hex(ufid: str) -> str:
    return ufid.replace('-', '')

def flow_matched_by_tc_cookie(flow: OVSFlowItem, tc: TCItem) -> bool:
    cookie: str = None
    for tc_action in tc.actions:
        if tc_action.cookie is not None:
            cookie = tc_action.cookie
            break
    if cookie is None or len(cookie) != 32:
        return False
    return tc_cookie_to_hex(cookie) == ufid_to_hex(flow.ufid)
    

def flow_matched_by_tc_content(flow: OVSFlowItem, tc: TCItem) -> bool:
        if tc.dev != flow.in_port:
            return False
        if (tc.src_mac is None and flow.eth_src is not None) or \
            (tc.src_mac is not None and flow.eth_src is None) or \
            (tc.src_mac is not None and flow.eth_src is not None and \
            tc.src_mac.lower() != flow.eth_src.lower()):
            return False
        if (tc.dst_mac is None and flow.eth_dst is not None) or \
            (tc.dst_mac is not None and flow.eth_dst is None) or \
            (tc.dst_mac is not None and flow.eth_dst is not None and \
            tc.dst_mac.lower() != flow.eth_dst.lower()):
            return False
        if tc.eth_type != flow.eth_type:
            return False
        if tc.eth_type == FlowEthType.IPv4:
            if (tc.src_ipv4 is None and flow.ipv4_src is not None) or \
                (tc.src_ipv4 is not None and flow.ipv4_src is None) or \
                (tc.src_ipv4 is not None and flow.ipv4_src is not None and \
                not (flow.ipv4_src.network.subnet_of(tc.src_ipv4.network) or \
                     flow.ipv4_src.network == tc.src_ipv4.network)):
                return False
            if (tc.dst_ipv4 is None and flow.ipv4_dst is not None) or \
                (tc.dst_ipv4 is not None and flow.ipv4_dst is None) or \
                (tc.dst_ipv4 is not None and flow.ipv4_dst is not None and \
                not (flow.ipv4_dst.network.subnet_of(tc.dst_ipv4.network) or \
                     flow.ipv4_dst.network == tc.dst_ipv4.network)):
                return False
        if tc.eth_type == FlowEthType.IPv6:
            if (tc.src_ipv4 is None and flow.ipv6_src is not None) or \
                (tc.src_ipv4 is not None and flow.ipv6_src is None) or \
                (tc.src_ipv4 is not None and flow.ipv6_src is not None and \
                not (flow.ipv6_src.network.subnet_of(tc.src_ipv6.network) or \
                     flow.ipv6_src.network == tc.src_ipv6.network)):
                return False
            if (tc.dst_ipv4 is None and flow.ipv6_dst is not None) or \
                (tc.dst_ipv4 is not None and flow.ipv6_dst is None) or \
                (tc.dst_ipv4 is not None and flow.ipv6_dst is not None and \
                not (flow.ipv6_dst.network.subnet_of(tc.dst_ipv6.network) or \
                     flow.ipv6_dst.network == tc.dst_ipv6.network)):
                return False
        if (tc.enc_dst_ip is None and flow.tunnel_dst is not None) or \
            (tc.enc_dst_ip is not None and flow.tunnel_dst is None) or \
            (tc.enc_dst_ip is not None and flow.tunnel_dst is not None and \
            not flow.tunnel_dst.network.subnet_of(tc.enc_dst_ip.network)):
            return False
        if (tc.enc_src_ip is None and flow.tunnel_src is not None) or \
            (tc.enc_src_ip is not None and flow.tunnel_src is None) or \
            (tc.enc_src_ip is not None and flow.tunnel_src is not None and \
            not flow.tunnel_src.network.subnet_of(tc.enc_src_ip.network)):
            return False
        if tc.enc_dst_port != flow.tunnel_tp_dst:
            return False
        
        for tc_action in tc.actions:
            for flow_action in flow.actions:
                if tc_action.action_type == TCActionType.ETH_PEDIT and flow_action.action_type == OVSFlowActionType.SET_ETH:
                    if tc_action.eth_pedit.lower() != flow_action.eth_dst.lower():
                        return False
                elif tc_action.action_type == TCActionType.EGRESS_REDIRECT and flow_action.action_type == OVSFlowActionType.REDIRECT:
                    if tc_action.redirect_target != flow_action.redirect_target:
                        return False
                elif tc_action.action_type == TCActionType.TUNNEL_KEY_SET and flow_action.action_type == OVSFlowActionType.SET_TUNNEL:
                    if (tc_action.tunnel_dst_ip is None and flow_action.tunnel_dst_ip is not None) or \
                        (tc_action.tunnel_dst_ip is not None and flow_action.tunnel_dst_ip is None) or \
                        (tc_action.tunnel_dst_ip is not None and flow_action.tunnel_dst_ip is not None and \
                        not flow_action.tunnel_dst_ip.network.subnet_of(tc_action.tunnel_dst_ip.network)):
                        return False
                    if (tc_action.tunnel_src_ip is None and flow_action.tunnel_src_ip is not None) or \
                        (tc_action.tunnel_src_ip is not None and flow_action.tunnel_src_ip is None) or \
                        (tc_action.tunnel_src_ip is not None and flow_action.tunnel_src_ip is not None and \
                        not flow_action.tunnel_src_ip.network.subnet_of(tc_action.tunnel_src_ip.network)):
                        return False
                    if (tc_action.tunnel_dst_port is None and flow_action.tunnel_dst_port is not None) or \
                        (tc_action.tunnel_dst_port is not None and flow_action.tunnel_dst_port is None) or \
                        (tc_action.tunnel_dst_port is not None and flow_action.tunnel_dst_port is not None and \
                        tc_action.tunnel_dst_port != flow_action.tunnel_dst_port):
                        return False
        return True
