import requests
import yaml

result = requests.get(f"https://raw.githubusercontent.com/jhnnsrs/segmentor/master/port.yaml")
print(result.content)

print(yaml.load(result.content))