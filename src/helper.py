import os.path
import json
import src.config as toolbus
import src.db as db
from src.exceptions import NonExistantHost

def get_script(name):
    filename = f'scripts/{name}.toolbus'
    if not os.path.isfile(filename):
        return ''
    with open(filename, 'r') as f:
        lines = f.readlines()
    return "\n".join(lines)

def readfile(name):
    filename = f'assets/{name}'
    if not os.path.isfile(filename):
        return ''
    with open(filename, 'r') as f:
        lines = f.readlines()
    return "".join(lines)

def get_stage_link(newstage):
    proto = toolbus.server['proto']
    port = toolbus.server['port']
    host = toolbus.server['host']
    return f'{proto}://{host}:{port}/{newstage}?mac={{mac}}&host={{hostname}}&ifname={{ifname}}'

def prepare_result(host, stage=None, payload='', options=''):
    if stage is None:
        # we came from bootstrap
        stage = host['stage']
    stage_info = db.get_stage(stage)
    oldstage_info = db.get_stage(host['stage'])
    data = {}
    data['url'] = get_stage_link(stage_info[1])
    data['payload'] = payload
    data['stage'] = oldstage_info[1]
    data['options'] = options
    
    return json.dumps(data)

def param_from_message(message):
    param = {'mac': '', 'host': '', 'ifname': ''}
    if len(message) > 1:
        param = {k:v for (k,v) in [x.split('=') for x in message.split('&')]}
    return param

def prepare_request(message):
    param = param_from_message(message)
    print(param)
    host_info = db.get_host(param['mac'])
    print(host_info)
    if host_info['empty'] == True:
        raise NonExistantHost('wrong stage for non-existing Host.')
    return host_info