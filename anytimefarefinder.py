# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 19:04:32 2022

@author: samgo
"""
import requests
import pandas as pd
import csv

def get_anytime_fare(origin, destination, path):    
    anytime = -1
    # Todo implement railcard
    # todo think about whether multi-route implementation is correct. currently finds most expensive as it's probably the most permissable ticket.
    # Todo proper documentation.
    
    api_url = "https://gw.brfares.com/legacy_querysimple?orig=" + origin + "&dest=" + destination
    #railcard = "YNG"
    # to include railcards append + "&rlc=" + railcard to api_url.
    
    # First, check if fare is in existing file
    local_fares = load_fares(path)
    for n in range(len(local_fares)):
        if local_fares[n]['Origin'] == origin and local_fares[n]['Destination'] == destination:
            print("Found fare locally")
            return local_fares[n]['Fare']
        
    # No fare saved locally, continuing to make API request.
    # Load API Credentials
    f = open('credentials.txt', mode='r')
    user, pwrd = f.read().split(',')
    response = requests.get(api_url, auth=(user, pwrd))
    f.close()
    # Make API call
    print("Calling API")
    r = response.json()
    # Extracting the anytime fare.
    # if 'fares' not in r.keys():
    #     # No fares found?
    #     return -10000
    if 'error' in r.keys():
        raise Exception("Error occoured in API call - could the Quota have been exceeded?")
    
    
    for fare in r['fares']:
        #print("------------")
        #print(fare)
        if fare['ticket']['code'] != 'SDR' and fare['ticket']['code'] != 'SOR':
            continue
        #print(fare)
        if anytime < fare['adult']['fare'] or anytime == -1:
            # if anytime not yet found or found fare higher, make this the anytime fare.
            anytime = fare['adult']['fare']
        #break
    local_fares.append({'Origin':origin, 'Destination':destination,'Fare':anytime})
    save_fares(path, local_fares)
    return anytime

def save_fares(path, fares):
    with open(path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Origin", "Destination", "Fare"])
        writer.writeheader()
        writer.writerows(fares)

def load_fares(path):
    with open(path, 'r') as f:
        dict_reader = csv.DictReader(f)
        list_of_dict = list(dict_reader)
    return(list_of_dict)

#fares_local = [{'Origin':'CPM','Destination':'PAD','Fare':'19500'}]

#save_fares(save_fares_path, fares_local)
#loaded = load_fares(save_fares_path)

# save_fares_path = "saved_fares.csv"
#print(get_anytime_fare("CPM", "BRI", save_fares_path))

#target = 'PAD'
# station_list = pd.DataFrame(['CPM','BRI'], columns=['Code'])
# station_list['fares'] = -1


# for n in range(len(station_list)):
#     station_list['fares'][n]=get_anytime_fare(station_list['Code'][n],target, save_fares_path)



