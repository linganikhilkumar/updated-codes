from datetime import datetime
import boto3
import datetime
from dateutil.tz import * 

#variable
tablename = 'ami_backup_policy'
dest_region = 'us-east-1'
src_region = 'us-west-2'


datenowest = datetime.datetime.now(gettz("US/Eastern")) 
todaydayest = datenowest.strftime('%A')
todaydateest = datenowest.strftime("%Y-%m-%d")
todaydateest1  = datenowest.strftime("%Y-%m-01")

dynamodb=boto3.client('dynamodb',src_region)
cpyami=boto3.client('ec2',dest_region)



response=dynamodb.scan(TableName= tablename)

amis=response['Items']

#print "for loop started"
for i in response['Items']:
    j=i['ami_ids']['S'] 
#    print j
#    print "for loop ended"
    resp=cpyami.copy_image(
        Name='copy of '+j+' from us-west-2',
        SourceImageId = j,
        SourceRegion = src_region
     )
    print "adding tags"


    if  todaydayest == 'Sunday'  :  
        cpyami.create_tags(Resources=[resp['ImageId'],],Tags=[{'Key':'Auto-Backup','Value':'yes',},{'Key':'Backup_type','Value':'W',}])
    elif todaydateest == todaydateest1:
        cpyami.create_tags(Resources=[resp['ImageId'],],Tags=[{'Key':'Auto-Backup','Value':'yes',},{'Key':'Backup_type','Value':'M',}])
    else:
        cpyami.create_tags(Resources=[resp['ImageId'],],Tags=[{'Key':'Auto-Backup','Value':'yes',},{'Key':'Backup_type','Value':'D',}])

     
     
    print 'copied ami with id = '+resp['ImageId']+'successfully' 
    delete_entry = dynamodb.delete_item(
    TableName = 'ami_backup_policy',
    Key = {
        'ami_ids' : {
            'S' : j
        }
    }  
    )
    print "deleted ami id"+j+"from dynamodb table"
	
