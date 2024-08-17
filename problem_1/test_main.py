import unittest
import csv
from main import read_spec_file, write_fixed_width_file, parse_fixed_width_file
from data_generator import generate_random_data

class TestFixedWidthParser(unittest.TestCase):

    def setUp(self):
        self.spec_file = 'spec.json'
        self.spec = read_spec_file(self.spec_file)
        self.fixed_width_file = 'test_readable_data.txt'
        self.output_csv_file = 'test_output.csv'

    def test_generate_and_parse_fixed_width_file(self):
        data = generate_random_data(self.spec, num_records=5)
        write_fixed_width_file(data, self.spec, self.fixed_width_file)
        
        parse_fixed_width_file(self.spec, self.fixed_width_file, self.output_csv_file)
        
        with open(self.output_csv_file, 'r', encoding=self.spec['DelimitedEncoding']) as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        # Check that the header and five rows of data are present
        self.assertEqual(len(rows), 6)  # 1 header + 5 records
        self.assertEqual(rows[0], self.spec['ColumnNames'])

if __name__ == '__main__':
    unittest.main()