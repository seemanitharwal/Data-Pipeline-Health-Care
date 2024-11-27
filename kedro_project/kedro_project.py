from pipeline.tasks.load_data import load_csv_to_mongo, load_parquet_to_mongo, load_excel_to_mongo
from pipeline.tasks.load_data_from_mongo import load_data_from_mongo  # Import the corrected load function
from pipeline.tasks.clean_data import clean_data
from pipeline.tasks.structure_data import structure_patient_data,structure_symptoms
from pipeline.tasks.merge_data import merge_data
from pipeline.tasks.save_data import save_to_mongo

# Step 1: Load raw data into MongoDB (already implemented in the previous step)
def load_raw_data():
    #change file paths as per requirement
    load_csv_to_mongo('D:/DOWNLOADS/kedro_project/Data_Patient/patients.csv', 'patients')
    load_csv_to_mongo('D:/DOWNLOADS/kedro_project/Data_Patient/patient_gender.csv', 'patient_gender')
    load_parquet_to_mongo('D:/DOWNLOADS/kedro_project/Data_Patient/encounters.parquet', 'encounters')
    load_csv_to_mongo('D:/DOWNLOADS/kedro_project/Data_Patient/symptoms.csv', 'symptoms')
    load_csv_to_mongo('D:/DOWNLOADS/kedro_project/Data_Patient/medications.csv', 'medications')
    load_excel_to_mongo('D:/DOWNLOADS/kedro_project/Data_Patient/conditions.xlsx', 'Sheet1', 'conditions')

# Step 2: Load data from MongoDB
def load_data_from_mongo_step():
    data = load_data_from_mongo()
    return data

# Step 3: Clean and structure the data
def clean_and_structure_data(data):
    cleaned_data = {key: clean_data(df,key) for key, df in data.items()}
    
    # Specifically structure the symptoms and patients data
    structured_patients = structure_patient_data(cleaned_data['patients'])
    
    # BELOW STEPS CAN BE DONE AS PER REQUIREMENT
    structured_symptoms = structure_symptoms(cleaned_data['symptoms'])
    # structured_medications = structure_medications(cleaned_data['medications'])
    # structured_conditions = structure_conditions(cleaned_data['conditions'])
    # structured_encounters = structure_encounters(cleaned_data['encounters'])
    
    
    return cleaned_data, structured_patients,structured_symptoms

# Step 4: Merge all data
def merge_all_data(cleaned_data, structured_patients,structured_symptoms):
    merged_data = merge_data(structured_patients, cleaned_data['encounters'], structured_symptoms, cleaned_data['medications'], cleaned_data['conditions'],cleaned_data['patient_gender'])
    return merged_data

# Step 5: Save the final merged data
def save_final_data(merged_data):
    save_to_mongo(merged_data, "master_data")

# Main pipeline function
def run_pipeline():
    # Step 1: Load raw data into MongoDB
    load_raw_data()
    
    # Step 2: Load data from MongoDB
    data = load_data_from_mongo_step()
    
    # Step 3: Clean and structure data
    cleaned_data, structured_patients,structured_symptoms = clean_and_structure_data(data)
    
    # Step 4: Merge all data
    merged_data = merge_all_data(cleaned_data, structured_patients,structured_symptoms)
    
    # Step 5: Save final merged data
    save_final_data(merged_data)

    print("Pipeline executed successfully.")



# Execute the pipeline
if __name__ == "__main__":
    run_pipeline()

