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

# list all variables for group A102106: Means of transportation (18)
endpoint = "/groups/A102106/variables"
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
# get data with geography filter rutned on (Washington, DC)
endpoint = "/data/2016"
payload = {"in": 'state:11', "for": 'county:001', "get": 'group(A102106)'}
response = requests.get(server+endpoint, headers=header, params=payload)
# Uncomment the next line if you want to see what the actual response looks like
#print(response.text)
output = response.json()
location = output["data"][0]["name"]
geoid = output["data"][0]["geoid"]
estimates = numcols * [0]
MOEs = numcols * [0]
for variable in output["data"][0].keys():
    if variable in ["geoid","name"]:
        continue
    vname, suffix = variable.split("_")
    index = int(suffix[1:])-1
    if suffix[0] == "e":
        value = int(output["data"][0][variable].replace(",",""))
        # put the value in the estimates list
        estimates[index] = value
        if variable == "A102106_e1":
            total = value
    elif suffix[0] == "m":
        value = int(output["data"][0][variable][3:].replace(",",""))
        # extract numeric portion only and put it in the MOEs list
        MOEs[index] = value
df = pd.DataFrame(
    {
        "Variable": pd.Series(colnames),
        "MOE": pd.Series(MOEs, dtype="int32"),
        "Estimate": pd.Series(estimates, dtype="int32")
    }
)
df["Low"] = df.Estimate - df.MOE
df["High"] = df.Estimate + df.MOE
df["Est. %"] = round(100*df.Estimate / total,2)
df

