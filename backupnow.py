import boto3
import datetime
import sys
from datetime import date
from pytz import timezone
import pytz
from dateutil.tz import *
# variables
backup_tag = 'AMI_Backup_Policy'

#current_dest_time = '03:00'
# current time
client = boto3.client('ec2')
dynamodb = boto3.client('dynamodb')
def create_ami(inst):
	amiresponse = client.create_image(InstanceId=inst, Name= inst+'-'+date.today())
        client.create_tags(Resources=[amiresponse['ImageId'],],Tags=[{'Key': 'Auto-Backup','Value': 'yes',},],)
        dynamodb.put_item(TableName = 'ami_backup_policy',Item={'ami_ids' :{'S': amiresponse['ImageId'],}})

def lambda_handler(event, keys):
    current_local_time = tzlocal()
    now = datetime.datetime.now()   
    now = now.replace(tzinfo = current_local_time) 
 #   time_now = create_time.strftime("%H:%M")
 #    print now
    ty = pytz.timezone('US/Eastern')
    current_dest_time = now.astimezone(ty)
    print current_dest_time
   
  
    response = client.describe_instances(Filters=[{'Name': 'tag-key', 'Values':[backup_tag]}])
# print response
    for reservation in response['Reservations']:
        for n in reservation['Instances']:
            for j in  n['Tags']:
                if j['Key'] == backup_tag:
                	bvalue =  j['Value']
                	if current_dest_time == bvalue.split('-')[0]:
                		create_ami(n['InstanceId']);               		
