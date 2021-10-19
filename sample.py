import requests
import json

API_KEY = 'hKa5akD7RKqdCsmB'


'''
Get information on all robots available for the user
RESPONSE: [{"id": "robsimhaydryq9lfgphbn4", "name": "sim-test", "agentVersion": "3.24.0", "agentOnline": false, "updatedTs": 1634583464630 }]
'''
def get_robots():
    # GET /robots request
    url = 'https://api.inorbit.ai/robots'
    headers = {
      'Accept': 'application/json',
      'x-auth-inorbit-app-key': API_KEY
    }
    response = requests.request('GET', url, headers = headers) # get response from InOrbit API
    print(response)
    arrayofrobots = json.loads(response) # Convert JSON response to dictionary
    '''for loop to collect all IDS:
        pass'''
    return arrayofrobots['id']


'''
Get attribute details about a particular robot using its robotId
RESPONSE: { "id": "robsimhaydryq9lfgphbn4", "name": "sim-test", "agentVersion": "3.24.0", "agentOnline": true, "updatedTs": 1634603503255 }
'''
def get_robot(robotId):
    #GET /robots/robotId request
    url = 'https://api.inorbit.ai/robots/'+robotId
    headers = {
      'Accept': 'application/json',
      'x-auth-inorbit-app-key': API_KEY
    }
    response = requests.request('GET', url, headers = headers) # get response from InOrbit API
    print(response)
    robotattributes = json.loads(response) # Convert JSON response to dictionary
    if str(robotattributes['agentOnline']) == 'true':
        #agentOnline has possible values of true or false
        #IF the agent on the robot is online and the robot is able to communicate with InOrbit return True otherwise return False
        return True
    return False


'''
Get details of current map of the robot 
RESPONSE: { "robotId": "robsimhaydryq9lfgphbn4", "mapId": "map", "updatedTs": 1634571279270, "label": "map", "dataHash": "6051606626958011017",
    "height": 1066, "width": 719, "resolution": 0.019999999552965164, "x": -7.175000190734863, "y": -10.609999656677246 }
'''
def get_current_map(robotId):
    # GET /robots/robotId/maps/current request
    url = 'https://api.inorbit.ai/robots/'+robotId+'/maps/current'
    headers = {
        'Accept': 'application/json',
        'x-auth-inorbit-app-key': API_KEY
    }
    response = requests.request('GET', url, headers = headers) # get response from InOrbit API
    print(response)
    result = json.loads(response) # Convert JSON response to dictionary

    #Calculate the real world length and width size of the area represented by the map by using its pixel values and resolution
    mapresolution = result['resolution']
    maplength = result['height'] * mapresolution  # height in pixels * resolution
    mapwidth = result['width'] * mapresolution # width in pixels * resolution

    # return the values of mapId, resolution, width and height in real world size, origin x & y
    return result['mapId'], mapwidth, maplength, mapresolution, result['x'], result['y']


'''
Get the current position of the robot in the specified map
RESPONSE: { "mapId": "map", "mapDataHash": "6051606626958011017", "x": 1.747115135192871, "y": 8.967257499694824, "theta": -2.8662242889404297,
    "ts": 1634583459839, "xPixels": 446.10577626762785, "yPixels": 978.8628796978938 }
'''
def get_robot_pos(robotId, mapid):
    # GET /robots/robotId/localization/pose request
    url = 'https://api.inorbit.ai/robots/'+robotId+'/localization/pose'
    headers = {
        'Accept': 'application/json',
        'x-auth-inorbit-app-key': API_KEY
    }
    response = requests.request('GET', url, headers = headers) # get response from InOrbit API
    print(response)
    result = json.loads(response) # Convert JSON response to dictionary

    #IF the current position is in the same map as specified, return the x and y coordinates along with the robot's orientation within the map
    if result['mapId'] == mapid:
        # Return real world x coordinate value, y coordinate value, orientation in radians
        return result['x'], result['y'], result['theta']



