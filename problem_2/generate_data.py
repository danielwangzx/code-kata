import csv
import os
import argparse
from faker import Faker

fake = Faker()

def create_large_csv(file_name, target_size_mb):
    fieldnames = ['first_name', 'last_name', 'address', 'birth_date']
    estimated_record_size = 105  # Average bytes per record
    num_records = (target_size_mb * 1024 * 1024) // estimated_record_size

    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for _ in range(num_records):
            writer.writerow({
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'address': fake.address().replace('\n', ', '),
                'birth_date': fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat()
            })
    print(f"Generated approximately {target_size_mb}MB of data in {file_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a large CSV file with random data.")
    parser.add_argument('--size', type=int, default=2000, help='Target size of the CSV file in MB')
    args = parser.parse_args()
    
    create_large_csv('sample_data.csv', args.size)
