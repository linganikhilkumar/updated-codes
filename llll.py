import boto3
import datetime
import sys
from datetime import  date 
#variables
backup_tag= "AMI_Backup_Policy"
instancelist = []
timelist = []
newtimelist = []
#current time 

create_time = datetime.datetime.now()
#time_now = create_time.strftime("%H:%M")
time_now = '02:00'
#print time_now
today = date.today();
client = boto3.client('ec2')
dynamodb = boto3.client('dynamodb')
response = client.describe_instances(Filters=[{'Name': 'tag-key','Values':[backup_tag]}])

for reservation in response['Reservations']:
    for n in reservation['Instances'][0]['Tags']:
        if n['Key'] == backup_tag :
            b=n["Value"].split("-")
            timelist.append(b[0])       
    print timelist
for i in timelist:
    if i == time_now:
	newtimelist.append(i)

    print newtimelist

for time in  newtimelist:

    instance = reservation['Instances'][0]['InstanceId']
    print 'creating ami'
    amiresponse = client.create_image(InstanceId=instance, Name= instance +"-"+ str(today) )
    client.create_tags(
    Resources=[
    amiresponse['ImageId'],
        ],
    Tags=[
    {
    'Key': 'Auto-Backup',
    'Value': 'yes',
    },
    ],
    )
                
    print "copying ami id "+amiresponse['ImageId']+" to Dynamo db "
    dynamodb.put_item(
    TableName = 'ami_backup_policy',
    Item={'ami_ids' :{
    'S': amiresponse['ImageId'],
    }
    })

