import src.config as toolbus
import src.helper as helper
import src.db as db
from src.exceptions import NonExistantHost

def execute(message):
    print('loaded IP')
    param = helper.param_from_message(message)
    print(param)
    host_info = db.get_host(param['mac'])
    print(host_info)
    if host_info['empty'] == True:
        raise NonExistantHost('wrong stage for non-existing Host.')
    profile = prepare_template('netctl.profile', param['ifname'], host_info['ip'])
    db.update_stage(host_info)
    return helper.prepare_result(host_info, payload=profile)

def prepare_template(filename, ifname, ip):
    data = {}
    data['dns'] = "'" + "', '".join(toolbus.cluster['dns']) + "'"
    data['name'] = ifname
    data['gateway'] = toolbus.cluster['gateway']
    data['address'] = ip + '/' + toolbus.cluster['cidr']
    return helper.readfile(filename).format(**data)
