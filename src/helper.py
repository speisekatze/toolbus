import os.path
import json
import src.config as toolbus
import src.db as db

def get_script(name):
    filename = f'scripts/{name}.toolbus'
    if not os.path.isfile(filename):
        return ''
    with open(filename, 'r') as f:
        lines = f.readlines()
    return "\n".join(lines)

def readfile(name):
    filename = f'scripts/{name}'
    if not os.path.isfile(filename):
        return ''
    with open(filename, 'r') as f:
        lines = f.readlines()
    return "\n".join(lines)

def new_stage_link(newstage):
    proto = toolbus.server['proto']
    port = toolbus.server['port']
    host = toolbus.server['host']
    return f'{proto}://{host}:{port}/{newstage}?mac={{mac}}&host={{hostname}}&ifname={{ifname}}'

def prepare_result(host, payload=''):
    newstage = db.get_next_stage(host['stage'])
    host['stage'] = newstage[2]
    data = {}
    data['url'] = new_stage_link(newstage[1])
    data['payload'] = ''
    return json.dumps(data)

def param_from_message(message):
    param = {'mac': '', 'host': ''}
    if len(message) > 1:
        param = {k:v for (k,v) in [x.split('=') for x in message.split('&')]}
    return param