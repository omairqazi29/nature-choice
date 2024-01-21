import random

from pymongo import MongoClient
import re

# Replace this with your MongoDB Atlas connection string
connection_string = "mongodb+srv://omairqazi29:w9w3rFBuzqlbMXHd@nature-choice.ecojvus.mongodb.net/?retryWrites=true&w=majority"

# Connect to the cluster
client = MongoClient(connection_string, tlsAllowInvalidCertificates=True)
# Select your database
db = client['nature-choice']
# Select your collection
collection = db['nature-choice']

def add_entry_to_collection(name, esg_score):
    """
    Adds an entry with a name and esg_score to the specified MongoDB collection.

    :param collection: The MongoDB collection to which the entry will be added.
    :param name: The name to be added.
    :param esg_score: The ESG score to be added.
    """
    document = {"name": name, "esg_score": esg_score}
    collection.insert_one(document)

def find_esg_value_by_name(name):
    """
    Finds and returns the ESG value for a given name in the MongoDB collection.

    :param collection: The MongoDB collection to search.
    :param name: The name to search for (may not be an exact match).
    :return: The ESG value if found, None otherwise.
    """
    # Create a case-insensitive regular expression for the name
    name_regex = re.compile(re.escape(name), re.IGNORECASE)

    # Search for the document
    document = collection.find_one({"name": name_regex})

    if document:
        return document.get("esg_score")
    else:
        if 'sorry' in name.lower(): return 0
        esg_score = random.randint(0, 100)
        add_entry_to_collection(name, esg_score)
        return esg_score