import os
import argparse
import csv
import statistics

parser = argparse.ArgumentParser()
parser.add_argument(
        "--root_dir", help="root directory where all folders containing bag files are present", default='/media/smartcart/Seagate Expansion Drive/lsvr_data/')

args = vars(parser.parse_args())
root_dir = args["root_dir"]
catalog_root = './Catalog'

def get_catalog_data(catalog_file_path):
	combined_catalog = []
	with open(catalog_file_path, 'r') as csvFile:
	    reader = csv.reader(csvFile)
	    for row in reader:
	        combined_catalog.append(row)
	csvFile.close()
	return combined_catalog

def get_stable_weight(barcode, data_path, folder):
	try:
		cat_folder_path = os.path.join(data_path, folder)
		bag_folders = sorted(os.listdir(cat_folder_path))
		bag_folders = [x for x in bag_folders if '-' in x]
		median_weight = None
		for f in bag_folders:
			bag_path = os.path.join(cat_folder_path, f)
			if barcode[1:-1].strip("'") in f:
				weight_path = os.path.join(bag_path, 'stable_weight.txt')
				with open(weight_path, 'r') as f:
					weight_list = f.readlines()
					weight_list = [int(x.strip('\n')) for x in weight_list]
					median_weight = statistics.median(weight_list)
	except Exception as e:
		print(e)
		print('Weight Not available')
		median_weight = None
	return median_weight

category_folders = sorted(os.listdir(root_dir))
category_folders = [x for x in category_folders if '.' not in x and 'category' in x]
catalog_files = sorted(os.listdir(catalog_root))

bad_barcodes = []
for catalog_file in catalog_files:
	catalog_file_path = os.path.join(catalog_root, catalog_file)
	category_folder = os.path.basename(os.path.normpath(catalog_file_path))
	category_folder = category_folder.replace('.csv','')
	print(category_folder)
	catalog_data = get_catalog_data(catalog_file_path)
	with open(catalog_file_path, 'w') as f:
		f.write(",".join(map(str, catalog_data[0])))
		for i, row in enumerate(catalog_data[1:]):
			barcode = row[3]
			weight = get_stable_weight(barcode, root_dir, category_folder)
			if weight is not None:
				catalog_data[1:][i][4] = int(weight)
			else:
				bad_barcodes.append(barcode)
			f.write('\n')
			f.write(",".join(map(str,catalog_data[1:][i])))

		