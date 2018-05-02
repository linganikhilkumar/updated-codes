import boto3

dynamodb=boto3.client('dynamodb')
cpyami=boto3.client('ec2','us-east-1')
response=dynamodb.scan(
    TableName='ami_backup_policy'
      
)
#print response
amis=response['Items']
#print amis
#ls = []
print "for loop started"
for i in response['Items']:
    j=i['ami_ids']['S'] 
#    print j
#    print "for loop ended"
    resp=cpyami.copy_image(
        Name='copied from us-west-2',
        SourceImageId=j,
        SourceRegion='us-west-2'
     )
    print "adding tags"
    cpyami.create_tags(
    Resources=[
    resp['ImageId'],
     ],
    Tags=[
    {
    'Key':'Auto-Backup',
    'Value':'yes',
    },
    {
    'Key':'ami_tag',
    'Value':'M/W/D',
    }
    ]
    )

     

     
#    cpyamil = cpyami.describe_images(ImageIds=[resp['ImageId'],],) 
#    print "copying ami to N.Vergina"
#    while (cpyamil['Images'][0]['State'] == 'pending'):
#        print "#",
    print 'copied ami with id = '+resp['ImageId']+'successfully' 
#    delete_entry = dynamodb.delete_item(
#    TableName = 'ami_backup_policy',
#    Key = {
#        'ami_ids' : {
#            'S' : j
#        }
#    }  
#    )
#    print "deleted ami id"+j+"from dynamodb table"
	
