#!/usr/bin/env python
# coding: utf-8

import requests
import os

# Get API key from environment variable
key = os.environ['CTPP_API_KEY']
header = {"x-api-key": key}

# Set base URL for API
server = "https://ctppdata.transportation.org/api"

# List all available datasets
endpoint = "/datasets"
response = requests.get(url=server+endpoint, headers=header)
print(response.text)

# List all groups for year 2016 matching keyword "means of transportation"
endpoint = "/groups"
payload = {"year": 2016, "keyword": 'means of transportation'}
response = requests.get(server+endpoint, headers=header, params=payload)
# Uncomment the next line if you want to see what the actual response looks like
#print(response.text)
output = response.json()
for group in output['data']:
    name = group["name"]
    desc = group["description"]
    print(f"{name}: {desc}")

# list all variables for group B302201: Workers by time leaving home and by means of transportation
endpoint = "/groups/B302201/variables"
payload = {"year": 2016}
response = requests.get(server+endpoint, headers=header, params=payload)
# Uncomment the next line if you want to see what the actual response looks like
#print(response.text)
output = response.json()
print(f'{output["total"]} variables returned')
# if output["total"]>100: # check if there are more columns than the default page size
#     payload["size"] = output["total"] # resize the page to include all variables
#     response = requests.get(server+endpoint, headers=header, params=payload)
#     output = response.json()
colnames = [] # a list to hold column names (for later)
for column in output["data"]:
    name = column["name"]
    desc = column["label"]
    if "_e" in name: # only report estimates
        print(f"{name}: {desc}")
        vname, suffix = name.split("_")
        colnames.append(desc)
numcols = len(colnames)
print(f"{numcols} items selected")

import pandas as pd # for table display
# get data with geography filter on California tracts
endpoint = "/data/2016"
payload = {"in": 'state:06', "for": 'tract', "d-in": 'state:06', "d-for": 'tract', "get": 'group(b302201)', "page": '1', "size": '100'}
response = requests.get(server+endpoint, headers=header, params=payload)
# Uncomment the next line if you want to see what the actual response looks like
# print(response.text)

output = response.json()
res = output["data"][0]["origin_name"]
pow = output["data"][0]["destination_name"]
geoid = output["data"][0]["geoid"]