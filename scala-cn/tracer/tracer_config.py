TRACING_INTERVAL = 1

AGENT_BASE_PATH = '~/agent'

DP_TRACE_FILE = f'{AGENT_BASE_PATH}/ovs_dp.log'
FABRIC_TRACE_FILE = f'{AGENT_BASE_PATH}/fabric.log'
OVS_FLOW_TRACE_FILE = f'{AGENT_BASE_PATH}/ovs_flow.log'
OVS_TABLE_TRACE_FILE = f'{AGENT_BASE_PATH}/ovs_table.log'
TC_TRACE_FILE = f'{AGENT_BASE_PATH}/tc_monitor.log'
RDMA_TRACE_FILE = f'{AGENT_BASE_PATH}/rdma_flow_tables.pkl'


DP_CMD = f'echo "# `date +%s.%N`" >> {DP_TRACE_FILE} && ovs-dpctl show >> {DP_TRACE_FILE} && echo ">>>" >> {DP_TRACE_FILE}'
FABRIC_CMD = f'echo "# `date +%s.%N`" >> {FABRIC_TRACE_FILE} && [Proprietary Tool] >> {FABRIC_TRACE_FILE} && echo ">>>" >> {FABRIC_TRACE_FILE}'
OVS_FLOW_CMD = f'echo "# `date +%s.%N`" >> {OVS_FLOW_TRACE_FILE} && ovs-appctl dpctl/dump-flows --names -m >> {OVS_FLOW_TRACE_FILE} && echo ">>>" >> {OVS_FLOW_TRACE_FILE}'
OVS_TABLE_CMD = f'echo "# `date +%s.%N`" >> {OVS_TABLE_TRACE_FILE} && ovs-ofctl dump-flows br-int --names -m >> {OVS_TABLE_TRACE_FILE} && echo ">>>" >> {OVS_TABLE_TRACE_FILE}'
TC_CMD = 'tc -timestamp monitor'
