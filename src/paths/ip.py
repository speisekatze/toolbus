import src.config as toolbus
import src.helper as helper
import src.db as db

def execute(message):
    print('loaded IP')
    host_info = prepare_request(message)
    profile = prepare_template('netctl.profile', param['ifname'], host_info['ip'])
    db.update_stage(host_info)
    options = {}
    options['netctl_profile'] = toolbus.cluster['prefix'] + 'internal'
    return helper.prepare_result(host_info, 2, payload=profile, options=options)

def prepare_template(filename, ifname, ip):
    data = {}
    data['dns'] = "'" + "', '".join(toolbus.cluster['dns']) + "'"
    data['name'] = ifname
    data['gateway'] = toolbus.cluster['gateway']
    data['address'] = ip + '/' + toolbus.cluster['cidr']
    return helper.readfile(filename).format(**data)
