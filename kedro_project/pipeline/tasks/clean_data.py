
import pandas as pd
import re
import numpy as np

# Data Cleaning Function to align with Tuva Data Model
def clean_data(df,key):

    if key == 'patients':
        # Clean 'first' and 'last' columns to remove digits and special characters, strip spaces, and convert to lowercase
        df['FIRST'] = df['FIRST'].apply(lambda x: re.sub(r'[^a-zA-Z\s]', '', str(x)).strip().lower())
        df['LAST'] = df['LAST'].apply(lambda x: re.sub(r'[^a-zA-Z\s]', '', str(x)).strip().lower())
        
        if 'MAIDEN' in df.columns:
            # Apply cleaning only to non-null and non-empty values in the 'MAIDEN' column
            df['MAIDEN'] = df['MAIDEN'].apply(
                lambda x: re.sub(r'[^a-zA-Z\s]', '', str(x)).strip().lower() 
                if pd.notnull(x) and str(x).strip() != '' else x
            )
    
        # Clean the 'address' column to remove leading/trailing spaces
        df['ADDRESS'] = df['ADDRESS'].apply(lambda x: str(x).strip() if pd.notnull(x) else x)

         # Rename all columns by assigning name
        df = df.rename(columns={
            'BIRTHDATE': 'birth_date',
            'DEATHDATE': 'death_date',
            'MARITAL': 'marital_status',
            'BIRTHPLACE': 'birth_place',
            'COUNTY': 'country',
            'LAT': 'latitude',
            'LON': 'longitude',
            'ZIP': 'zip_code',
            'SSN': 'social_security_number',
            'FIRST': 'first_name',
            'LAST': 'last_name',       
        })
        
    elif key == 'conditions':

         # Rename all columns by assigning name
        df = df.rename(columns={
            'START': 'condition_start_date',
            'STOP': 'condition_end_date',
            'ENCOUNTER': 'conditions_encounter_id',
            'DESCRIPTION': 'conditions_description',
            'CODE': 'conditions_code',
            'PATIENT':'conditions_patient'
            
        })
    
    elif key == 'medications':

         # Rename all columns by assigning name
        df = df.rename(columns={
            'START': 'medication_start_date',
            'STOP': 'medication_end_date',
            'ENCOUNTER': 'medications_encounter_id',
            'DESCRIPTION': 'medication_description',
            'CODE': 'medication_code',
            'REASONCODE': 'reason_code',
            'PATIENT':'medications_patient',
            'PAYER':'medications_payer_id',
            'PAYER_COVERAGE':'medications_payer_coverage',
            'REASONDESCRIPTION':'medications_reason_description'
                       
        })
    
    elif key == "encounters":
         # Rename all columns by assigning name
        df = df.rename(columns={
            'START': 'encounter_start_date',
            'STOP': 'encounter_end_date',
            'ENCOUNTER': 'encounter_id',
            'DESCRIPTION': 'encounter_description',
            'CODE': 'encounter_code'
        })
    
    elif key == "symptoms":
         # Drop 'gender' column from patients if it exists before merging as an empty column
        df = df.drop(columns=['GENDER'], errors='ignore')
        
        # Rename all columns by assigning names
        df = df.rename(columns={
            'RACE': 'symptoms_race',
            'ETHNICITY': 'symptoms_ethnicity',
            'PATIENT':'symptoms_patient'
            
        })
    elif key == "patient_gender":
        
        # Rename all columns by assigning names
        df = df.rename(columns={
            'Id': 'gender_id'
        })        
    df = df.drop(columns=['_id'], errors='ignore')    
    # Renaming columns to lowercase with underscores (from uppercase)
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]    
    
    return df




# Some cleaning standards as per requirenment


# # 1. Fixing the Patients Table
# def fix_patients(patients_df):
#     # Handle missing 'age', 'gender', and 'name'
#     patients_df['age'] = patients_df['age'].fillna(patients_df['age'].median())  # Impute missing age with median
#     patients_df['gender'] = patients_df['gender'].fillna('Unknown')  # Impute missing gender with 'Unknown'
#     patients_df['name'] = patients_df['name'].fillna('Unknown')  # Impute missing name with 'Unknown'
    
