import boto3 
import json
import csv

fields = ['Account ID','Email']
rows=list()
client=boto3.client('organizations')
paginator = client.get_paginator('list_accounts') #setting up a paginator
pages= paginator.paginate()
for page in pages:
    account=page['Accounts'] #listing out all accounts in specific page
    for acc in account:
        rows.append([acc['Id'],acc['Email']]) #filtering and appending account id, email to the 
filename="accountlist.csv" #name of csv file -&gt; in same location as the script

with open(filename, 'w') as csvfile: 
    csvwriter = csv.writer(csvfile)  # creating a csv writer object   
    csvwriter.writerow(fields)  # writing the fields 
    csvwriter.writerows(rows)   # writing the data rows 
