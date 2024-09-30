import os
from mlx_fs_dump import fancy_dump, flow_entry, flow_table, flow_group
import pandas as pd
from typing import List

client_ip_31_0 = 'IP(hex), e.g., 0x21fe2481'
server_ip_31_0 = 'IP(hex), e.g., 0x21fe2481'
client_pod_ip_31_0_prefix = 'IP(hex), e.g., 0x21fe2481'
server_pod_ip_31_0_prefix = 'IP(hex), e.g., 0x21fe2481'

def get_fg_hop(fte: flow_entry, entry_list: List[flow_entry]):
    p = fte.parent
    while not isinstance(p, flow_table):
        p = p.parent
    
    # Need to refine (recursive case)
    for entry in entry_list:
        if entry.dst_type == 'FLOW_TABLE' and entry.dst_value == p.table_id:
            p = entry
            while not isinstance(p, flow_table):
                p = p.parent
            break

    return len([k for k in p.children if isinstance(k, flow_group)])

def main():
    
    side = ['client', 'server']
    fte_type = ['ft_encap', 'ft_decap']
    action = ['encap', 'decap']
    verbs = ['send', 'write', 'read']
    metric = ['bw', 'lat']
    host_pod = ['host', 'pod']
    cols = ['key']
    for s in side:
        for t in fte_type:
            cols.append(f'{s}_{t}')
    for s in side:
        for a in action:
            cols.append(f'{s}_{a}')
    for v in verbs:
        for m in metric:
            for hp in host_pod:
                for s in side:
                    cols.append(f'{s}_{v}_{m}_{hp}')
    
    df = pd.DataFrame(columns=cols)

    if os.path.exists('../tmp/out.csv'):
        df = pd.read_csv('../tmp/out.csv')

    file_dirs = os.listdir('~/profiles/profiles_local', )
    file_dirs = sorted(file_dirs, key=lambda x: os.path.getmtime('~/profiles/profiles_local/%s' % x))
    processed = df['key'].tolist()
    for fdir in file_dirs:
        should_skip = False
        for i in range(4):
            if int(fdir.split('_')[2 * i + 1]) >= 200:
                should_skip = True
                break
        if should_skip:
            continue
        row_data = {}

        key_idx = 0

        for s in side:
            for t in fte_type:
                row_data[f'{s}_{t}'] = int(fdir.split('_')[2 * key_idx + 1])
                key_idx += 1
        key = '_'.join(fdir.split('_')[0:8])
        if key in processed:
            continue
        processed.append(key)
        row_data['key'] = key
                
        for s in side:
            for v in verbs:
                for m in metric:
                    dump = None
                    if s == 'client':
                        dump = fancy_dump(['-d', '18:00.0', '-f', f'~/profiles/profiles_local/{key}_{v}_{m}/{key}_{v}_{m}_ft_gvmi_0.txt'])
                    else:
                        dump = fancy_dump(['-d', '17:00.0', '-f', f'~/profiles/profiles_remote/{key}_{v}_{m}/{key}_{v}_{m}_ft_gvmi_0.txt'])
                    table_list, group_list, entry_list = dump.run()
                    for a in action:
                        hop = 0
                        for fte in entry_list:
                            if s == 'client' and a == 'encap':
                                if isinstance(fte, flow_entry) and fte.cr_found.index('outer_dst_ip_31_0') >= 0 \
                                    and (fte.cr_found[fte.cr_found.index('outer_dst_ip_31_0') + 1][0:-2] == server_pod_ip_31_0_prefix):
                                    hop = max(get_fg_hop(fte, entry_list), hop)
                            elif s == 'client' and a == 'decap':
                                if isinstance(fte, flow_entry) and fte.cr_found.index('inner_dst_ip_31_0') >= 0 \
                                    and (fte.cr_found[fte.cr_found.index('inner_dst_ip_31_0') + 1][0:-2] == client_pod_ip_31_0_prefix):
                                    hop = max(get_fg_hop(fte, entry_list), hop)
                            elif s == 'server' and a == 'encap':
                                if isinstance(fte, flow_entry) and fte.cr_found.index('outer_dst_ip_31_0') >= 0 \
                                    and (fte.cr_found[fte.cr_found.index('outer_dst_ip_31_0') + 1][0:-2] == client_pod_ip_31_0_prefix):
                                    hop = max(get_fg_hop(fte, entry_list), hop)
                            elif s == 'server' and a == 'decap':
                                if isinstance(fte, flow_entry) and fte.cr_found.index('inner_dst_ip_31_0') >= 0 \
                                    and (fte.cr_found[fte.cr_found.index('inner_dst_ip_31_0') + 1][0:-2] == server_pod_ip_31_0_prefix):
                                    hop = max(get_fg_hop(fte, entry_list), hop)
                        row_data[f'{s}_{a}'] = hop
                    for hp in host_pod:
                        log_filename = f'~/profiles/profiles_local/{key}_{v}_{m}/{key}_{v}_{m}_{hp}.log' if s == 'client' else f'~/profiles/profiles_remote/{key}_{v}_{m}/{key}_{v}_{m}_{hp}.log'
                        fp = open(log_filename, 'r')
                        lines = fp.readlines()
                        fp.close()
                        enter_data = False
                        data = ''
                        for line in lines:
                            if line.startswith(' #bytes'):
                                enter_data = True
                                continue
                            if not enter_data:
                                continue
                            if line.startswith('---'):
                                continue
                            data_split = line.split()
                            data = data_split[3] if m == 'bw' else data_split[4]
                            if m == 'lat':
                                break
                        row_data[f'{s}_{v}_{m}_{hp}'] = data
        df = pd.concat([pd.DataFrame(row_data, index=[0]), df], ignore_index=True)
        df = df[cols]
        df.to_csv('../tmp/out.csv')

if __name__ == '__main__':
    main()