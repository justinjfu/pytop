from collections import deque
#from pytop import parse_nvidia_ssh, parse_top_ssh
from pytop.combined import combined_parser_ssh
import time
from datetime import datetime

def clean_top_data(raw_data):
    procs = raw_data['processes']
    procs = filter(lambda x: x['USER'] != 'root', procs)
    procs_sorted = sorted(procs, key=lambda x: -float(x['%CPU']))

    top_procs = []
    for i, proc in enumerate(procs_sorted[:20]):
        cpu = float(proc['%CPU'])
        if cpu <= 10.0: 
            break
        top_procs.append({
            'user': proc['USER'],
            'cpu': cpu,
            'pid': int(proc['PID']),
            'cmd': proc['COMMAND'],
            'memory': float(proc['%MEM']),
        })

    return {
        'timestamp': raw_data['general']['time'],
        'processes': top_procs,
    }

def clean_nvidia_data(raw_data):
    num_gpu = int(raw_data['Attached GPUs'].strip())
    gpu_data_list = []
    for gpu_id in range(1, num_gpu+1):
        gpu_key = 'GPU 0000:%.2d:00.0' % gpu_id
        gpu_data = raw_data[gpu_key]
        usage = float(gpu_data['Utilization']['Gpu'][:-1].strip())/100.


        gpu_data = {
            'name': 'GPU %.2d' % gpu_id,
            'model': gpu_data['Product Name'],
            'temperature': gpu_data['Temperature']['GPU Current Temp'],
            'usage': usage,
            'memory_total': gpu_data['FB Memory Usage']['Total'],
            'memory_used': gpu_data['FB Memory Usage']['Used'],
        }
        gpu_data_list.append(gpu_data)


    clean_data = {
        'timestamp': raw_data['Timestamp'],
        'gpu': gpu_data_list,
    }
    return clean_data

def clean_combined_data(raw_data):
    timestamp = str(datetime.now())
    clean_cpu = clean_top_data(raw_data['cpu'])
    clean_cpu['timestamp'] = timestamp


    gpu_data_list = []
    for gpu_info in raw_data['gpu']['info']:
        gpu_id = int(gpu_info['pci.bus_id'].split(':')[1])
        usage = float(gpu_info['utilization.gpu'][:-1].strip())/100.
        gpu_data = {
            'name': 'GPU %.2d' % gpu_id,
            'model': gpu_info['name'],
            'temperature': int(gpu_info['temperature.gpu']),
            'usage': usage,
            'memory_total': gpu_info['memory.total'],
            'memory_used': gpu_info['memory.used'],
        }
        gpu_data_list.append(gpu_data)

    for gpu_proc in raw_data['gpu']['processes']:
        gpu_id = int(gpu_proc['gpu_bus_id'].split(':')[1])
        gpu_proc['gpu_id'] = gpu_id
        del gpu_proc['gpu_bus_id']

    clean_gpu = {
        'gpu': gpu_data_list,
        'processes': raw_data['gpu']['processes'],
        'timestamp': timestamp
    }

    clean_data = {
        'cpu': clean_cpu,
        'gpu': clean_gpu,
    }
    return clean_data

class MachineData(object):
    def __init__(self, hosts, ssh_user, identities, history=10, update_interval=60):
        self.__hosts = hosts
        self.__user = ssh_user
        self.__identities = identities
        self.history = history
        self.machine_to_data = {}
        self.machine_to_ts = {}
        self.update_interval = update_interval

    @property
    def hosts(self):
        return self.__hosts

    def query(self, machine_id):
        idx = self.__hosts.index(machine_id)
        cur_time = time.time()
        if cur_time - self.machine_to_ts.get(machine_id, 0)  > self.update_interval:
            res = clean_combined_data(combined_parser_ssh(user=self.__user, hostname=self.__hosts[idx], identity_file=self.__identities[idx], verbose=True, timeout=5))
            self.machine_to_data[machine_id] = res
            self.machine_to_ts[machine_id] = cur_time
        return self.machine_to_data.get(machine_id, {'cpu': 'Error', 'gpu': 'Error'})

    def query_top(self, machine_id):
        return self.query(machine_id)['cpu']

    def query_nvidia(self, machine_id):
        return self.query(machine_id)['gpu']


class MachineDataOld(object):
    def __init__(self, hosts, ssh_user, identities, history=10, update_interval=60):
        self.__hosts = hosts
        self.__user = ssh_user
        self.__identities = identities
        self.history = history
        self.machine_to_data_top = {}
        self.machine_to_data_nv = {}
        self.machine_to_ts_top = {}
        self.machine_to_ts_nv = {}
        self.update_interval = update_interval

    @property
    def hosts(self):
        return self.__hosts

    def query_top(self, machine_id):
        idx = self.__hosts.index(machine_id)
        cur_time = time.time()
        if cur_time - self.machine_to_ts_top.get(machine_id, 0)  > self.update_interval:
            res = clean_top_data(parse_top_ssh(user=self.__user, hostname=self.__hosts[idx], identity_file=self.__identities[idx], verbose=True, timeout=10))
            self.machine_to_data_top[machine_id] = res
            self.machine_to_ts_top[machine_id] = cur_time
        return self.machine_to_data_top.get(machine_id, {})

    def query_nvidia(self, machine_id):
        idx = self.__hosts.index(machine_id)
        cur_time = time.time()
        if cur_time - self.machine_to_ts_nv.get(machine_id, 0)  > self.update_interval:
            res = clean_nvidia_data(parse_nvidia_ssh(user=self.__user, hostname=self.__hosts[idx], identity_file=self.__identities[idx], verbose=True, timeout=10))
            self.machine_to_data_nv[machine_id] = res
            self.machine_to_ts_nv[machine_id] = cur_time
        return self.machine_to_data_nv.get(machine_id, {})
