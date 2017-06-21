import re

EXAMPLE_TOP = """
top - 17:58:00 up 7 days,  2:28,  1 user,  load average: 2.53, 2.29, 1.99
Tasks: 316 total,   2 running, 314 sleeping,   0 stopped,   0 zombie
%Cpu(s):  4.9 us,  0.9 sy,  0.5 ni, 93.6 id,  0.1 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem : 32857252 total, 12465496 free,  9152500 used, 11239256 buff/cache
KiB Swap: 16688124 total, 16688124 free,        0 used. 22538388 avail Mem 


  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
 4006 hello  20   0 29.636g 1.432g 346904 R 112.5  4.6 150:08.37 python
 2506 hello  20   0 1507088 367224 121832 S   6.2  1.1  97:40.55 chrome
 2704 hello  20   0  782928  74936  53588 S   6.2  0.2   7:30.90 chrome
 3570 hello  20   0  655028  52360  28328 S   6.2  0.2  36:35.43 gnome-terminal-
20227 hello  20   0 1381860 274352  81544 S   6.2  0.8   0:20.88 chrome
20823 hello  20   0   41960   3760   3200 R   6.2  0.0   0:00.01 top
    1 root      20   0  185464   6036   3916 S   0.0  0.0   0:08.79 systemd
    2 root      20   0       0      0      0 S   0.0  0.0   0:00.13 kthreadd

"""

TOP_REGEX = re.compile(r'top\s*-?\s+(?P<time>[0-9: ]+)\s+up\s+(?P<uptime>.+),\s+(?P<users>[0-9]+) users?,\s+load average: (?P<load1>[0-9.]+), (?P<load2>[0-9.]+), (?P<load3>[0-9.]+)')
TASKS_REGEX = re.compile(r'Tasks:\s+(?P<total>[0-9]+) total,\s+(?P<running>[0-9]+) running,\s+(?P<sleeping>[0-9]+) sleeping,\s+(?P<stopped>[0-9]+) stopped,\s+(?P<zombie>[0-9]+) zombie')
CPU_REGEX = re.compile(r'\%?Cpu\(s\):\s+(?P<us>[0-9.]+)\%?\s*us,\s+(?P<sy>[0-9.]+)\%?\s*sy,\s+(?P<ni>[0-9.]+)\%?\s*ni,\s+(?P<id>[0-9.]+)\%?\s*id,\s+(?P<wa>[0-9.]+)\%?\s*wa,\s+(?P<hi>[0-9.]+)\%?\s*hi,\s+(?P<si>[0-9.]+)\%?\s*si,\s+(?P<st>[0-9.]+)\%?\s*st')
MEM1_REGEX = 'a'
MEM2_REGEX = 'b'
START = 0
BLANK = 1
PROC_HEAD = 2
PROC_ENTRY = 3

PROCESSES = 'processes'
GENERAL = 'general'
TASKS = 'tasks'
CPU='cpu'

def parse_top(raw_txt):
    """
    Return a nested dictionary containing parsed output of the top command.

    Keys included are:
        general: time, uptime, users, load1, load2, load3
        tasks: total, running, sleeping, stopped, zombie
        cpu: us, sy, ni, id, wa, hi, si, st
        processes: A list of dictionaries containing PID, USER, PR, NI, VIRT, RES, SHR, S, %CPU, %MEM, TIME+, COMMAND


    >>> result = parse_top(EXAMPLE_TOP)
    >>> result[CPU]['us']
    4.9
    >>> len(result[PROCESSES])
    8
    """
    state = START
    data = {}
    headers = []
    for line in raw_txt.split('\n'):
        if state == START:
            result = TOP_REGEX.match(line)
            if result:
                data[GENERAL] = result.groupdict()
                state = TOP_REGEX
        elif state == TOP_REGEX:
            result = TASKS_REGEX.match(line)
            if result:
                subdata = {}
                data[TASKS] = result.groupdict()
                state = CPU_REGEX
        elif state == CPU_REGEX:
            result = CPU_REGEX.match(line)
            if result:
                data[CPU] = result.groupdict()
                state = MEM1_REGEX
        elif state == MEM1_REGEX:
            # not implemented
            state = MEM2_REGEX
        elif state == MEM2_REGEX:
            # not implemented
            state = PROC_HEAD
        elif state == PROC_HEAD:
            # not implemented
            if line.strip():
                state = PROC_ENTRY
                headers = line.split()
                data[PROCESSES] = []
        elif state == PROC_ENTRY:
            # not implemented
            state = PROC_ENTRY
            values = line.split()
            if values:
                data[PROCESSES].append({headers[i]: values[i] for i in range(len(headers))})
        else:
            raise NotImplementedError()
    return data
