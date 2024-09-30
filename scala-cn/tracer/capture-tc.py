import subprocess
import time
from threading import Thread
from threading import Lock
import sys
import re

last_active_time = -1
need_flush = False
to_file = False
lock = Lock()

def io_print(contents):
    if to_file:
        with open('tc_monitor.log', 'a') as f:
            f.write(contents)
            f.flush()
    print(contents, end='')
    sys.stdout.flush()

def flush_thread():
    global last_active_time, need_flush, lock
    while True:
        if last_active_time < 0:
            time.sleep(1)
            continue
        current_time = time.time()

        lock.acquire()
        if current_time - last_active_time > 1 and need_flush:
            io_print('>>>\n')
            need_flush = False
        lock.release()

        time.sleep(1)

def main():
    global last_active_time, need_flush, lock

    init_tc()

    cmd = 'tc -timestamp monitor'
    p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while True:
        for line in iter(p.stdout.readline, b''):
            line = line.decode('utf-8')
            if line.startswith('Timestamp'):

                lock.acquire()
                if need_flush:
                    io_print('>>>\n')
                    need_flush = False
                lock.release()

                io_print(line)
            else:
                last_active_time = time.time()
                io_print(line)
                
                lock.acquire()
                need_flush = True
                lock.release()
        if p.poll() is not None:
            break

def get_devs():
    cmd = '[Proprietary Tool]'
    p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    devs = []
    meet_interface = False
    break_count = 0
    begin_parsing = False
    for line in iter(p.stdout.readline, b''):
        line = line.decode('utf-8')
        if '[Proprietary Config]' in line:
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

def init_tc():
    devs = get_devs()
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
            io_print('# %f %s %s\n' % (time.time(), dev, dir))
            io_print('%s\n' % outstr)
            io_print('>>>\n')
    io_print('<<<\n')

if __name__ == '__main__':
    to_file = False
    if len(sys.argv) >= 2 and '-f' in sys.argv:
        to_file = True
    daemon_thread = Thread(target=flush_thread)
    daemon_thread.start()
    main()
