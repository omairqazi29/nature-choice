import random

from pymongo import MongoClient
import csv
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
        esg_score = random.randint(0, 100)
        add_entry_to_collection(name, esg_score)
        return esg_score


     
#csv_file = '/home/aaryan/Desktop/nature-choice/ESG Data With Company Performance.csv'
#
## Open the CSV file for reading
#with open(csv_file, 'r') as file:
#    # Create a CSV reader object
#    csv_reader = csv.reader(file)
#    
#    # Read the headers
#    headers = next(csv_reader)
#    
#    # Initialize a list to store the values from the first and third columns
#    values_list = []
#    
#    # Loop through the rows in the CSV file
#    for row in csv_reader:
#        first_column_value = row[0]  # Value from the first column (0-based index)
#        third_column_value = row[4]  # Value from the third column (0-based index)
#        
#        # Append the values to the list
#        values_list.append((first_column_value, third_column_value))
#
## Print the extracted values
#for values in values_list:
#    if values[0] is '' or values[1] is '':
#        continue
#
#    esg_score = int(values[1])
#
#    if random.randint(1, 2) == 1:
#        esg_score = min(100, esg_score + random.randint(1,5))
#    else:
#        esg_score = max(0, esg_score - random.randint(1,5))
#
#    if esg_score == 0:
#        continue
#
#
#    add_entry_to_collection(values[0], esg_score)
