import src.config as toolbus
import src.helper as helper
import src.db as db


def execute(message):
    print('loaded Hostname')
    host_info = helper.prepare_request(message)
    host_info['stage'] = 2
    db.update_stage(host_info)
    options = {'hostname': host_info['hostname']}
    return helper.prepare_result(host_info, 3, options=options)

