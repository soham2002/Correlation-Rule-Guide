import os
import yaml

def extract_names_from_yaml(directory, output_file):
    names = []

    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.yaml') or filename.endswith('.yml'):
            file_path = os.path.join(directory, filename)
            try:
                # Open and parse the YAML file
                with open(file_path, 'r') as file:
                    data = yaml.safe_load(file)

                    # Check if 'name' exists in the YAML data
                    if 'name' in data:
                        names.append(data['name'])

            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    # Write the names to the output file
    with open(output_file, 'w') as output:
        for name in names:
            output.write(name + '\n')

    print(f"Extracted names have been written to {output_file}")

# Usage example
directory = "F:/Vehere/RulesList-1.7.1"
output_file = "extracted_names.txt" 
extract_names_from_yaml(directory, output_file)
