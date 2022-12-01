import ipaddress
import random
import src.config as toolbus
import src.helper as helper
import src.db as db
from src.exceptions import InvalidClusterRole

def execute(message):
    print('loaded bootstrap')
    param = helper.param_from_message(message)
    host_info = db.get_host(param['mac'])
    print(host_info)
    if host_info['empty'] == True:
        host_info = create_host(param)
    return helper.prepare_result(host_info)


def create_host(param):
    host = {}
    print('new host '+param['mac'])
    group_info = db.get_group(param['host'].replace('cluster', ''))
    if group_info is None:
        raise InvalidClusterRole("could not create host. No Roles matching hostname.")
    serial = int(group_info[3]) + 1  
    db.update_group(group_info[0], serial)
    net_ips = set([str(ip) for ip in ipaddress.IPv4Network(group_info[2])])
    used_ips = set(db.get_ips_from_group(group_info[0]))
    usable_ips = list(net_ips - used_ips)
    host['ip'] = random.choice(usable_ips)
    host['stage'] = 0
    host['uid'] = param['mac']
    host['hostname'] = toolbus.cluster['prefix'] + group_info[1] + '{:02}'.format(serial)
    host['group'] = group_info[0]
    host['empty'] = False
    db.new_host(host)
    return host
    