import csv
import hashlib
import multiprocessing as mp
import os
import math
import shutil

PROTECTED_FIELDS = ['first_name', 'last_name', 'address']
FIELD_NAMES = ['first_name', 'last_name', 'address', 'birth_date']

def hash_value(value):
    return hashlib.sha1(value.encode('utf-8')).hexdigest()

def process_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile, fieldnames=FIELD_NAMES)
        writer = csv.DictWriter(outfile, fieldnames=FIELD_NAMES)
        writer.writeheader()
        next(reader)
        for row in reader:
            for field in PROTECTED_FIELDS:
                row[field] = hash_value(row[field])
            writer.writerow(row)

def split_csv(input_file, num_splits):
    file_size = os.path.getsize(input_file)
    split_size = file_size // num_splits
    with open(input_file, 'r', encoding='utf-8') as f:
        header = f.readline()
        lines = f.readlines()

    split_files = []
    for i in range(num_splits):
        split_file = f'split_{i}.csv'
        split_files.append(split_file)
        with open(split_file, 'w', encoding='utf-8') as sf:
            sf.write(header)
            sf.writelines(lines[i * split_size:(i + 1) * split_size])

    return split_files

def parallel_anonymize(input_file, output_file):
    cpu_count = mp.cpu_count()
    split_files = split_csv(input_file, cpu_count)
    pool = mp.Pool(cpu_count)
    pool.starmap(process_csv, [(file, f"{file}_anonymized.csv") for file in split_files])
    pool.close()
    pool.join()

    with open(output_file, 'w', encoding='utf-8') as f_out:
        for i, file in enumerate(split_files):
            with open(f"{file}_anonymized.csv", 'r', encoding='utf-8') as f_in:
                if i == 0:
                    shutil.copyfileobj(f_in, f_out)
                else:
                    f_in.readline()
                    shutil.copyfileobj(f_in, f_out)
            os.remove(file)
            os.remove(f"{file}_anonymized.csv")

if __name__ == "__main__":
    parallel_anonymize('sample_data.csv', 'anonymized_data.csv')
