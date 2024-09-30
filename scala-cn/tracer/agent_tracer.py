from threading import Thread, Lock
import sys
import subprocess
import time
import tracer_config
from typing import List, Dict
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import pickle
import struct
from common.mlx_resdump.resdump_api import RDMACommandRequest, RDMAFlowTable, RDMAFlowGroup, RDMAFlowTableEntry
from common.mlx_resdump.segments.Segment import Segment


class TracingThread(Thread):
    def __init__(self) -> None:
        super().__init__()

class DataPathTracer(TracingThread):
    def __init__(self) -> None:
        super().__init__()
    
    def run(self):
        while True:
            subprocess.run(tracer_config.DP_CMD, shell=True)
            time.sleep(tracer_config.TRACING_INTERVAL)

class FabricTracer(TracingThread):
    def __init__(self) -> None:
        super().__init__()
    
    def run(self):
        while True:
            subprocess.run(tracer_config.FABRIC_CMD, shell=True)
            time.sleep(tracer_config.TRACING_INTERVAL)

class OVSFlowTracer(TracingThread):
    def __init__(self) -> None:
        super().__init__()
    
    def run(self):
        while True:
            subprocess.run(tracer_config.OVS_FLOW_CMD, shell=True)
            time.sleep(tracer_config.TRACING_INTERVAL)

class OVSTableTracer(TracingThread):
    def __init__(self) -> None:
        super().__init__()
    
    def run(self):
        while True:
            subprocess.run(tracer_config.OVS_TABLE_CMD, shell=True)
            time.sleep(tracer_config.TRACING_INTERVAL)

class RDMATracer(TracingThread):
    def __init__(self) -> None:
        super().__init__()
    
    def get_rdma_pci_id(self) -> List[str]:
        cmd = '[Proprietary Tool]'

        if sys.argv[0].endswith('.py'):
            cmd = '[Proprietary Tool]'

        rdma_buses: List[str] = []

        output: str = ''
        p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        phy_name = []

        while True:
            for line in iter(p.stdout.readline, b''):
                line = line.decode('utf-8')
                output += line
            if p.poll() is not None:
                break
        
        line_split = output.split(os.linesep)

        __count = 0
        meet_backends = False
        begin_parsing = False
        for line in line_split:
            if line.startswith('Backends:'):
                __count = 0
                meet_backends = True
            elif line.startswith('--'):
                if not meet_backends:
                    continue
                __count += 1
                if __count == 3:
                    break
                elif __count == 2:
                    begin_parsing = True
            elif begin_parsing:
                tmp = line.strip().split()
                if len(tmp) <= 1:
                    continue

                if tmp[1] in phy_name:
                    continue

                phy_name.append(tmp[1])

                if os.path.exists('/sys/class/net/%s/bonding/slaves' % tmp[1]):
                    slave_names: List[str] = []
                    with open('/sys/class/net/%s/bonding/slaves' % tmp[1], 'r') as f:
                        line = f.readline()
                        line = line.strip()
                        line_split = line.split()
                        for slave_name in line_split:
                            slave_names.append(slave_name)
                    for slave_name in slave_names:
                        config_path = '/sys/class/net/%s/device/uevent' % slave_name
                        if os.path.exists(config_path):
                            with open(config_path, 'r') as f:
                                lines = f.readlines()
                                for line in lines:
                                    line = line.strip()
                                    if line.startswith('PCI_SLOT_NAME'):
                                        pci_bus_id = line.split('=')[-1]
                                        if pci_bus_id.endswith('00.0'):
                                            rdma_buses.append(pci_bus_id)
            
        return rdma_buses
    
    def run(self):
        rdma_buses = self.get_rdma_pci_id()
        # print(rdma_buses)
        time_tables = []

        while True:
            flow_tables: Dict[int, RDMAFlowTable] = {}
            for bus_id in rdma_buses:
                segments: List[Segment] = RDMACommandRequest.query_all_ft_id_context(bus_id)
                for segment in segments:
                    if segment.get_type() == 0x4010:
                        segment_data = segment.get_data()
                        slice = segment_data[8:12]
                        table_id = struct.unpack('I', slice)[0]
                        flow_tables[table_id] = RDMAFlowTable(table_id)
                        flow_tables[table_id].parse_from_resource_dump(segment_data)

                for table_id in flow_tables:
                    segments: List[Segment] = RDMACommandRequest.query_all_fg_id_content(bus_id, table_id)
                    for segment in segments:
                        if segment.get_type() == 0x4012:
                            segment_data = segment.get_data()
                            slice = segment_data[8:16]
                            table_id, group_id = struct.unpack('II', slice)
                            flow_tables[table_id].flow_groups[group_id] = RDMAFlowGroup(group_id)
                            flow_tables[table_id].flow_groups[group_id].parse_from_resource_dump(segment_data)

                for table_id in flow_tables:
                    segments: List[Segment] = RDMACommandRequest.query_all_fte_id_context(bus_id, table_id)
                    for segment in segments:
                        if segment.get_type() == 0x4014:
                            segment_data = segment.get_data()
                            slice = segment_data[8:16]
                            table_id, flow_index = struct.unpack('II', slice)
                            flow_tables[table_id].flow_table_entries[flow_index] = RDMAFlowTableEntry(flow_index)
                            flow_tables[table_id].flow_table_entries[flow_index].parse_from_resource_dump(segment_data)
            
            time_tables.append({'time': time.time(), 'flow_tables': flow_tables})
            pickle.dump(time_tables, open(tracer_config.RDMA_TRACE_FILE, 'wb'))
            time.sleep(tracer_config.TRACING_INTERVAL)

