#
# Author: Colin Hare
#

''' Description: makes continuous calls to the googlemaps API,
    Retrieving the duration of travel.
    Should the duration drop below a desired value, alerts the user with music
    Uses whatever builtin audio playing system is available'''

import googlemaps
import datetime
import time
import os

api_key = "" #Created when signing up for API usage: https://pypi.org/project/googlemaps/#description
gmaps = googlemaps.Client(api_key)
origin = ['Chatsworth High School, Chatsworth, California']
destination = ['Tokyo Table, Irvine, California']
numberCalls = 0
goodToDrive = False

'''Returns results if user were to depart right now
    a: index for origin list. b: index for destination list'''
def leaveRightNow(a,b): 
    global numberCalls
    numberCalls+=1
    return gmaps.distance_matrix(origins=origin[a],destinations=destination[b],
                           mode='driving',avoid='tolls',units='imperial',
                            departure_time=datetime.datetime.now(),traffic_model='best_guess')

def startChecking():
    desiredTime = 5400 #desired drive duration, in seconds
    call_interval = 900 #time in between each API call, in seconds
    print('Time right now: {}\nTime in between each call: {} minutes\n'.format(
        datetime.datetime.now(), call_interval/60))
    while True:
        travelResults = leaveRightNow(0,0) #print(travelResults['rows'][0]['elements'])
        print('{}\n'.format(travelResults['rows'][0]['elements'][0]['duration_in_traffic']['text']))
        travelTime = travelResults['rows'][0]['elements'][0]['duration_in_traffic']['value'] #in seconds
        if travelTime<=desiredTime:
            goodToDrive = True
            break
        if numberCalls == 20: #prevents from running endlessly, assuming duration never reaches desired time
            break
        time.sleep(call_interval) #places process in background for length of call_interval

    if goodToDrive==True:
        file = "Mossari-Le_Reve_Getty_remix.mp3"
        os.system(file) #plays audio file using system's native audio player
        print("Ready to drive. Number of calls: {}".format(numberCalls))
startChecking()
print('end')
