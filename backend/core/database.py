import pymongo

def factory(uri: str, db_name: str):
    """
    Creates a MongoDB database client.
    """
    return pymongo.MongoClient(uri)[db_name]
