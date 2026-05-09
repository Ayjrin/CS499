# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, username: str = 'aacuser', password: str = 'shmeep'): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        USER = username
        PASS = password
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 

    # Create a method to return the next available record number for use in the create method

    def get_next_record_number(self):
        try:
            last_record = self.collection.find_one(sort=[("rec_num", - 1)])
            if last_record:
                return last_record["rec_num"] + 1
            else:
                return 1
        except Exception as e:
            print(f"error in get_next_record_number: {e}")
    
    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        if data is not None and isinstance(data, dict):
            data["record_number"] = self.get_next_record_number()
            result = self.database.animals.insert_one(data)  # data should be dictionary
            return True if result.inserted_id else False
        else: 
            raise Exception("Nothing to save, because data parameter is empty or data is not a dict") 
        

    # Create method to implement the R in CRUD.    
    def read(self, query):
        if query is not None and isinstance(query, dict):
            try:
                results = list(self.collection.find(query))
                return results
            except Exception as e:
                print(f"query failed: {e}")
                return []
        else:
            raise Exception("query cannot be None -- must be valid dictionary")
    
    # Update method to implement the U in CRUD.
    def update(self, query, update_data):
        if query is not None and isinstance(query, dict):
            if update_data is not None and isinstance(update_data, dict):
                try:
                    result = self.collection.update_many(query, update_data)
                    return result.modified_count
                except Exception as e:
                    print(f"Update failed: {e}")
                    return 0
            else:
                raise Exception("Update data cannot be None and must be a valid dictionary")
        else:
            raise Exception("Query cannot be None and must be a valid dictionary")
    
    # Delete method to implement the D in CRUD.
    def delete(self, query):
        if query is not None and isinstance(query, dict):
            try:
                result = self.collection.delete_many(query)
                return result.deleted_count
            except Exception as e:
                print(f"Delete failed: {e}")
                return 0
        else:
            raise Exception("Query cannot be None and must be a valid dictionary")