class TCTracer(TracingThread):

    def __init__(self) -> None:
        super().__init__()

        self.last_active_time = -1
        self.need_flush = False
        self.lock = Lock()

    def io_print(self, contents):
        with open(tracer_config.TC_TRACE_FILE, 'a') as f:
            f.write(contents)
            f.flush()
        # print(contents, end='')
        sys.stdout.flush()

    def flush_thread(self):
        while True:
            if self.last_active_time < 0:
                time.sleep(1)
                continue
            current_time = time.time()

            self.lock.acquire()
            if current_time - self.last_active_time > 1 and self.need_flush:
                self.io_print('>>>\n')
                self.need_flush = False
            self.lock.release()

            time.sleep(1)

    def get_devs(self):
        cmd = '[Proprietary Tool]'
        p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        devs = []
        meet_interface = False
        break_count = 0
        begin_parsing = False
        for line in iter(p.stdout.readline, b''):
            line = line.decode('utf-8')
            if 'interface-ep' in line:
                meet_interface = True
                continue
            elif line.startswith('--'):
                if not meet_interface:
                    continue
                break_count += 1
                if break_count == 2:
                    break
                elif break_count == 1:
                    begin_parsing = True
            elif begin_parsing:
                try:
                    line_split = line.strip().split()
                    devs.append(line_split[1])
                except Exception as e:
                    pass
        cmd = 'ifconfig'
        p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in iter(p.stdout.readline, b''):
            line = line.decode('utf-8')
            if '[Proprietary Config]' in line:
                devs.append('[Proprietary Config]')
            elif '[Proprietary Config]' in line:
                devs.append('[Proprietary Config]')
            elif '[Proprietary Config]' in line:
                devs.append('[Proprietary Config]')
            elif '[Proprietary Config]' in line:
                devs.append('[Proprietary Config]')
        return devs

    def init_tc(self):
        devs = self.get_devs()
        for dev in devs:
            for dir in ['ingress', 'egress']:
                cmd = 'tc filter show dev %s %s' % (dev, dir)
                p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                outstr = ''
                while True:
                    for line in iter(p.stdout.readline, b''):
                        line = line.decode('utf-8')
                        outstr += line
                    if p.poll() is not None:
                        break
                self.io_print('# %f %s %s\n' % (time.time(), dev, dir))
                self.io_print('%s\n' % outstr)
                self.io_print('>>>\n')
        self.io_print('<<<\n')
    
    def run(self):

        daemon_thread = Thread(target=self.flush_thread, name='tc_flush')
        daemon_thread.start()

        self.init_tc()

        p = subprocess.Popen([tracer_config.TC_CMD], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        while True:
            for line in iter(p.stdout.readline, b''):
                line = line.decode('utf-8')
                if line.startswith('Timestamp'):

                    self.lock.acquire()
                    if self.need_flush:
                        self.io_print('>>>\n')
                        self.need_flush = False
                    self.lock.release()

                    self.io_print(line)
                else:
                    self.last_active_time = time.time()
                    self.io_print(line)
                    
                    self.lock.acquire()
                    self.need_flush = True
                    self.lock.release()
            if p.poll() is not None:
                break

def main():
    tracers: List[TracingThread] = [RDMATracer(), DataPathTracer(), FabricTracer(), OVSFlowTracer(), OVSTableTracer(), TCTracer()]
    for t in tracers:
        t.start()
    for t in tracers:
        t.join()

if __name__ == '__main__':
    main()