
import json
import csv
import argparse
from data_generator import generate_random_data

def read_spec_file(spec_file):
    """Read and parse the spec.json file."""
    with open(spec_file, 'r', encoding='utf-8') as file:
        spec = json.load(file)
    return spec

def write_fixed_width_file(data, spec, output_file):
    """Write data to a fixed-width file using spec."""
    with open(output_file, 'w', encoding=spec['FixedWidthEncoding']) as file:
        for record in data:
            file.write(''.join(record) + '\n')

def parse_fixed_width_file(spec, input_file, output_file):
    """Parse fixed-width file to CSV format."""
    offsets = list(map(int, spec['Offsets']))
    column_names = spec['ColumnNames']
    fixed_width_encoding = spec['FixedWidthEncoding']
    delimited_encoding = spec['DelimitedEncoding']
    include_header = spec['IncludeHeader'].lower() == 'true'

    positions = []
    start = 0
    for offset in offsets:
        end = start + offset
        positions.append((start, end))
        start = end

    with open(input_file, 'r', encoding=fixed_width_encoding) as infile,          open(output_file, 'w', encoding=delimited_encoding, newline='') as outfile:
        
        writer = csv.writer(outfile)
        
        if include_header:
            writer.writerow(column_names)

        for line in infile:
            # Trim the parsed fields to remove extra spaces
            row = [line[start:end].strip() for start, end in positions]
            writer.writerow(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process fixed-width data and generate a CSV output.")
    parser.add_argument('--records', type=int, default=5, help="Number of records to generate (default: 5)")
    
    args = parser.parse_args()

    spec_file = 'spec.json'
    spec = read_spec_file(spec_file)

    # Generate random but readable data based on spec
    data = generate_random_data(spec, num_records=args.records)
    
    # Write the generated data to a fixed-width file in the output directory
    fixed_width_file = 'output/readable_data.txt'
    write_fixed_width_file(data, spec, fixed_width_file)
    
    # Parse the fixed-width file to CSV in the output directory
    output_csv_file = 'output/output.csv'
    parse_fixed_width_file(spec, fixed_width_file, output_csv_file)
    
    print(f"Generated {args.records} records.")
    print(f"Fixed-width file '{fixed_width_file}' generated and parsed to '{output_csv_file}'.")
