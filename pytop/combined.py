
TEST = """
pid, process_name, used_gpu_memory [MiB], gpu_bus_id
3238, python, 4239 MiB, 0000:01:00.0
5076, python, 4239 MiB, 0000:01:00.0
9861, python, 3475 MiB, 0000:01:00.0
2780, python, 4239 MiB, 0000:03:00.0
14407, python, 3475 MiB, 0000:03:00.0
27617, python, 4239 MiB, 0000:03:00.0
9179, python, 4237 MiB, 0000:04:00.0
11895, python, 4237 MiB, 0000:04:00.0
BREAK
name, pci.bus_id, memory.total [MiB], memory.used [MiB], utilization.gpu [%], temperature.gpu
TITAN X (Pascal),0000:01:00.0, 12189 MiB, 11964 MiB, 54 %, 67
TITAN X (Pascal),0000:02:00.0, 12189 MiB, 11 MiB, 0 %, 50
TITAN X (Pascal),0000:03:00.0, 12189 MiB, 11964 MiB, 53 %, 76
TITAN X (Pascal),0000:04:00.0, 12186 MiB, 8717 MiB, 32 %, 83
BREAK
top - 23:48:46 up 14 days,  5:00, 20 users,  load average: 22.49, 23.87, 24.32
Tasks: 401 total,   6 running, 394 sleeping,   1 stopped,   0 zombie
%Cpu(s): 38.0 us,  8.5 sy,  0.0 ni, 50.9 id,  2.6 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem : 32841076 total, 21244832 free,  8063012 used,  3533232 buff/cache
KiB Swap: 33448956 total, 32064280 free,  1384676 used. 24056080 avail Mem

PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
5076 usera   20   0 20.297g 918992 209548 S 150.0  2.8 562:40.90 python
9179 usera   20   0 20.295g 909792 211000 S 125.0  2.8 882:40.18 python
11895 userb   20   0 20.295g 909740 207948 R 125.0  2.8 877:40.13 python
9861 userb   20   0 19.534g 898832 212784 R 118.8  2.7 546:57.85 python
BREAK
CONTAINER ID        IMAGE                  COMMAND                  CREATED             STATUS              PORTS               NAMES
c6aa8d92051f        my_img/my_img:0.1      "/usr/bin/tini -- ..."   5 minutes ago       Up 5 minutes                            aabe8a34-7170-41d1-9702-0f86c5557a86
d6aa8d92051f        my_img/my_img:0.2      "/usr/bin/tini -- ..."   3 minutes ago       Up 3 minutes                            dabe8a34-7170-41d1-9702-0f86c5557a86
"""
import csv
import re
from os.path import join, dirname, realpath

from pytop.top_parser import parse_top
from pytop.cmdline import call_ssh_script

THIS_FILE_DIR = dirname(realpath(__file__))
COMBINED_SCRIPT = join(THIS_FILE_DIR, 'combined.sh')

def combined_parser_ssh(*args, **kwargs):
    raw_txt = call_ssh_script(COMBINED_SCRIPT, *args, **kwargs)
    return combined_parser(raw_txt)

def parse_docker(raw_txt):
    headers = ['CONTAINER ID', 'IMAGE', 'COMMAND', 'CREATED', 'STATUS', 'PORTS', 'NAMES']
    header_pos = []
    header_line = True
    data = []
    for line in raw_txt.split('\n'):
        if header_line:
            header_line = False
            # docker is always aligned - find char positions of headers
            header_pos = [line.find(header) for header in headers]
        else:
            # parse
            idxs = header_pos+[len(line)]
            line_data = [line[idxs[i]:idxs[i+1]].strip() for i in range(len(header_pos))]
            data.append({headers[i].lower():line_data[i] for i in range(len(headers))})
    return headers, data

def combined_parser(raw_txt):
    breaks = raw_txt.split('\nBREAK\n')
    gpu_proc_header, gpu_proc_data = parse_csv(breaks[0].strip(), divider=',')
    gpu_info_header, gpu_info_data = parse_csv(breaks[1].strip(), divider=',')
    top_data = parse_top(breaks[2].strip())
    docker_headers, docker_data = parse_docker(breaks[3].strip())


    # Match up GPU processes with CPU
    pid_to_user = {proc['PID'] : proc['USER'] for proc in top_data['processes']}

    gpu_proc_data2 = []
    for proc in gpu_proc_data:
        proc['user'] = pid_to_user.get(proc['pid'], 'N/A')
        gpu_proc_data2.append(proc)
    gpu_proc_data = gpu_proc_data2

    data = {
        'gpu': {'processes': list(gpu_proc_data), 'info': list(gpu_info_data)},
        'cpu': top_data,
        'docker': docker_data
    }
    return data


def parse_csv(raw_txt, divider=','):
    try:
        reader = csv.reader(raw_txt.split('\n'), delimiter=divider)
        header = next(reader)
        for i, heading in enumerate(header):
            header[i] = re.sub('\[.*\]','',heading).strip()
        rows = []
        def gen():
            for row in reader:
                yield {header[i]:row[i].strip() for i in range(len(header))}
        return header, gen()
    except:
        return [], []



if __name__ == "__main__":
    import pprint
    result = combined_parser(TEST)
    pprint.pprint(result)
