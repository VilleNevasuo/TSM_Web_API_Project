import requests
import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import datetime
import certifi
ca = certifi.where()

load_dotenv()

client = MongoClient(
    "mongodb+srv://wildu55:"+os.environ["dbpassword"]+"@tsmtest.f0cnqjq.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
print(client.list_database_names())
db = client.test

ah = db.test1

personDocument = {
    "name": {"first": "Alan", "last": "Turing"},
    "birth": datetime.datetime(1912, 6, 23),
    "death": datetime.datetime(1954, 6, 7),
    "contribs": ["Turing machine", "Turing test", "Turingery"],
    "views": 1250000
}

result = ah.insert_one(personDocument)


# def authenticate():

#     url = 'https://auth.tradeskillmaster.com/oauth2/token'

#     myobj = {
#         "client_id": "c260f00d-1071-409a-992f-dda2e5498536",

#         "grant_type": "api_token",

#         "scope": "app:realm-api app:pricing-api",

#         "token": os.environ["token"]
#     }

#     x = requests.post(url, json=myobj)
#     access_data = json.loads(x.text)

#     return access_data["access_token"]


# def query(url, access_token):

#     x = requests.get(url, headers={
#         'Authorization': f'Bearer {access_token}'})

#     return json.loads(x.text)


# def main():

#     realm_url = 'https://realm-api.tradeskillmaster.com/realms-by-name/EU-Thekal'
#     ah_url = 'https://realm-api.tradeskillmaster.com/auction-houses/468'
#     item_url = 'https://pricing-api.tradeskillmaster.com/ah/468'

#     access_token = authenticate()

#     realm_data = query(realm_url, access_token)
#     ah_data = query(ah_url, access_token)
#     item_data = query(item_url, access_token)

#     thekal_id = realm_data["realmId"]
#     region_id = ah_data["region"]["regionId"]

#     for el in realm_data["auctionHouses"]:
#         if el["type"] == "Horde":
#             ah_id = el["auctionHouseId"]

#     print(item_data[1])
#     print(item_data[2])


# main()
