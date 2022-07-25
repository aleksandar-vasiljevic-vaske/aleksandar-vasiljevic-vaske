import os
import subprocess
import json
import time
import boto3
import Parameters

###___Promenljive___###
# Promenljiva koja cuva vrednosti kreirane uloge
v_Role_Name = "Zadatak2V3"
#v_Role_Details = {}

v_SNS_Topic_Name = "Zadatak2V3"
#v_SNS_Topic_Details = {}
#v_SNS_Topic_ARN = ''



###___Kraj Promenljivih___###

###___Funkcije___###


###___Kraj Funkcija___###


######_______POCETAK GLAVNOG PROGRAMA_______######

# Kreiranje uloge za izvrsavanje Lamda funkcije
#os.system("aws iam create-role --role-name %s --assume-role-policy-document '{\"Version\": \"2012-10-17\",\"Statement\": [{ \"Effect\": \"Allow\", \"Principal\": {\"Service\": \"lambda.amazonaws.com\"}, \"Action\": \"sts:AssumeRole\"}]}' --profile %s > v_Role_Details.json" %(v_Role_Name,Parameters.Profile))

v_Role_Details_Dict = open('v_Role_Details.json')
v_Role_Arn = json.load(v_Role_Details_Dict)
print(v_Role_Arn["Role"]["Arn"])

# Cekanje (stopiranje izvrsenja glavnog programa) 10 sekundi da se izvrsi prethodna komanda kako ne bi doslo do nepredvidjenih gresaka
###time.sleep(10)

# Dodavanje polise za izvrsavanje Lamda servisa novokreiranoj ulozi
###os.system("aws iam attach-role-policy --role-name %s --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole --profile %s" %(v_Role_Name,Parameters.Profile))

# Cekanje (stopiranje izvrsenja glavnog programa) 10 sekundi da se izvrsi prethodna komanda kako ne bi doslo do nepredvidjenih gresaka
###time.sleep(10)

# Kreiranje SNS teme
###os.system("aws sns create-topic --name %s --profile %s > v_SNS_Topic_Details.json" %(v_SNS_Topic_Name,Parameters.Profile))
v_SNS_Topic_Details_Dict = open('v_SNS_Topic_Details.json')
v_SNS_Topic_Arn = json.load(v_SNS_Topic_Details_Dict)
print(v_SNS_Topic_Arn["TopicArn"])

# Cekanje (stopiranje izvrsenja glavnog programa) 10 sekundi da se izvrsi prethodna komanda kako ne bi doslo do nepredvidjenih gresaka
###time.sleep(10)

# Prijavljivanje korisnika na SNS temu
###os.system("aws sns subscribe --topic-arn %s --protocol email --notification-endpoint aleksandar.vasiljevic.vaske@gmail.com --profile %s > v_SNS_Topic_Subscription_Status.json" %(v_SNS_Topic_Arn["TopicArn"],Parameters.Profile))

v_SNS_Topic_Subscription_Status_Dict = open('v_SNS_Topic_Subscription_Status.json')
v_SNS_Topic_Subscription_Status_State = json.load(v_SNS_Topic_Subscription_Status_Dict)

# Kreiranje deployment koda
###os.system("touch ./lambda_function.py")
###Deploy_File = open("./lambda_function.py", "w")
###Deploy_File.write("import json\nimport boto3\n\ndef lambda_handler(event, context):\n\tnotification = \"Hello, world!\"\n\tclient = boto3.client('sns')\n\tresponse = client.publish (\n\t\tTargetArn = \"%s\",\n\t\tMessage = json.dumps({\'default\': notification}),\n\t\tMessageStructure = \'json\'\n)\n\nreturn {\n\t\'statusCode\': 200\n}\n" %v_SNS_Topic_Arn["TopicArn"])
###Deploy_File.close()

# Cekanje (stopiranje izvrsenja glavnog programa) 10 sekundi da se izvrsi prethodna komanda kako ne bi doslo do nepredvidjenih gresaka
###time.sleep(10)

#  Kreiranje deployment arhive
###os.system("zip ./Zadatak2V3Deploy.zip ./lambda_function.py")

# Cekanje (stopiranje izvrsenja glavnog programa) 10 sekundi da se izvrsi prethodna komanda kako ne bi doslo do nepredvidjenih gresaka
###time.sleep(10)

# Kreiranje Lamda servisa i Deploy koda Lamda funkcije
###os.system("aws lambda create-function --function-name %s --region %s --zip-file fileb://Zadatak2V3Deploy.zip --runtime python3.9 --handler \"main/lambda_handler\" --role %s --profile %s > v_Lambda_Function_Details.json" %(v_SNS_Topic_Name,Parameters.Region,v_Role_Arn["Role"]["Arn"],Parameters.Profile))
v_Lambda_Funcion_Details_Dict = open('v_Lambda_Function_Details.json')
v_Lambda_Function_Arn = json.load(v_Lambda_Funcion_Details_Dict)
print(v_Lambda_Function_Arn["FunctionArn"])

# Cekanje (stopiranje izvrsenja glavnog programa) 10 sekundi da se izvrsi prethodna komanda kako ne bi doslo do nepredvidjenih gresaka
###time.sleep(10)

# Kreiranje EventBridge okidaca
###os.system("aws events put-rule --schedule-expression \"cron(0 23 * * ? *)\" --name %s --profile %s > v_CloudWatch_Rule_Details.json" %(v_SNS_Topic_Name,Parameters.Profile))
v_CloudWatch_Rule_Details_Dict = open('v_CloudWatch_Rule_Details.json')
v_CloudWatch_Rule = json.load(v_CloudWatch_Rule_Details_Dict)
print(v_CloudWatch_Rule["RuleArn"])

# Dodela prava CloudWatch Event Rule-u da okida Lambda Funkciju
os.system("aws lambda add-permission --function-name %s --statement-id 'AllowCloudWatchLambda' --action 'lambda:InvokeFunction' --principal events.amazonaws.com --source-arn %s --profile %s > v_Event_Rule_Permission.json"%(v_Lambda_Function_Arn["FunctionName"],v_CloudWatch_Rule["RuleArn"],Parameters.Profile))

# Povezivanje CloudWatch Event Rule-a i Lambda Funkcije
os.system("aws events put-targets --rule %s --targets '{\"Id\": \"1\", \"Arn\": \"%s\"}' --profile %s" %(v_SNS_Topic_Name,v_Lambda_Function_Arn["FunctionArn"],Parameters.Profile))


######_______KRAJ GLAVNOG PROGRAMA______######
