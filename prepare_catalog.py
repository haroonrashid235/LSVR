import os
import csv

catalog_file = 'product-catalog.csv'
labels_file = 'Labels/category_8.txt'
catalog_root = './Catalog'

# create catalog folder if it doesn't exist
os.makedirs(catalog_root, exist_ok=True)

with open(labels_file, 'r') as f:
	data = f.readlines()
	labels  = [x.strip('\n') for x in data]

combined_catalog = []
with open(catalog_file, 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        combined_catalog.append(row)
csvFile.close()

cat_label_file = labels_file.rsplit('/',1)[1]

catalog_file = os.path.join(catalog_root, cat_label_file.replace('.txt', '.csv'))

count = 0
found = []
with open(catalog_file, 'w') as f:
	f.write(",".join(map(str, combined_catalog[0])))
	for label in labels:
		for item in combined_catalog[1:]:
			if str(label) == str(item[3]):
				f.write('\n')
				f.write(",".join(map(str,item)))
				found.append(label)
				count += 1

print(set(labels) - set(found))
print(f'Found {len(set(found))}/{len((labels))} barcodes')
