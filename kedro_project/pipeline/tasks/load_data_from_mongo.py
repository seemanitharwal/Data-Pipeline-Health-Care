import pymongo
import pandas as pd

# MongoDB client connection
def get_mongo_client():
    return pymongo.MongoClient("mongodb://localhost:27017") # CLIENT STRING MONGO DB

# Function to load data from MongoDB
def load_data_from_mongo(db_name="kedro_db"): # DB NAME
    client = get_mongo_client()
    db = client[db_name]
    
    # Define collections
    collections = ["patients", "encounters", "symptoms", "medications", "conditions","patient_gender"] # collections Names
    data_dict = {}
    
    # Load each collection and convert to a DataFrame
    for collection_name in collections:
        collection = db[collection_name]
        data = list(collection.find({}))  # Retrieve all documents
        df = pd.DataFrame(data)
        data_dict[collection_name] = df  # Add each DataFrame to the dictionary
    
    return data_dict


