import json
import boto3

config_client = boto3.client('config')
paginator = config_client.get_paginator('get_compliance_details_by_config_rule')
s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

def send_sns(HTML_EMAIL_CONTENT):
   
    client = boto3.client('ses',region_name='eu-west-3')
    CHARSET = "UTF-8"
    #HTML_EMAIL_CONTENT = notification
   

    response = client.send_email(
        Destination={
            "ToAddresses": [
                "david.nassy@yahoo.com",
            ],
        },
        Message={
            "Body": {
                "Html": {
                    "Charset": CHARSET,
                    "Data": HTML_EMAIL_CONTENT,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Auto-remediated unencrypted S3 Buckets",
            },
        },
        Source="david.nassy@yahoo.com",
    )
def lambda_handler(event, context):
   
    with open("whitelist.db", 'r') as f:
        EXCLUSIONS = f.read().splitlines()
   
    notification=""

    response_iterator = paginator.paginate(
        ConfigRuleName='s3-default-encryption-kms',
        ComplianceTypes=[
            'NON_COMPLIANT'
        ],
        PaginationConfig={
            'MaxItems': 1000,
            'PageSize': 100
        }
    )

    for response in response_iterator:
        non_compliant=json.loads(json.dumps(response, default=str))
        eval_result=non_compliant.get('EvaluationResults')
       
        for e in eval_result:
            non_comp_rsc= e.get('EvaluationResultIdentifier').get('EvaluationResultQualifier').get('ResourceId')
           
            if non_comp_rsc  not in EXCLUSIONS:
               
                bucket = s3.Bucket(non_comp_rsc)
                print(non_comp_rsc)
                bucket_encryption = s3_client.put_bucket_encryption(Bucket= non_comp_rsc,
                    ServerSideEncryptionConfiguration={
                        'Rules': [
                            {
                                'ApplyServerSideEncryptionByDefault': {
                                    'SSEAlgorithm': 'AES256',
                                },
                            },
                        ]
                    },
                )
                notification += f"<a href='https://s3.console.aws.amazon.com/s3/buckets/{non_comp_rsc}' target='_blank'>{non_comp_rsc}</a><br/><br/>"
                send_sns(notification)
               
    


