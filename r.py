import boto3

client = boto3.client('ec2','us-east-1')
response = client.describe_images(Filters=[{'Name': 'tag:ami_tag','Values': ['M/W/D',]},])
amis= []
for i in response['Images']:
    amis.append(i['ImageId'])
print ami
if(len(amis)==0):
    print 'there are no amis with given tag'
else:
    print 'deletion of amis started'
    for j in amis:
        print 'Deregistering AMI with id '+j
        amis_delete = client.deregister_image(
        ImageId=j,
        ) 
        print 'AMI With id '+j+' deregistered' 	

