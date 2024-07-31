# using the flowkit package
import flowkit as fk
import numpy as np
import pandas as pd
import os


# Pattern in the folder
file_patterns = ["TA76", "TA77", "TA78", "TA79", "TA80", "TA82", "TA83", "TA84",
                     "TA85", "TA86", "TA87", "TA88", "TA89"] 



# This returns a dataframe of the control files

def controlfiles(directory, file_patterns):
    
    # Initialize an empty list to store all control file paths
    control_files_total = []
    select_folder_pattern = []
    select_file_pattern = []
    all_files = os.listdir(directory)
    
    for pattern in file_patterns:
        # Select folders that match the current pattern
        matching_directories = [f for f in all_files if re.search(pattern, f)]
        select_folder_pattern.extend(matching_directories)
        newfolderpath = [os.path.join(directory, folder) for folder in select_folder_pattern]
        
        # Select files in the folders
        for folder in newfolderpath:
            if os.path.isdir(folder):  # Ensure it's a directory
                matching_file_pattern = [f for f in os.listdir(folder) if re.search(pattern, f)]
                select_file_pattern.extend(matching_file_pattern)
                
                # Create new file paths based on the pattern
                newfilepath = [os.path.join(folder, file) for file in matching_file_pattern]
                
                # List all .fcs files in the directory that match the pattern
                for path in newfilepath:
                    if os.path.isdir(path):
                        all_fcs_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.fcs')]
                        
                        # Further filter files that contain "STD" 
                        control_files = [f for f in all_fcs_files if 'STD' in f]
                        control_files_total.extend(control_files)
                        df = pd.DataFrame(control_files_total)
    
    return df
