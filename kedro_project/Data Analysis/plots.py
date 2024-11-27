import pandas as pd
import matplotlib.pyplot as plt
import pymongo

# MongoDB client connection
def get_mongo_client():
    return pymongo.MongoClient("mongodb://localhost:27017") # CLIENT STRING MONGO DB

def load_data_from_mongo_collection(db_name="kedro_db", collection_name="medications"):
    client = get_mongo_client()
    db = client[db_name]
    collection = db[collection_name]
    data = list(collection.find({}))  # Retrieve all documents
    df = pd.DataFrame(data)
    
    return df
 
 
def plot_distinct_medications_over_time():
    # Convert to DataFrame
    df = load_data_from_mongo_collection()

    # Convert 'START' column to datetime
    df['START'] = pd.to_datetime(df['START'], errors='coerce')

    # Handle duplicates - let's drop duplicate medication descriptions
    df_cleaned = df.drop_duplicates(subset=['START', 'DESCRIPTION'])

    # Group by the 'START' date and count occurrences of each medication
    medication_counts = df_cleaned.groupby(['START', 'DESCRIPTION']).size().unstack(fill_value=0)

    # Plotting
    plt.figure(figsize=(12, 6))
    medication_counts.plot(kind='line', marker='o')
    plt.title('Distinct Medications Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Occurrences')
    plt.grid(True)
    plt.legend(title='Medication', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    plt.show()
    

def piechart_patient_racial_gender_percentage():

    # Load data
    df = load_data_from_mongo_collection(collection_name="master_data")
    
    # Group by 'race' and 'sex', count the occurrences for each combination
    grouped_data = df.groupby(['race', 'sex']).size().reset_index(name='counts')
    
    # Combine 'race' and 'sex' into a single label for each slice
    grouped_data['race_sex'] = grouped_data['race'] + ' - ' + grouped_data['sex']
    
    # Prepare labels and sizes for the pie chart
    labels = grouped_data['race_sex']
    sizes = grouped_data['counts']
    
    # Define a color palette to enhance the visual appeal
    colors = plt.cm.Paired(range(len(grouped_data)))  # Use the 'Paired' colormap
    
    # Create the pie chart
    fig, ax = plt.subplots(figsize=(10, 7))
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=labels, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=colors, 
        wedgeprops={'edgecolor': 'black', 'linewidth': 1.5},
        textprops={'color': 'black', 'fontsize': 12}
    )
    
    # Beautify the plot: Add title, style the text
    ax.set_title('Distribution of Patients by Race and Gender', fontsize=16, fontweight='bold')
    
    # Add a legend for clarity
    ax.legend(wedges, labels, title="Race and Gender", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=12)
    
    # Add a more professional look to the pie chart
    plt.setp(autotexts, size=10, weight="bold", color="white")
    plt.tight_layout()  # Adjust layout to prevent clipping
    
    # Display the plot
    plt.show()

def percentage_of_patients_with_all_symptoms_above_30():
    # Load the data (replace this with the actual loading function)
    df = load_data_from_mongo_collection(collection_name="master_data")

    # List of required columns
    required_columns = ['rash', 'joint_pain', 'fatigue', 'fever']
    
    # Ensure missing columns are added with a default value of 0
    for col in required_columns:
        if col not in df.columns:
            df[col] = 0  # Add the column with 0 values

    # Check if each symptom category is >= 30 for all four symptoms
    condition_met = (
        (df['rash'] >= 30) &
        (df['joint_pain'] >= 30) &
        (df['fatigue'] >= 30) &
        (df['fever'] >= 30)
    )
    
    # Count the total number of patients and those meeting the condition
    total_patients = len(df)
    patients_meeting_condition = condition_met.sum()
    
    # Calculate the percentage
    percentage = (patients_meeting_condition / total_patients) * 100
    print(f"Percentage of patients with all symptoms ≥ 30: {percentage:.2f}%")


    
# Run the main function
if __name__ == "__main__":
    #plot_distinct_medications_over_time()
    #piechart_patient_racial_gender_percentage()
    percentage_of_patients_with_all_symptoms_above_30()
    
