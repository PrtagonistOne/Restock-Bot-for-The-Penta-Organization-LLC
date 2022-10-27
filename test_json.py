import json

with open('cookies/lowes.json', 'r') as f:
    data = json.load(f)


print(data)
for key, val in enumerate(data):
    val['domain'] = '.lowes.com'
    print(key, val)
