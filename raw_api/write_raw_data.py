import os
import json
import csv
from collections import defaultdict

aries_ids = defaultdict(dict)
for csvf in os.listdir('data'):
	with open(os.path.join('data', csvf)) as f:
		reader = csv.DictReader(f, dialect='excel')
		for row in reader:
			id = row['subject_aries_id']
			aries_ids[id].update(row)

with open('aries_raw_data.json', 'w') as f:
	json.dump(aries_ids, f)