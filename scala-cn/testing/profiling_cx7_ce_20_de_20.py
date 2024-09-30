import os
import configparser
import time
import subprocess
import pexpect
import traceback

config = configparser.ConfigParser()
config.read('../config.ini')
remote_ip = config['profiling']['remote_ip']
remote_pod_ip = config['profiling']['remote_pod_ip']
local_ip = config['profiling']['local_ip']
username = config['profiling']['username']
password = config['profiling']['password']

def send_string_and_wait(shell, command, wait_time, should_print):
    shell.send(command)
    time.sleep(wait_time)
    receive_buffer = shell.recv(1024)
    if should_print:
        return receive_buffer

def exec_local_cmd_timeout(cmd, timeout):
    p = subprocess.Popen([cmd], shell=True, stdin=subprocess.PIPE)

    sec = 0
    while True:
        if sec >= timeout or p.poll() is not None:
            break
        time.sleep(1)
        sec += 1
    p.kill()

def main():
    global remote_ip, local_ip, username, password
    verbs = ['send', 'write', 'read']
    metric = ['bw', 'lat']
    MAX_TEST_TC = 21

    cmd = 'echo 0 > /sys/module/mlx5_core/parameters/num_of_groups'
    os.system(cmd)
    p = pexpect.spawn('ssh %s@%s' % (username, remote_ip), encoding='utf8')
    p.expect('password', timeout=5)
    p.sendline(password)
    p.expect(username, timeout=5)
    p.sendline('sudo su -c bash')
    p.expect('password', timeout=5)
    p.sendline(password)
    p.expect('root', timeout=5)
    p.sendline(cmd)
    p.expect('root', timeout=5)

    for remote_decap in range(0, MAX_TEST_TC):
        rg = MAX_TEST_TC
        if remote_decap == 10:
            rg = 41
        for local_encap in range(0, rg):
            for v in verbs:
                for m in metric:
                    local_decap = 0
                    remote_encap = 0
                    try:
                        file_root = '~/cx7_fg_cen_20_sde_20/profiles'
                        file_leading = 'cen_%d_cde_%d_sen_%d_sde_%d_%s_%s' % (local_encap, local_decap, remote_encap, remote_decap, v, m)
                        file_path_remote = '%s_remote/%s' % (file_root, file_leading)
                        file_path_local = '%s_local/%s' % (file_root, file_leading)
                        filename_host_remote = '%s/%s_host.log' % (file_path_remote, file_leading)
                        filename_host_local = '%s/%s_host.log' % (file_path_local, file_leading)
                        filename_pod_remote = '%s/%s_pod.log' % (file_path_remote, file_leading)
                        filename_pod_local = '%s/%s_pod.log' % (file_path_local, file_leading)
                        if os.path.exists(filename_pod_local):
                            continue
                        if not os.path.exists(file_path_local):
                            os.makedirs(file_path_local)
                        p = pexpect.spawn('ssh %s@%s' % (username, remote_ip), encoding='utf8')
                        p.expect('password', timeout=5)
                        p.sendline(password)
                        p.expect(username, timeout=5)
                        p.sendline('sudo su -c bash')
                        p.expect('password', timeout=5)
                        p.sendline(password)
                        p.expect('root', timeout=5)
                        p.sendline('mkdir -p %s' % file_path_remote)
                        p.expect('root', timeout=5)
                        os.system('python3 ~/offloading/delete_all_tc.py')
                        os.system('python3 ~/offloading/offload.py -n %d --encap -p 1 -c' % local_encap)
                        os.system('python3 ~/offloading/offload.py -n %d --decap -p 1 -c' % local_decap)
                        
                        p.sendline('python3 ~/offloading/delete_all_tc.py')
                        p.expect('root', timeout=1200)
                        p.sendline('python3 ~/offloading/offload.py -n %d --encap -p 1 -c' % remote_encap)
                        p.expect('root', timeout=1200)
                        p.sendline('python3 ~/offloading/offload.py -n %d --decap -p 1 -c' % remote_decap)
                        p.expect('root', timeout=1200)

                        ib_cmd = 'ib_%s_%s' % (v, m)
                        cmd = ''
                        if 'bw' in m:
                            cmd = 'kubectl exec -i b01 -- %s -d mlx5_0 -q 4 -a > %s' % (ib_cmd, filename_pod_remote)
                        else:
                            cmd = 'kubectl exec -i b01 -- %s -d mlx5_0 -a > %s' % (ib_cmd, filename_pod_remote)
                        p.sendline(cmd)
                        time.sleep(1)
                        if 'bw' in m:
                            cmd = 'kubectl exec -i a01 -- %s -d mlx5_0 -q 4 -a %s > %s' % (ib_cmd, remote_pod_ip, filename_pod_local)
                        else:
                            cmd = 'kubectl exec -i a01 -- %s -d mlx5_0 -a %s > %s' % (ib_cmd, remote_pod_ip, filename_pod_local)
                        exec_local_cmd_timeout(cmd, 120)
                        os.system('pkill %s' % ib_cmd)
                        try:
                            p.expect('root', timeout=60)
                        except pexpect.exceptions.TIMEOUT:
                            p.sendline('pkill %s' % ib_cmd)

                        p.sendline('chown -R %s %s' % (username, file_path_remote))
                        p.expect('root', timeout=5)
                        p.sendline('chgrp -R %s %s' % ('users', file_path_remote))
                        p.expect('root', timeout=5)

                        p.sendline('exit')
                        p.expect(username, timeout=5)
                        p.sendline('rsync -avzh %s %s@%s:%s' % (file_path_remote, username, local_ip, '%s_remote' % file_root))
                        p.expect('speedup is', timeout=10)
                        p.sendline('exit')

                    except Exception as e:
                        traceback.print_exception(e)



if __name__ == '__main__':
    main()
