import pandas as pd

# Function to structure patient data into Tuva Patient schema
def structure_patient_data(df):

    # Ensure unique IDs as string
    df['patient_id'] = df['patient_id'].astype(str)

    return df


def structure_symptoms(df):
    """
    This function takes a DataFrame and restructures the 'symptoms' column into separate columns 
    for each symptom with its corresponding value.
    
    Parameters:
    - df: DataFrame containing the 'symptoms' column with symptom names and their values
    
    Returns:
    - DataFrame with separate columns for each symptom, containing their respective values.
    """
    
    # Initialize an empty dictionary to hold the symptoms and their corresponding values
    symptom_dict = {'rash': [], 'joint_pain': [], 'fatigue': [], 'fever': []}
    
    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        # Split the symptoms string by ';' to get individual symptom-value pairs
        symptom_pairs = row['symptoms'].split(';')
        
        # Initialize a temporary dictionary to store the values for this row
        temp_symptoms = {'rash': None, 'joint_pain': None, 'fatigue': None, 'fever': None}
        
        # Process each symptom pair
        for pair in symptom_pairs:
            # Split each pair by ':' to separate the symptom name and its value
            symptom_name, symptom_value = pair.split(':')
            symptom_value = int(symptom_value.strip())  # Convert the value to an integer
            
            # Clean the symptom name and store it in the temporary dictionary
            symptom_name_clean = symptom_name.strip().lower().replace(" ", "_")  # Normalize name
            if symptom_name_clean in temp_symptoms:
                temp_symptoms[symptom_name_clean] = symptom_value
        
        # Append the processed symptom values to the corresponding list
        for key in symptom_dict.keys():
            symptom_dict[key].append(temp_symptoms[key])
    
    # Create new DataFrame from the symptom dictionary
    symptoms_df = pd.DataFrame(symptom_dict)
    
    # Concatenate the original DataFrame with the new symptoms DataFrame
    df = pd.concat([df, symptoms_df], axis=1)
    
    df = df.drop(columns=['symptoms'], errors='ignore')
    
    return df


