import requests
import json

API_KEY = 'ABC123'


def get_robots():
    url = 'https://api.inorbit.ai/robots'
    headers = {
      'Accept': 'application/json',
      'x-auth-inorbit-app-key': API_KEY
    }
    response = requests.request('GET', url, headers = headers, data=payload)
    print(response)
    arrayofrobots = json.loads(response)
    '''[
          {
            "id": "string",
            "name": "string",
            "agentOnline": true,
            "agentVersion": "string",
            "updatedTs": 0
          }
    ]'''
    '''for loop to collect all IDS:
        pass'''
    return arrayofrobots['id']


def get_robot(robotId):
    url = 'https://api.inorbit.ai/robots/'+robotId
    headers = {
      'Accept': 'application/json',
      'x-auth-inorbit-app-key': API_KEY
    }
    response = requests.request('GET', url, headers = headers, data=payload)
    robotattributes = json.loads(response)
    if robotattributes['agentOnline'] == 'true':
        return True

    '''{
        "id": "0011-aabb-cccc",
        "name": "demo-robot-1234",
        "agentOnline": true,
        "agentVersion": "1.2.3",
        "updatedTs": 1594944602962
    }'''


def get_current_map(robotId):
    url = 'https://api.inorbit.ai/robots/'+robotId+'/maps/current'
    headers = {
        'Accept': 'application/json',
        'x-auth-inorbit-app-key': API_KEY
    }
    response = requests.request('GET', url, headers = headers, data=payload)
    result = json.loads(response)
    mapid = result['mapId']
    mapresolution = result['resolution']
    mapwidth = result['width'] * mapresolution
    mapheight = result['height'] * mapresolution
    maporiginx = result['x']
    maporiginy = result['y']
    '''[
        {
            "robotId": "string",
            "mapId": "string",
            "label": "string",
            "width": 0,
            "height": 0,
            "resolution": 0,
            "x": 0,
            "y": 0,
            "dataHash": "string",
            "updatedTs": 0
        }
    ]'''
    return mapid, mapwidth, mapheight, mapresolution, maporiginx, maporiginy


def get_robot_pos(robotId, mapid):
    url = 'https://api.inorbit.ai/robots/'+robotId+'/localization/pose'
    headers = {
        'Accept': 'application/json',
        'x-auth-inorbit-app-key': API_KEY
    }
    response = requests.request('GET', url, headers = headers, data=payload)
    '''{
        "mapId": "string",
        "mapDataHash": "string",
        "x": 0,
        "y": 0,
        "theta": 0,
        "ts": 0,
        "xPixels": 0,
        "yPixels": 0
    }'''
    result = json.loads(response)
    if result['mapId'] == mapid:
        return result['x'], result['y'], result['theta']


def moverobot(robotId, movetox, movetoy, movetotheta):
    #post_waypoints
    url = 'https://api.inorbit.ai/robots/'+robotId+'/navigation/waypoints'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-auth-inorbit-app-key': API_KEY
    }
    payload = json.dumps({
      "waypoints": [
        {
          "frameId": "string",
          "x": movetox,
          "y": movetoy,
          "theta": movetotheta
        }
      ]
    })
    response = requests.request('POST', url, headers=headers, data=payload)
    print(response.json())
    #if check a parameter in response to make sure its running:
    #    return True


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
        destination_x = curr_x-10  #Go left
        destination_y = curr_y-0  # Straight Left
        destination_theta = curr_theta-3.14159  # rotate by 180°
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
            #Till an action is running
