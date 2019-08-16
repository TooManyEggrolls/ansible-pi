import boto3
import sys

# Create a client w/ virginia region
client = boto3.client('ec2', region_name='us-east-1')

# Fetch all instances where Description tag = user input string
describe_response = client.describe_instances(Filters=[
    {'Name': 'tag:Description',
        'Values': [
            sys.argv[1],
        ]
     },
]
)

# Get the state of each instance(running, stopped, etc)
for res in describe_response['Reservations']:
    print(res['Instances'][0]['InstanceId'] + ' is ' +
          res['Instances'][0]['State']['Name'])

# Gather a list of just only the stopped servers, to start later.
stopped_instanceIDs = []
for res in describe_response['Reservations']:
    if res['Instances'][0]['State']['Name'] == 'stopped':
        stopped_instanceIDs.append(res['Instances'][0]['InstanceId'])

		
# Gather a list of just only the running servers, to stop later.
running_instanceIDs = []
for res in describe_response['Reservations']:
    if res['Instances'][0]['State']['Name'] == 'running':
        running_instanceIDs.append(res['Instances'][0]['InstanceId'])

	
#Argument for discovering if all are started or stopped already
if sys.argv[2] == 'start' and not stopped_instanceIDs:
    print("all servers are already started")

# Start the whole list at once in a single call
elif sys.argv[2] == 'start':
    startlist_response = client.start_instances(
        InstanceIds=stopped_instanceIDs, DryRun=False)
		
# Parse the response to see what happened to each server
    for res in startlist_response['StartingInstances']:
        print(
            'InstanceID: ' +
            res['InstanceId'] +
            ' has transitioned from ' +
            res['PreviousState']['Name'] +
            ' to ' +
            res['CurrentState']['Name'])

elif sys.argv[2] == 'stop' and not running_instanceIDs:
    print("all servers are already stopped")

# Stop the whole list at once in a single call
	
elif sys.argv[2] == 'stop':
    stoplist_response = client.stop_instances(
        InstanceIds=running_instanceIDs, DryRun=False)

# Parse the response to see what happened to each server
    for res in stoplist_response['StoppingInstances']:
        print(
            'InstanceID: ' +
            res['InstanceId'] +
            ' has transitioned from ' +
            res['PreviousState']['Name'] +
            ' to ' +
            res['CurrentState']['Name'])

else:
    print("please look at your syntax")
	
print("Process Completed")
