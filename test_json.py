import json

with open('cookies/home_depot.json', 'r') as f:
    data = json.load(f)

for key, val in enumerate(data):
    print(key, val)
