import src.config as toolbus
from src.helper import get_script, get_host, get_next_stage, get_group, update_group

def execute(message):
    print('loaded config')
    param = {'mac': '', 'host': ''}
    if len(message) > 1:
        param = {k:v for (k,v) in [x.split('=') for x in message.split('&')]}
    print(param['mac'])
    print(param['host'])
    host_info = get_host(param['mac'])
    print(host_info)
    if host_info is None:
        stage = 0
    group_info = get_group(param['host'].replace('cluster', ''))
    print(group_info)
    serial = int(group_info[3]) + 1
    print(serial)
    new_hostname = toolbus.cluster['prefix'] + group_info[1] + '{:02}'.format(serial)
    update_group(group_info[0], serial)
    return 'OK'