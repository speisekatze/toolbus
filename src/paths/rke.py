import src.config as toolbus
import src.helper as helper
import src.db as db


def execute(message):
    print('loaded rke')
    host_info = helper.prepare_request(message)
    group = db.get_group(id=host_info['group'])
    host_info['stage'] = 4
    db.update_stage(host_info)
    return helper.prepare_result(host_info, 4, payload=toolbus.cluster['rke'][group[1]], options={})

