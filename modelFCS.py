
import numpy as np
import pandas as pd
from random import sample
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_validate, RepeatedStratifiedKFold
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.pipeline import make_pipeline
from imblearn.ensemble import BalancedRandomForestClassifier
from sklearn.preprocessing import FunctionTransformer
import matplotlib.pyplot as plt
import flowkit as fk
import sys


class SelectCellPreprocess:

    # Constructor
    def __init__(self, fcsdata_path, target_path) -> None:
        self.fcsdata_path = fcsdata_path
        self.target_path = target_path
        self.fcsdata = None
        self.target = None
        self.downsample_idx = None

    # Function to extract sample data from .fcs file
    def get_fcs_data(self, fcsdata_path):
        try:
            sample = fk.Sample(fcsdata_path)
            df_fcs_events = sample.as_dataframe(source='raw')
            df_fcs_events.columns = df_fcs_events.columns.get_level_values('pnn')
            return df_fcs_events
        except Exception as e:
            print(f"Error processing {fcsdata_path}: {e}")
            return None
        
    # Load target CSV file
    def get_target(self, target_path):
        try:
            return pd.read_csv(target_path)
        except Exception as e:
            print(f"Error loading labels: {e}")
            return None

    # Load data method to load fcs and target data
    def load_data(self):
        if not self.fcsdata:
            self.fcsdata = self.get_fcs_data(self.fcsdata_path)
        if not self.target:
            self.target = self.get_target(self.target_path)

    # Downsample method
    def downsample(self, N: int):
        try:
            if N > len(self.target):
                raise ValueError("N cannot be larger than the total number of samples.")
            # Sample N random indices from the available cells
            self.downsample = sample(range(0, len(self.target)), N)
        except Exception as e:
            print(f"Error during downsampling: {e}")
            return None

    # Lymphocyte preprocessing
    def lymphocyte_preprocess_data(self, N):
        self.load_data()
        self.downsample(N)
        label = "Lymphocytes"
        # Check if the label exists in the target dataframe
        if label not in self.target.columns:
            raise KeyError(f"Label '{label}' not found in target data.")
        lymphocyte_features = self.fcsdata.iloc[self.downsample]
        lymphocyte_index = lymphocyte_features.index
        lymphocyte_target = self.target[label].iloc[lymphocyte_index]
        return lymphocyte_features, lymphocyte_target

    # Single cells preprocessing
    def single_cells_preprocess_data(self):
        self.load_data()
        label = "Lymphocytes"
        if label not in self.target.columns:
            raise KeyError(f"Label '{label}' not found in target data.")
       
        single_cells_target = self.target[self.target[label]]  
        single_cells_index = single_cells_target.index
        single_cells_features = self.fcsdata.loc[single_cells_index]
        return single_cells_features, single_cells_target

    # Live cells preprocessing
    def live_cells_preprocess_data(self):
        self.load_data()
        label = "Single Cells"
        if label not in self.target.columns:
            raise KeyError(f"Label '{label}' not found in target data.")
        
        live_cells_target = self.target[self.target[label]]  
        live_cells_index = live_cells_target.index
        live_cells_features = self.fcsdata.iloc[live_cells_index]
        return live_cells_features, live_cells_target


# Main execution function
def main():
    command = sys.argv[1:]

    fcsdata_path = command[0]  # 'path/to/fcsdata'
    target_path = command[1]   # 'path/to/target_csv'
   
    # Instantiate the class
    preprocessor = SelectCellPreprocess(fcsdata_path, target_path)
    
    # Select the lymphocytes
    try:
        x, y = preprocessor.lymphocyte_preprocess_data(N) 
        print(f"Lymphocyte data shape: {x.shape}")
        
        # Preprocess single cells data
        X_single_cell, y_single_cell = preprocessor.single_cells_preprocess_data()
        print(f"Single cell data shape: {X_single_cell.shape}")

        # Preprocess live cells data
        X_live_cell, y_live_cell = preprocessor.live_cells_preprocess_data()
        print(f"Live cell data shape: {X_live_cell.shape}")
    
    except Exception as e:
        print(f"An error occurred during preprocessing: {e}")


if __name__ == "__main__":
    main()



class MultiClass:

    # Constructor
    def __init__(self, target_path):
        self.target_path = target_path
        self.fcsdata = None
        self.target = None
    
    def load_data(self):
        
        if not self.fcsdata:
            self.fcsdata = self.get_fcs_data(self.fcsdata_path)
        if not self.target:
            self.target = self.get_target(self.target_path)

    def add_extra_target(self, )
        data = SelectCellPreprocess.load_data
        
        # Step 1: Subset the columns for 'Lymphocytes', 'Single Cells', 'Live'
        subset_df = data[['Lymphocytes', 'Single Cells', 'Live']]
        #convert the binary labels to int
        subset_df['Lymphocytes'] = subset_df['Lymphocytes'].astype(int)
        subset_df['Single Cells'] = subset_df['Single Cells'].astype(int)
        subset_df['Live'] = subset_df['Live'].astype(int)
        subset_df['new_class'] = subset_df.sum(axis=1)
        # Step 4: Define a function to classify based on the row sum
        def classify(row_sum):
            if row_sum == 0:
                return 'Non-Lymphocytes'
            elif row_sum == 1:
                return 'Non-Single Cells'
            elif row_sum == 2:
                return 'Dead'
            elif row_sum == 3:
                return 'Alive'

        # Apply the function to the 'new_class' column
        subset_df['classification'] = subset_df['new_class'].apply(classify)
        new_column = subset_df['classification']
        print(new_column.unique())
        return new_column
