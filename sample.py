import requests
import json

API_KEY = 'hKa5akD7RKqdCsmB'


def get_robots():
    # Get information on all robots available for the user
    # RESPONSE: [{"id": "robsimhaydryq9lfgphbn4", "name": "sim-test", "agentVersion": "3.24.0", "agentOnline": false, "updatedTs": 1634583464630 }]

    # GET /robots request
    url = 'https://api.inorbit.ai/robots'
    headers = {
      'Accept': 'application/json',
      'x-auth-inorbit-app-key': API_KEY
    }
    response = requests.request('GET', url, headers = headers)  # Get response from InOrbit API
    arrayofrobots = response.json()  # Convert JSON response to dictionary
    print(arrayofrobots)
    for allrobots in arrayofrobots:
        print(allrobots['id'])
        return [allrobots['id']]


def get_robot(robotId):
    # Get attribute details about a particular robot using its robotId
    # RESPONSE: { "id": "robsimhaydryq9lfgphbn4", "name": "sim-test", "agentVersion": "3.24.0", "agentOnline": true, "updatedTs": 1634603503255 }

    # GET /robots/robotId request
    url = 'https://api.inorbit.ai/robots/'+robotId
    headers = {
      'Accept': 'application/json',
      'x-auth-inorbit-app-key': API_KEY
    }
    response = requests.request('GET', url, headers = headers)  # Get response from InOrbit API
    robotattributes = response.json()  # Convert JSON response to dictionary
    print(robotattributes)
    if robotattributes['agentOnline'] == True:
        #agentOnline has possible values of true or false
        #IF the agent on the robot is online and the robot is able to communicate with InOrbit return True otherwise return False
        return True
    return False


def get_current_map(robotId):
    # Get details of current map of the robot
    # RESPONSE: { "robotId": "robsimhaydryq9lfgphbn4", "mapId": "map", "updatedTs": 1634571279270, "label": "map", "dataHash": "6051606626958011017",
    #    "height": 1066, "width": 719, "resolution": 0.019999999552965164, "x": -7.175000190734863, "y": -10.609999656677246 }

    # GET /robots/robotId/maps/current request
    url = 'https://api.inorbit.ai/robots/'+robotId+'/maps/current'
    headers = {
        'Accept': 'application/json',
        'x-auth-inorbit-app-key': API_KEY
    }
    response = requests.request('GET', url, headers = headers)  # Get response from InOrbit API
    result = response.json()  # Convert JSON response to dictionary
    print(result)

    # Calculate the real world length and width size of the area represented by the map by using its pixel values and resolution
    mapresolution = result['resolution']
    maplength = result['height'] * mapresolution  # height in pixels * resolution
    mapwidth = result['width'] * mapresolution  # width in pixels * resolution
    print(result['mapId'])

    # Return the values of mapId, resolution, width and height in real world size, origin x & y
    return result['mapId'], mapwidth, maplength, mapresolution, result['x'], result['y']


def get_robot_pos(robotId, mapid):
    # Get the current position of the robot in the specified map
    # RESPONSE: {"mapId": "map", "mapDataHash": "6051606626958011017", "x": 1.747115135192871, "y": 8.967257499694824, "theta": -2.8662242889404297,
    #           "ts": 1634583459839, "xPixels": 446.10577626762785, "yPixels": 978.8628796978938}

    # GET /robots/robotId/localization/pose request
    url = 'https://api.inorbit.ai/robots/'+robotId+'/localization/pose'
    headers = {
        'Accept': 'application/json',
        'x-auth-inorbit-app-key': API_KEY
    }
    response = requests.request('GET', url, headers = headers)  # Get response from InOrbit API
    result = response.json()  # Convert JSON response to dictionary
    print(result)
    # IF the current position is in the same map as specified, return the x and y coordinates along with the robot's orientation within the map
    if result['mapId'] == mapid:
        # Return real world x coordinate value, y coordinate value, orientation in radians
        return result['x'], result['y'], result['theta']


def moverobot(robotId, movetox, movetoy, movetotheta):
    # Send waypoint values for a robot to move to - x & y coordinate and theta
    # RESPONSE: { "message": "Action executed" }
    # After Execution of moverobot(robotid,10,10,-2.8662242889404297)
    # get_robot_pos gives RESPONSE: { "mapId": "map", "mapDataHash": "6051606626958011017", "x": 0.015002617612481117, "y": 0.05243345722556114,
    # "theta": 0.1102590337395668, "ts": 1634604390908, "xPixels": 359.5001484528217, "yPixels": 533.1216676113382 }

    # POST /robots/robotId/navigation/waypoint
    url = 'https://api.inorbit.ai/robots/'+robotId+'/navigation/waypoints'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-auth-inorbit-app-key': API_KEY
    }

    # Convert waypoint parameters - x,y,theta - to JSON
    payload = json.dumps({
      "waypoints": [
        {
          "x": movetox,
          "y": movetoy,
          "theta": movetotheta
        }
      ]
    })
    response = requests.request('POST', url, headers=headers, data=payload)  # Get response from InOrbit API
    print(response)
    result = response.json()  # Convert JSON response to dictionary
    print(result)
    if result['message'] == 'Action executed':
        # IF move robot action is executed successfully, return True,
        # otherwise return False in all other scenarios or execution or communication failing
        return True
    return False


