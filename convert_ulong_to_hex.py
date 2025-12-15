#!/usr/bin/env python3
"""
Convert H3 IDs from unsigned long (decimal) to hexadecimal format
Usage: python3 convert_ulong_to_hex.py input.csv output.csv
"""

import sys

def convert_ulong_to_hex_csv(input_file, output_file):
    """
    Convert CSV with format: ulong_id,density
    to format: h3_hex_code,density
    """
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        # Write header
        f_out.write('h3code,density\n')

        line_count = 0
        for line in f_in:
            line = line.strip()
            if not line:
                continue

            try:
                parts = line.split(',')
                if len(parts) != 2:
                    print(f"Warning: Skipping invalid line: {line}")
                    continue

                ulong_id = int(parts[0])
                density = parts[1]

                # Convert to hexadecimal (remove '0x' prefix)
                h3_hex = hex(ulong_id)[2:]

                f_out.write(f'{h3_hex},{density}\n')
                line_count += 1

            except ValueError as e:
                print(f"Warning: Skipping line due to error: {line} - {e}")
                continue

        print(f"Successfully converted {line_count} records")
        print(f"Output written to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 convert_ulong_to_hex.py input.csv output.csv")
        print("Example: python3 convert_ulong_to_hex.py sample_points.csv sample-density.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_ulong_to_hex_csv(input_file, output_file)
