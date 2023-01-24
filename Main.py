import requests
import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import datetime
import certifi
ca = certifi.where()

load_dotenv()


def insert_database(items):

    client = pymongo.MongoClient("mongodb+srv://"
                                 + os.environ["dbusername"]
                                 + ":"+os.environ["dbpassword"]
                                 + "@ahdatatest.7cfmuia.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
    database = client["AHdatabase"]

    minBuytoutCol = database["minBuyout"]
    quantityCol = database["quantity"]
    marketValuesCol = database["marketValue"]
    historicalCol = database["historical"]
    numAuctionsCol = database["numAuctions"]

    minBuyouts = []
    quantities = []
    marketValues = []
    historicals = []
    numAuctions = []

    for item in items:
        minBuyouts.append({
            "itemId": item["itemId"],
            "Date": datetime.datetime.utcnow(),
            "value": item["minBuyout"]
        })
        quantities.append({
            "itemId": item["itemId"],
            "Date": datetime.datetime.utcnow(),
            "value": item["quantity"]
        })
        marketValues.append({
            "itemId": item["itemId"],
            "Date": datetime.datetime.utcnow(),
            "value": item["marketValue"]
        })
        historicals.append({
            "itemId": item["itemId"],
            "Date": datetime.datetime.utcnow(),
            "value": item["historical"]
        })
        numAuctions.append({
            "itemId": item["itemId"],
            "Date": datetime.datetime.utcnow(),
            "value": item["numAuctions"]
        })

    minBuytoutCol.insert_many(minBuyouts)
    quantityCol.insert_many(quantities)
    marketValuesCol.insert_many(marketValues)
    historicalCol.insert_many(historicals)
    numAuctionsCol.insert_many(numAuctions)


def authenticate():

    url = 'https://auth.tradeskillmaster.com/oauth2/token'

    myobj = {
        "client_id": "c260f00d-1071-409a-992f-dda2e5498536",

        "grant_type": "api_token",

        "scope": "app:realm-api app:pricing-api",

        "token": os.environ["token"]
    }

    x = requests.post(url, json=myobj)
    access_data = json.loads(x.text)

    return access_data["access_token"]


def query(url, access_token):

    x = requests.get(url, headers={
        'Authorization': f'Bearer {access_token}'})

    return json.loads(x.text)


def main():

    realm_url = 'https://realm-api.tradeskillmaster.com/realms-by-name/EU-Thekal'
    ah_url = 'https://realm-api.tradeskillmaster.com/auction-houses/468'
    item_url = 'https://pricing-api.tradeskillmaster.com/ah/468'

    access_token = authenticate()

    realm_data = query(realm_url, access_token)
    ah_data = query(ah_url, access_token)
    item_data = query(item_url, access_token)

    print(type(item_data))
    print(len(item_data))

    thekal_id = realm_data["realmId"]
    region_id = ah_data["region"]["regionId"]

    print("thekal id", thekal_id)
    print("region id", region_id)

    for el in realm_data["auctionHouses"]:
        if el["type"] == "Horde":
            ah_id = el["auctionHouseId"]

    # for line in item_data:
    #     if line["minBuyout"] > 0:
    #         print(line["itemId"])

    insert_database(item_data)


main()
