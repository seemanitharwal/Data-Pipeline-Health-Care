import pandas as pd
import pymongo
from io import StringIO

# MongoDB client connection
def get_mongo_client():
    return pymongo.MongoClient("mongodb://localhost:27017")

# Function to load CSV data into MongoDB
def load_csv_to_mongo(file_path, collection_name, db_name="kedro_db"): #DB NAME
    client = get_mongo_client()
    db = client[db_name]
    collection = db[collection_name]
    
    # Read the CSV file into DataFrame
    df = pd.read_csv(file_path)
    
    # Convert DataFrame to a list of dictionaries
    data_dict = df.to_dict("records")
    
    # Insert data into MongoDB
    collection.insert_many(data_dict)
    print(f"Inserted data from {file_path} into {collection_name} collection.")

# Function to load Parquet data into MongoDB
def load_parquet_to_mongo(file_path, collection_name, db_name="kedro_db"):
    client = get_mongo_client()
    db = client[db_name]
    collection = db[collection_name]
    
    # Read the Parquet file into DataFrame
    df = pd.read_parquet(file_path)
    
    # Convert DataFrame to a list of dictionaries
    data_dict = df.to_dict("records")
    
    # Insert data into MongoDB
    collection.insert_many(data_dict)
    print(f"Inserted data from {file_path} into {collection_name} collection.")

# Function to load Excel data into MongoDB
def load_excel_to_mongo(file_path, sheet_name, collection_name, db_name="kedro_db"):
    client = get_mongo_client()
    db = client[db_name]
    collection = db[collection_name]
    
    # Read the Excel file into DataFrame
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Convert DataFrame to a list of dictionaries
    data_dict = df.to_dict("records")
    
    # Insert data into MongoDB
    collection.insert_many(data_dict)
    print(f"Inserted data from {file_path} (sheet {sheet_name}) into {collection_name} collection.")
