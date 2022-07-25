# Uvozimo potrebne biblioteke i pomocne fajlove
import boto3
import os.path
import time
import json
import Parameters
from os.path import dirname
from requests import get

# Utvrdjujemo koji je IP masine sa koje se pokrece skript
myip = get('https://api.ipify.org').text
print 'My public IP address is: ', myip

script_dir = dirname(__file__)
print(script_dir)

# Postavljamo parametre sesije sa AWS-om/CloudFormation-om
boto3.setup_default_session(profile_name='awsuser')

sess = boto3.Session(region_name=Parameters.Region, profile_name='awsuser')
# Inicijalizacija sesije za CloudFormation
myclient = sess.client('cloudformation')

# Inicijalizacija stack promenljive
stack = ''

# Uzimamo iz navedenog CloudFormation StackTemplate-a/fajla sve informacije i smestamo ih u promenljivu stack
with open('%s' %Parameters.StackTemplate) as fd:
    stack = fd.read()
#    print(stack)


# Postavka parametara za CloudFormation Template i smestanje istih u promenljivu params

    params = [
#        {
#            'ParameterKey': 'Instance-Type',
#            'ParameterValue': 't2.micro'
#
#        },
        {
            'ParameterKey': 'KeyName',
            'ParameterValue': 'moj-kp-1'
        },
        {
            'ParameterKey': 'SSHLocation',
            'ParameterValue': '%s/32'%myip
        },
        {
            'ParameterKey': 'VPCSetup',
            'ParameterValue': '10.1.0.0/16'
        },
        {
            'ParameterKey': 'MyPublicSubnet',
            'ParameterValue': '10.1.0.0/24'
        }
    ]
# Pozivamo CloudFormation operaciju kreiranja okruzenja iz StackTemplate-a
    myclient.create_stack(StackName=Parameters.StackName, TemplateBody=stack, Parameters=params)
# Cekamo neko vreme jer sam uvideo da komanda cekanja na zavrsetak kreiranja steka puca ukoliko se odmah izvrsava
time.sleep(5.5)
# Izvrsavamo komandu CloudFormation-a kroz AWS CLI da sacekamo kreiranje stack-a
os.system("aws cloudformation wait stack-create-complete --region %s --stack-name %s --profile awsuser" %(Parameters.Region,Parameters.StackName))
# Izvrsavamo komandu CloudFormation-a kroz AWS CLI da nam prikaze detalje o kreiranom steku a najvise zbog izlaza (Outputs) kako bi videli javnu IP adresu/URL novo kreirane EC2 instance/Web Servera
os.system("aws cloudformation describe-stacks --stack-name %s --profile awsuser" %Parameters.StackName)