#     # Remove duplicates based on 'patient_id' and 'name'
#     patients_df.drop_duplicates(subset=['patient_id', 'name'], keep='first', inplace=True)
    
#     # Standardize gender field to 'Male', 'Female', 'Other'
#     patients_df['gender'] = patients_df['gender'].apply(lambda x: x.capitalize() if x in ['male', 'female', 'other'] else 'Unknown')
    
#     # Check for unrealistic ages (age < 0 or > 120)
#     patients_df = patients_df[patients_df['age'] >= 0]
#     patients_df = patients_df[patients_df['age'] <= 120]
    
#     return patients_df

# # 2. Fixing the Encounters Table
# def fix_encounters(encounters_df):
#     # Remove duplicates based on 'encounter_id'
#     encounters_df.drop_duplicates(subset=['encounter_id'], keep='first', inplace=True)
    
#     # Ensure 'start_time' and 'end_time' are in datetime format
#     encounters_df['start_time'] = pd.to_datetime(encounters_df['start_time'], errors='coerce')
#     encounters_df['end_time'] = pd.to_datetime(encounters_df['end_time'], errors='coerce')
    
#     # Fix overlapping encounters by checking for 'end_time' earlier than 'start_time'
#     encounters_df = encounters_df[encounters_df['end_time'] > encounters_df['start_time']]
    
#     # Handle missing 'patient_id'
#     encounters_df = encounters_df.dropna(subset=['patient_id'])
    
#     return encounters_df

# # 3. Fixing the Symptoms Table
# def fix_symptoms(symptoms_df):
#     # Handle missing 'description' and 'severity'
#     symptoms_df['description'] = symptoms_df['description'].fillna('Unknown')
#     symptoms_df['severity'] = symptoms_df['severity'].fillna('Unknown')
    
#     # Standardize severity (e.g., 'Mild', 'Moderate', 'Severe')
#     symptoms_df['severity'] = symptoms_df['severity'].apply(lambda x: x.capitalize() if x in ['mild', 'moderate', 'severe'] else 'Unknown')
    
#     # Remove duplicate symptoms for the same patient
#     symptoms_df.drop_duplicates(subset=['patient_id', 'description'], keep='first', inplace=True)
    
#     return symptoms_df

# # 4. Fixing the Conditions Table
# def fix_conditions(conditions_df):
#     # Handle missing 'condition_code' and 'description'
#     conditions_df['condition_code'] = conditions_df['condition_code'].fillna('Unknown')
#     conditions_df['description'] = conditions_df['description'].fillna('Unknown')
    
#     # Standardize condition codes (e.g., use a proper medical coding system like ICD-10)
#     # Here we're just applying a placeholder fix; ideally, this should be mapped against a standard codebook
#     conditions_df['condition_code'] = conditions_df['condition_code'].apply(lambda x: x.strip().upper())
    
#     # Remove duplicates for the same patient and condition
#     conditions_df.drop_duplicates(subset=['patient_id', 'condition_code'], keep='first', inplace=True)
    
#     return conditions_df

# # 5. Fixing the Medications Table
# def fix_medications(medications_df):
#     # Handle missing 'medication_name' and 'dosage'
#     medications_df['medication_name'] = medications_df['medication_name'].fillna('Unknown Medication')
#     medications_df['dosage'] = medications_df['dosage'].fillna('Unknown Dosage')
    
#     # Standardize medication names (e.g., generic vs. brand names)
#     medications_df['medication_name'] = medications_df['medication_name'].apply(lambda x: x.strip().title())
    
#     # Standardize dosage (e.g., remove unexpected symbols or characters)
#     medications_df['dosage'] = medications_df['dosage'].apply(lambda x: str(x).replace('mg', ' mg').replace('ml', ' ml').strip())
    
#     # Ensure 'start_date' and 'end_date' are in datetime format
#     medications_df['start_date'] = pd.to_datetime(medications_df['start_date'], errors='coerce')
#     medications_df['end_date'] = pd.to_datetime(medications_df['end_date'], errors='coerce')
    
#     # Remove medications that have missing patient IDs
#     medications_df = medications_df.dropna(subset=['patient_id'])
    
#     # Fix overlapping prescriptions (if any)
#     medications_df = medications_df[medications_df['end_date'] > medications_df['start_date']]
    
#     return medications_df
