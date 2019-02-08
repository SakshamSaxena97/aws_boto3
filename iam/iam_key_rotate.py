#!usr/bin/python3

import boto3
import subprocess
from pprint import pprint
import datetime
import dateutil
from dateutil import parser
from botocore.exceptions import ClientError


try:
    iamclient = boto3.client('iam')
    response = iamclient.list_users()
    # pprint(response)
    iam_data=dict()
    iam_data['Username']=[]
    iam_data['Owner']=[]
    iam_data['AccessKeyID']=[]

    for users in response['Users']:
        # pprint(users)
        user=users['UserName']
        data=iamclient.list_access_keys(UserName=users['UserName'])
        # pprint(data)
        if len(data['AccessKeyMetadata'])==0:
            print ("No Access Key")   
        else:
            # print ("Access Key present")
            for i in data['AccessKeyMetadata']:
                if (i['Status']=='Active'):
                    # print (data)
                    if 'CreateDate' in i:
                        d=datetime.datetime.now().date()-i['CreateDate'].date()
                        if(d.days>=90):
                            # print(i['UserName'])
                            username= i['UserName']
                            # pprint(i)
                            accessKeyId= i['AccessKeyId']
                            # print(iam_data['Username'])
                            tag=iamclient.list_user_tags(UserName=username)
                            # pprint(tag)                                                        
                            tags= tag['Tags'] 
                            if len(tags) == 0:
                                print("There are no tags")
                            else:                           
                                for i in tags:
                                    key = i['Key']
                                    value = i['Value']
                                    # print(value)
                                    if (key == 'Owner'):
                                        iam_data['Owner'].append(value)
                                        iam_data['Username'].append(username)
                                        iam_data['AccessKeyID'].append(accessKeyId)
    # print(iam_data)                                    
                                    
except Exception as e:
    print("Error:",e)

