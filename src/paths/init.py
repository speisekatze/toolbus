import src.config as toolbus
from src.helper import get_script





def execute(_):
    print('loaded init')
    proto = toolbus.server['proto']
    port = toolbus.server['port']
    host = toolbus.server['host']
    script = get_script('init')
    script = script.replace('%%proto%%', str(proto))
    script = script.replace('%%port%%', str(port))
    script = script.replace('%%host%%', str(host))
    script = script.replace('%%stage%%', 'bootstrap')
    return script