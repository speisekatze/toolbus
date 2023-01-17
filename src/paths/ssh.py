import src.config as toolbus
import src.helper as helper
import src.db as db


def execute(message):
    print('loaded ssh')
    host_info = helper.prepare_request(message)
    host_info['stage'] = 3
    db.update_stage(host_info)
    return helper.prepare_result(host_info, 4, payload=toolbus.cluster['users'], options={})

