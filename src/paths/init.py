import src.config as toolbus
from src.helper import get_script





def execute(message):
    print('loaded init')
    proto = toolbus.server['proto']
    port = toolbus.server['port']
    host = toolbus.server['host']
    return get_script('init').format(proto=proto, port=port, host=host, stage='config')