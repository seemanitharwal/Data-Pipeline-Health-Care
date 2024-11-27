import pandas as pd

def merge_datasets(df1, df2, left_key, right_key, how='outer'):
    """
    Merges two datasets on specified primary keys.
    
    Parameters:
    - df1: First DataFrame
    - df2: Second DataFrame
    - left_key: The column name in df1 to use as the merge key
    - right_key: The column name in df2 to use as the merge key
    - how: The type of merge to perform (default is 'outer')
     
    Returns:
    - Merged DataFrame
    """
    
    # Merge the two datasets
    merged_data = pd.merge(df1, df2, left_on=left_key, right_on=right_key, how=how)
    
    return merged_data


def merge_data(patients, encounters, symptoms, medical_history, financial,gender):    
    """
    Merges all datasets into one DataFrame with a unique patient ID.
    
    Parameters:
    - patients: DataFrame containing patient details
    - gender: DataFrame containing patient gender information
    - financial: DataFrame containing patient financial data
    - encounters: DataFrame containing patient encounters data
    - symptoms: DataFrame containing patient symptoms data
    - medical_history: DataFrame containing patient medical history
    
    Returns:
    - Merged DataFrame with all information for each patient
    """
    # Drop 'gender' column from patients if it exists before merging 
    patients = patients.drop(columns=['gender'], errors='ignore')
    
    # Merge datasets step by step using the merge_datasets function
    merged_data = merge_datasets(patients, gender, left_key='patient_id', right_key='gender_id', how='outer')
    
    #RENAME GENDER TO SEX as TUVA Standards
    if 'gender' in merged_data.columns:
        merged_data = merged_data.rename(columns={'gender': 'sex'}) # standard TUVA
    
    # Fill missing patient_id with gender_id 
    merged_data['patient_id'] = merged_data['patient_id'].fillna(merged_data['gender_id'])
    
    merged_data = merged_data.drop(columns=['gender_id'], errors='ignore')
    
    # Merge with financial, encounters, symptoms, and medical history
    merged_data = merge_datasets(merged_data, financial, left_key='patient_id', right_key='conditions_patient', how='outer')
    
    merged_data['patient_id'] = merged_data['patient_id'].fillna(merged_data['conditions_patient'])
    
    merged_data = merge_datasets(merged_data, encounters, left_key='patient_id', right_key='patient', how='outer')
    
    merged_data['patient_id'] = merged_data['patient_id'].fillna(merged_data['patient'])
    
    merged_data = merge_datasets(merged_data, symptoms, left_key='patient_id', right_key='symptoms_patient', how='outer')
    
    merged_data['patient_id'] = merged_data['patient_id'].fillna(merged_data['symptoms_patient'])
    
    merged_data = merge_datasets(merged_data, medical_history, left_key='patient_id', right_key='medications_patient', how='outer')
    
    merged_data['patient_id'] = merged_data['patient_id'].fillna(merged_data['medications_patient'])
    
    merged_data['patient_id'] = merged_data['patient_id'].astype(str)  # Ensure patient_id is string
   
    # Drop the original patient columns after renaming to avoid duplication
    merged_data = merged_data.drop(columns=['patient','medications_patient','symptoms_patient','conditions_patient','id'], errors='ignore')
    
    # Save only the 'patient_id' column to a CSV file
    merged_data [['patient_id']].to_csv('patient_ids.csv', index=False)

    # Remove duplicates based on patient_id and keep the first occurrence
    merged_data = merged_data.drop_duplicates(subset=['patient_id'], keep='first')
    
    return merged_data
