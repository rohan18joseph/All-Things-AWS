import json
import boto3
import sys

def domain_finder():
    input_cert=sys.argv[1]
    list_final = []
    ec2 = boto3.client('ec2')
    response = ec2.describe_regions()
    region_list = response['Regions']
    regions = list()
    # print(region)
    for item in region_list:
        regions.append(item['RegionName'])
    # list regions now contains all aws regions
    #below for loop to iterate for every region
    for x in range(0, len(regions)):
        try:
            apigw = boto3.client('apigateway', regions[x])
            dict_domain_names = apigw.get_domain_names()
            try:
                for i in range(len(dict_domain_names["items"])):
                    keys = list(dict_domain_names["items"][i].keys())
                    if ("certificateArn" in keys):
                        #checks for certs of edge optimized domains
                        cert_arn = dict_domain_names["items"][i]["certificateArn"]
                        list_final.append([cert_arn, dict_domain_names["items"][i]["domainName"], regions[x]])
                    else:
                        #checks for certs of regional domains
                        cert_arn = dict_domain_names["items"][i]["regionalCertificateArn"]
                        list_final.append([cert_arn, dict_domain_names["items"][i]["domainName"], regions[x]])
            except:
                pass
        except:
            pass
    #list_final contains all API gateway assoc iated certificates and domains.
    #below for loop to check if cert is present in list of all the certificates associated to domain.
    flag=0
    for i in list_final:
        if input_cert in i:
            flag=1
            print("DOMAIN NAME : ", i[1])
            print("REGION : ", i[2])
    if flag==0:
        print("Certificate is not associated to any API Gateway domain")



#Calling the function
domain_finder()
