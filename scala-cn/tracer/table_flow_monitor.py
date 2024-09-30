import os
import time
import subprocess

while True:
    cmd = 'ovs-ofctl dump-flows br-int'
    ret = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    flow_table = ret.stdout
    cmd = 'ovs-appctl dpctl/dump-flows --names -m'
    ret = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    flow_info = ret.stdout
    print(flow_table)
    print()
    print(flow_info)
    time.sleep(5)
