
import unittest
import os
import csv
import glob
from main_with_spark import anonymize_data_with_spark
from main import parallel_anonymize

class TestAnonymization(unittest.TestCase):

    def concatenate_pyspark_output(self, output_dir, output_file):
        """Concatenate PySpark part files into a single output CSV file."""
        part_files = glob.glob(os.path.join(output_dir, 'part-*'))
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for i, part_file in enumerate(sorted(part_files)):
                with open(part_file, 'r', encoding='utf-8') as infile:
                    if i == 0:
                        outfile.write(infile.read())  # Write header and data
                    else:
                        infile.readline()  # Skip the header
                        outfile.write(infile.read())  # Write only data

    def compare_files_in_chunks(self, original_file, anonymized_file, chunk_size=1000):
        with open(original_file, 'r', encoding='utf-8') as original, open(anonymized_file, 'r', encoding='utf-8') as anonymized:
            original_reader = csv.DictReader(original)
            anonymized_reader = csv.DictReader(anonymized)

            while True:
                original_chunk = [row for _, row in zip(range(chunk_size), original_reader)]
                anonymized_chunk = [row for _, row in zip(range(chunk_size), anonymized_reader)]

                if not original_chunk:
                    break  # End of file

                for orig_row, anon_row in zip(original_chunk, anonymized_chunk):
                    self.assertNotEqual(orig_row['first_name'], anon_row['first_name'])
                    self.assertNotEqual(orig_row['last_name'], anon_row['last_name'])
                    self.assertNotEqual(orig_row['address'], anon_row['address'])

    def test_anonymization_with_spark(self):
        input_file = 'sample_data.csv'
        output_dir = 'anonymized_data_spark_output'
        output_file = 'anonymized_data_spark_combined.csv'
        anonymize_data_with_spark(input_file, output_dir)
        self.concatenate_pyspark_output(output_dir, output_file)
        self.assertTrue(os.path.exists(output_file))

        self.compare_files_in_chunks(input_file, output_file)

    def test_anonymization_without_spark(self):
        input_file = 'sample_data.csv'
        output_file = 'anonymized_data.csv'
        parallel_anonymize(input_file, output_file)
        self.assertTrue(os.path.exists(output_file))

        self.compare_files_in_chunks(input_file, output_file)

if __name__ == '__main__':
    unittest.main()