'''
Send waypoint values for a robot to move to - x & y coordinate and theta
RESPONSE: { "message": "Action executed" }
After Execution of moverobot(robotid,10,10,-2.8662242889404297)
get_robot_pos gives RESPONSE: { "mapId": "map", "mapDataHash": "6051606626958011017", "x": 0.015002617612481117, "y": 0.05243345722556114,
"theta": 0.1102590337395668, "ts": 1634604390908, "xPixels": 359.5001484528217, "yPixels": 533.1216676113382
}
'''
def moverobot(robotId, movetox, movetoy, movetotheta):
    #POST /robots/robotId/navigation/waypoint
    url = 'https://api.inorbit.ai/robots/'+robotId+'/navigation/waypoints'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-auth-inorbit-app-key': API_KEY
    }
    #Convert waypoint parameters - x,y,theta - to JSON
    payload = json.dumps({
      "waypoints": [
        {
          "x": movetox,
          "y": movetoy,
          "theta": movetotheta
        }
      ]
    })
    response = requests.request('POST', url, headers=headers, data=payload) # get response from InOrbit API
    print(response.json())
    result = json.loads(response) # Convert JSON response to dictionary
    if result('message') == 'Action executed':
        return True


def get_actions(robotId):
    url = 'https://api.inorbit.ai/robots/'+robotId+'/actionDefinitions'
    headers = {
        'Accept': 'application/json',
        'x-auth-inorbit-app-key': API_KEY
    }
    response = requests.request('GET', url, headers=headers, data=payload)
    result = json.loads(response)
    return result['actionId']


def perform_action(robotId, actionId):
    url = 'https://api.inorbit.ai/robots/'+robotId+'/actions'
    headers = {
        'Accept': 'application/json',
        'x-auth-inorbit-app-key': API_KEY
    }
    payload = json.dumps({
      "actionId": actionId,
      "parameters": {
        "param1": "some value",
        "param2": "otherValue"
      }
    })
    response = requests.request('POST', url, headers=headers, data=payload)
    '''{
      "executionId": "string",
      "status": "started",
      "statusDetails": "string",
      "startTs": 0,
      "lastUpdateTs": 0,
      "returnCode": 0,
      "stderr": "string",
      "stdout": "string"
    }
    '''
    result = json.loads(response)
    return result['executionId']

def get_actionstatus(robotId, executionId):
    url = 'https://api.inorbit.ai/robots/'+ robotId +'/actions/'+ executionId
    headers = {
        'Accept': 'application/json',
        'x-auth-inorbit-app-key': API_KEY
    }
    response = requests.request('GET', url, headers=headers, data=payload)
    '''{
      "executionId": "string",
      "status": "started",
      "statusDetails": "string",
      "startTs": 0,
      "lastUpdateTs": 0,
      "returnCode": 0,
      "stderr": "string",
      "stdout": "string"
    }
    '''
    result = json.loads(response)
    if result['executionId'] == executionId
        return result['status']

robotID = get_robots() # get list of all robots
for ids in robotID:
    if get_robot(ids):
        #if Robot is Online
        mapid, mapwidth, mapheight, mapresolution, maporiginx, maporiginy = get_current_map(ids)
        curr_x, curr_y, curr_theta = get_robot_pos(ids,mapid)
        destination_x = 10  #Go left
        destination_y = 10  # Straight Left
        destination_theta = -2.8662242889404297  # rotate by 180°
        while moverobot(ids, destination_x, destination_y, destination_theta): #go left by 10m and rotate by -3.14rad or 180°,
            # Check if robot is travelling
            #Check if robot has stopped travelling
            travel_x,travel_y,travel_theta = get_robot_pos()
            if ((travel_x - destination_x <= mapresolution) and
                    (travel_y - destination_y <= mapresolution) and
                    (travel_theta - destination_theta <= 0.0349066)):
                pass
                #Finish
        actionid = get_actions(ids)
        execid = perform_action(ids,actionid)
        while get_actionstatus(ids, execid) == 'started':
            pass
            #Till an action is running