def get_actions(robotId, actionlabel):
    # Get the list of actions available for the robot
    # RESPONSE: [ { "actionId": "RunScript-xp3InB", "type": "PublishToTopic", "label": "Pickup", "requiresLock": false, "parameters": [] },
    #            { "actionId": "PublishToTopic-jFHZjB", "type": "PublishToTopic", "label": "Heavy Load", "requiresLock": false, "parameters": [] },
    #            { "actionId": "PublishToTopic-t-CmZy", "type": "PublishToTopic", "label": "Dock", "requiresLock": false, "parameters": [] } ]

    # GET /robots/robotId/actionDefinitions
    url = 'https://api.inorbit.ai/robots/'+robotId+'/actionDefinitions'
    headers = {
        'Accept': 'application/json',
        'x-auth-inorbit-app-key': API_KEY
    }
    response = requests.request('GET', url, headers=headers)  # Get response from InOrbit API
    result = response.json()  # Convert JSON response to dictionary
    print(result)
    for actions in result:
        # FOR all available actions, IF the action label we need exists, return the actionId for it
        if actions['label'] == actionlabel:
            return actions['actionId']


def perform_action(robotId, actionId):
    # Execute an action for a robot
    # On running perform_action(robotId,"RunScript-xp3InB")
    # RESPONSE: { "status": "started", "startTs": 1634609482097, "lastUpdateTs": 1634609482097 }

    # POST /robots/robotId/actions
    url = 'https://api.inorbit.ai/robots/'+robotId+'/actions'
    headers = {
        'Accept': 'application/json',
        'x-auth-inorbit-app-key': API_KEY
    }
    payload = json.dumps({
      "actionId": actionId
    })
    response = requests.request('POST', url, headers=headers, data=payload)  # Get response from InOrbit API
    result = response.json()  # Convert JSON response to dictionary
    print(result)
    return result['executionId']  # TODO: if Execution ID is returned in all query responses or for a certain type of request


def get_actionstatus(robotId, executionId):
    # Get Action's current status
    # According to the API documentation the above POST command should return an executionId but it didn't.
    # RESPONSE here should be: { "executionId": "string", "status": "started", "statusDetails": "string", "startTs": 0, "lastUpdateTs": 0,
    #                    "returnCode": 0, "stderr": "string", "stdout": "string" }

    # GET /robots/robotId/actions/executionId
    url = 'https://api.inorbit.ai/robots/'+ robotId +'/actions/'+ executionId
    headers = {
        'Accept': 'application/json',
        'x-auth-inorbit-app-key': API_KEY
    }
    response = requests.request('GET', url, headers=headers)  # Get response from InOrbit API
    result = response.json()  # Convert JSON response to dictionary
    print(result)
    if result['executionId'] == executionId:
        # IF the execution id in the response matches the one provided, return the status of the action
        return result['status']

if __name__ == '__main__':
    robotID = get_robots()  # Get list of all robots
    for ids in robotID:
        # FOR all available robots
        if get_robot(ids):
            # IF Robot is Online
            mapid, mapwidth, mapheight, mapresolution, maporiginx, maporiginy = get_current_map(ids)
            curr_x, curr_y, curr_theta = get_robot_pos(ids, mapid)
            destination_x = 10  # Go to x = 10
            destination_y = 10  # Go to y = 10
            destination_theta = -2.8662242889404297  # rotate by 180°
            if moverobot(ids, destination_x, destination_y, destination_theta):  # Move to new Waypoint
                # TODO: Check if robot is travelling
                # TODO: Check if robot has stopped travelling
                # TODO: Wait till above checks are being performed and then
                travel_x, travel_y, travel_theta = get_robot_pos()  # Get new position of robot after it has finished travelling
                if ((travel_x - destination_x <= mapresolution) and
                        (travel_y - destination_y <= mapresolution) and
                        (travel_theta - destination_theta <= 0.0349066)):
                    pass
                    # Finish checking if robot has arrived at destination
            actionid = get_actions(ids, 'Pickup')
            # execid = perform_action(ids, actionid)
            # while get_actionstatus(ids, execid) == 'started':
            #    pass
                # Till an action is running
