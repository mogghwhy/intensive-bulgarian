import os
import glob
import configparser
from pathlib import Path
import polars as pl

# Initialize a ConfigParser object to read the configuration file
config = configparser.ConfigParser()
config.optionxform = str  # Preserve case sensitivity of option names
config.read('./config.ini')  # Read the configuration file

# Access the 'BASES' section from the config
bases = config['BASES']
keys = bases.keys()  # Get all keys in the 'BASES' section
meta = config['DATA']  # Access the 'DATA' section from the config
data_extension = meta.get('EXT')  # Get the data file extension from 'DATA'
input_data_extension= meta.get('INPUTEXT')

# Initialize lists to store base folders and lesson metadata
baseFolders = []
lesson_meta = []
new_column_names = []
cwd = os.getcwd()  # Get the current working directory

datalist = meta.get('DATALIST')
datalist_path = os.path.join(cwd, datalist)

# Collect base folder paths from the configuration
for key in keys:
    base = bases.get(key)  # Get each base folder path
    baseFolders.append(base)  # Append it to the list of base folders

# Get column names from the configuration (not used in this code)
columns = config['COLUMNS'].keys()
for col in columns:
    new_column_names.append(col)
new_column_names = new_column_names[:-1]
# Create full paths for each base folder in the current working directory
path_meta = [{'path': os.path.join(cwd, p), 'subpath': p } for p in baseFolders]

# Iterate over each path to find directories and their corresponding input files
for path_pair in path_meta:
    if os.path.exists(path_pair['path']) and os.path.isdir(path_pair['path']):  # Check if path exists and is a directory
        # Iterate over subdirectories within the current path
        for folder in [f.name for f in os.scandir(path_pair['path']) if f.is_dir()]:
            fp = os.path.join(path_pair['path'], folder)
            inp = os.path.join(fp, 'input')  # Define the input directory path            
            data_file = folder + data_extension  # Construct the data file name
            data_file_path = os.path.join(fp, data_file)  # Create full path for data file
            lesson_meta.append({'input': inp, 'outdata': data_file_path, 'subpath': os.path.join(path_pair['subpath'], folder, data_file)})  # Append metadata to list            

line_ending = '\n'
first=True
# Process each pair of input directory and output data file paths
for pair in lesson_meta:
    
    input_folder = pair["input"]
    if os.path.exists(input_folder) and os.path.isdir(input_folder):  # Check if input directory exists
        with os.scandir(input_folder) as entries:  # Scan entries in the input directory
            csv_files = [entry.path for entry in entries if entry.is_file() and entry.name.endswith(input_data_extension)]    
            # Filter for CSV files with the specified extension                
        # Load and concatenate CSV files into a single DataFrame if any CSV files found
        if len(csv_files) > 0:            
            lazy_frame = pl.scan_csv(csv_files, has_header=False, separator=";", new_columns=new_column_names)
            sorted_data = lazy_frame.sort(new_column_names[0]).collect()            
            # Write the combined DataFrame to a new CSV file        
            sorted_data.write_csv(pair['outdata'])  # Save the DataFrame to output file path specified in lesson_meta
            if first:
                first=False
                # Open the file in write mode to clear existing content
                with open(datalist_path, 'w') as file:
                    # Write initial line
                    file.write(pair['subpath'] + line_ending)
            else:
                with open(datalist_path, 'a') as file:
                    file.write(pair['subpath'] + line_ending)
