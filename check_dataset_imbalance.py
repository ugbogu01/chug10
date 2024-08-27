def check_dataset_imbalance(labelData):
    """
    Checks for imbalance in the dataset based on the distribution of True and False labels.
    
    Parameters:
    labelData (pd.Series): A pandas Series containing True and False labels.

    Returns:
    None
    """
    # Get the counts of True and False labels
    counts = labelData.value_counts()

    # Extract True and False counts, defaulting to 0 if a label is absent
    true_count = counts.get(True, 0)
    false_count = counts.get(False, 0)
    total_count = true_count + false_count

    # Handle the case where there are no labels in the dataset
    if total_count == 0:
        print("Class label is empty")
        return
    
    # Calculate percentages
    true_percentage = (true_count / total_count) * 100
    false_percentage = 100 - true_percentage
    
    # Determine the majority and print the imbalance level
    majority_label = 'True' if true_percentage >= false_percentage else 'False'
    majority_percentage = max(true_percentage, false_percentage)
    minority_percentage = 100 - majority_percentage

    if majority_percentage == 50:
        print("Dataset is balanced.")
    elif 40 <= minority_percentage < 50:
        print(f"Mild Imbalance, Majority class is '{majority_label}'. No need for Balancing Class labels.")
    elif 20 <= minority_percentage < 40:
        print(f"Moderate Imbalance, Majority class is '{majority_label}'. Consider Balancing Class labels.")
    elif minority_percentage < 20:
        print(f"Extreme Imbalance, Majority class is '{majority_label}'. Balance Class labels.")

# Example usage:
# check_dataset_imbalance(pd.Series([True, True, False, True, False]))
# check_dataset_imbalance(y_labels)
