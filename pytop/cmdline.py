import subprocess 
import pytop.nvidia_parser as nvidia_parser
import pytop.top_parser as top_parser

NVIDIA_CMD = 'nvidia-smi -q'
TOP_CMD = 'top -n 1 -b'

def call(cmd, verbose=False, dry=False, timeout=None):
    if dry or verbose:
        print('CMD:', cmd)
        val = None
    if not dry:
        val = subprocess.check_output(cmd, shell=True, timeout=timeout)
        val = val.decode('ascii')
    return val

def call_ssh(cmd, user, hostname='localhost', identity_file='~/.ssh/id_rsa', verbose=False, dry=False, timeout=None):
    ssh_cmd = 'ssh {user}@{host} -i {id} \'{cmd}\''.format(user=user, host=hostname, id=identity_file, cmd=cmd)
    return call(ssh_cmd, verbose=verbose, dry=dry, timeout=timeout)

def raw_nvidia_smi():
    return call(NVIDIA_CMD)

def raw_top():
    return call(TOP_CMD)

def raw_nvidia_smi_ssh(*args, **kwargs):
    return call_ssh(NVIDIA_CMD, *args, **kwargs)

def raw_top_ssh(*args, **kwargs):
    return call_ssh(TOP_CMD, *args, **kwargs)

def parse_nvidia_ssh(*args, **kwargs):
    raw_data = raw_nvidia_smi_ssh(*args, **kwargs)
    return nvidia_parser.parse_nvidia(raw_data)

def parse_top_ssh(*args, **kwargs):
    raw_data = raw_top_ssh(*args, **kwargs)
    result = top_parser.parse_top(raw_data)
    return result

