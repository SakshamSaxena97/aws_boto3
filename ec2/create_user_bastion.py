#!/usr/bin/python3
import boto3
import re
import subprocess
from pprint import pprint
from scp import SCPClient
import pysftp
import paramiko

ip = input("Ur IP:")
print (ip)
user = input("Name of User:")
print(user)
reg= input("Region (us-east-1 / ap-southeast-1): ")
username = input("Username (ubuntu/centos/admin): ")
userKey = input("Enter the user's key:")
ec2client = boto3.client('ec2',region_name='{0}'.format(reg))

response = ec2client.describe_instances()
# pprint(response)
user_key = userKey
server_data = dict()
server_data['InstanceID'] = []
server_data['VpcID'] = []
server_data['IP'] = []
server_data['Name'] = []
server_data['keyName'] = []
bastion = ['cl-panel-bastion','kafka-bastion','core-dev-bastion','godam-dev-bastion-server','DSG-bastion-aza','central-staging-bastion','done-nginx-bastion','Saksham','central-dev-bastion','done-data-quality-bastion']
# print (bastion)
for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:      
        state = instance["State"]
        # print (state['Name'])
        if state['Name'] == 'running':
            flag = 0
            # pprint(instance)
            # server_data.append(instance["InstanceId"])
            # print(instance["InstanceId"])   
            if 'Tags' in instance:
                tag = instance['Tags'] 
                # pprint (tag)
                # # print (len(server_data))            
                for i in tag:
                    key = i['Key']
                    value = i['Value']
                    if key == 'Name':
                        for j in range(len(bastion)):
                            # print(value + "," + str(j))
                            if value == bastion[j]:
                                bastion_name = value
                                server_data['Name'].append(bastion_name)                            
                                print(server_data['Name'])
                                flag = 1
                                
                                # print(server_data)
                #pprint(instance['InstanceId'])
                if flag == 1:
                    ins = instance['InstanceId']
                    server_data['InstanceID'].append(ins)
                    vpcid = instance['VpcId']
                    server_data['VpcID'].append(vpcid)
                    pubip = instance['PublicIpAddress']
                    server_data['IP'].append(pubip)
                    keyname = instance['KeyName']
                    server_data['keyName'].append(keyname)
                    print (server_data)
            #     count = 0
            #     counter =[]
                    if ip in server_data['IP']:
                        print("This IP is present")
                        ind = server_data['IP'].index(ip)
                        print(server_data['keyName'][ind])
                #         # ec2client = boto3.client('ec2',region_name='us-east-1')

                #         # response = ec2client.describe_instances()
                #         # pprint(response)
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                #         # ip= '34.229.247.166'
                        # username='ubuntu'
                        key_filename= '{0}.pem'.format(server_data['keyName'][ind])
                        print(key_filename)
                        # user =    'check_new'
                        user_key = userKey
                        # group = 'admin'
                        yml_string="""
- hosts: localhost
  sudo: yes
  tasks:

     - name: Add User
       user: name={0}
             shell=/bin/bash
             
     - name: Adding keys for {0}
       authorized_key: user={0} key="{1}" path=/home/{0}/.ssh/authorized_keys state=present
       with_items: ssh_keys.results                    

                        """.format(user,user_key)

                        fh=open('/home/delhivery/pyaws/user.yml','w')
                        fh.write(yml_string + "\n")
                        fh.close()

                        ssh.connect(ip,
                                    username='{0}'.format(username),
                                    key_filename='{0}.pem'.format(server_data['keyName'][ind]))


                        

                        # check = subprocess.Popen("sudo ansible --version", shell=True, stdout=subprocess.PIPE).stdout.read()
                        

                        command = 'sudo apt-add-repository ppa:ansible/ansible && sudo apt-get update && sudo apt-get install ansible -y && sudo ansible-playbook user.yml && ls /home'
                        stdin, stdout, stderr = ssh.exec_command(command)
                        print("Commands executed \n")
                        
                        subprocess.Popen("scp -i " + str(key_filename) + " /home/delhivery/pyaws/user.yml " + str(username) + "@" + str(ip) + ":~/", shell=True, stdout=subprocess.PIPE).stdout.read()            
                        print("SCP Done")

                        stdin.flush()
                        data = stdout.read().splitlines()
                        for line in data:   
                            print (line)
                        ssh.close()

                        print("All done")
                        break      
                    else:     
                        print("No such Bastion in the list")


        
        