import json

old = json.load(open('tri_datadictionary.json'))

new = []

for entry in old:
    entry['api'] = 'raw-' + entry['type']
    if 'choices' in entry:
        for choice in entry['choices']:
            choice['value'] = choice['value'].strip()
    new.append(entry)

with open('aries_config.json', 'w') as f:
    json.dump(new, f)