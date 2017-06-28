
EXAMPLE_INPUT = """
==============NVSMI LOG==============

Timestamp                           : Wed Jun 21 13:30:09 2017
Driver Version                      : 375.39

Attached GPUs                       : 2
GPU 0000:01:00.0
    Product Name                    : TITAN X (Pascal)
    Product Brand                   : GeForce
    Display Mode                    : Enabled
    Display Active                  : Enabled
    Persistence Mode                : Disabled
    Accounting Mode                 : Disabled
    Accounting Mode Buffer Size     : 1920
    Driver Model
        Current                     : N/A
        Pending                     : N/A

GPU 0000:02:00.0
    Product Name                    : TITAN X (Pascal)

"""

CMD = 'nvidia-smi -q'

def deep_set(_dict, keys, value):
    if len(keys) == 0:
        raise ValueError("Keys must be a list with len > 0")
    if len(keys) == 1:
        _dict[keys[0]] = value
    else:
        _dict[keys[0]] = deep_set(_dict.get(keys[0], {}), keys[1:], value)
    return _dict

def parse_nvidia(raw_txt):
    """
    >>> result = parse_nvidia(EXAMPLE_INPUT)
    >>> result['Driver Version']
    '375.39'
    >>> result['GPU 0000:01:00.0']['Driver Model']
    {'Current': 'N/A', 'Pending': 'N/A'}
    """
    key_stack = []
    data = {}
    for line in raw_txt.split('\n'):
        if line.strip() == '':
            continue
        if 'NVSMI LOG' in line:
            continue
        if ': ' not in line:
            num_ws = len(line)-len(line.lstrip())  # amount of whitespace
            while len(key_stack)>0 and num_ws <= key_stack[-1]['ws']:
                key_stack.pop()
            key_stack.append({'ws': num_ws, 'k': line.strip()})
        else:
            k, v = [s.strip() for s in line.split(': ')]
            key_list = [s['k'] for s in key_stack]+[k]
            deep_set(data, key_list, v)
    return data

