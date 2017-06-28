import subprocess 
import nvidia_parser
import top_parser

NVIDIA_CMD = 'nvidia-smi -q'
TOP_CMD = 'top -n 1 -b'

def call(cmd, verbose=False, dry=False):
    if dry or verbose:
        print(cmd)
    if not dry:
        val = subprocess.check_output(cmd, shell=True)
    return val

def call_ssh(cmd, user, hostname='localhost', identity_file='~/.ssh/id_rsa', verbose=False, dry=False):
    ssh_cmd = 'ssh {user}@{host} -i {id} \'{cmd}\''.format(user=user, host=hostname, id=identity_file, cmd=cmd)
    return call(cmd, verbose=verbose, dry=dry)

def raw_nvidia_smi():
    return call(NVIDIA_CMD)

def raw_top():
    return call(TOP_CMD)

def raw_nvidia_smi_ssh(*args, **kwargs):
    return call_ssh(NVIDIA_CMD, *args, **kwargs)

def raw_top_ssh(*args, **kwargs):
    return call_ssh(TOP_CMD, *args, **kwargs)

def parse_nvidia_ssh(*args, **kwargs):
    return nvidia_parser.parse_nvidia(raw_nvidia_smi_ssh(*args, **kwargs))

def parse_top_ssh(*args, **kwargs):
    return top_parser.parse_top(raw_top_ssh(*args, **kwargs))
