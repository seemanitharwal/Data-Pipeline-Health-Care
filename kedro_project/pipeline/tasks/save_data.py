import pandas as pd
from pymongo import MongoClient

# Function to save data to MongoDB
def save_to_mongo(df, collection_name):
    if df.empty:
        print("Dataframe is empty. No data to insert into MongoDB.")
        return

    # Convert dataframe to a list of dictionaries
    records = df.to_dict("records")
    
    # Check if records is empty
    if not records:
        print("No records to insert. The dataframe might not have been properly converted.")
        return
    
    # MongoDB client
    client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI
    db = client['kedro_db']  # Replace with your database name
    collection = db[collection_name]
    
    # Insert records into MongoDB
    try:
        collection.insert_many(records)
        print(f"{len(records)} records inserted successfully into {collection_name}.")
    except Exception as e:
        print(f"An error occurred while inserting data: {e}")

