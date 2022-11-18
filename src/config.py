import yaml

def load_yaml(config_file):
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

c = load_yaml("config/config.yaml")
server = c['toolbus']['server']
cluster = c['toolbus']['cluster']
db = c['toolbus']['db']