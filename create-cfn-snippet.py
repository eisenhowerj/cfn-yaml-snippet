#!/usr/bin/env python3

import json
import requests

# Vars

output_file="snippets/resource-types.json"
# specs from us-east-1 https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-resource-specification.html
url="https://d1uauaxba7bl26.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json"

# Load the source data:

r = requests.get(url)
data = r.json()

# Start the output data

output = {}

# Add the resources to the output

for d in data['ResourceTypes']:

    prefix = d.replace('AWS::', "")
    prefix = prefix.replace('::', "-")
    prefix = prefix.lower()

    body = ""
    description = ""
    scope = "source.cloudformation"

    body = body + ( '${1:LogicalID}:\r\n' )

    # add a name placeholder
    body = body + ( '\tType: \"' + d + '\"\r\n' )
    body = body + ( "\tProperties:\r\n")

    description = "Attributes:\r\n"
    if 'Attributes' in data['ResourceTypes'][d]:
        for a in data['ResourceTypes'][d]['Attributes']:
            # description = description + "Attributes: " + "\r\n\t" + a
            description = description + "  " + a + "\r\n"
    else:
        description = "No Attributes\r\n"
    print (description)

    # for each resources 'properties':
    for p in data['ResourceTypes'][d]['Properties']:

        required = data['ResourceTypes'][d]['Properties'][p]['Required']

        item = ""
        itemList = 0


        if ( 'PrimitiveType' in data['ResourceTypes'][d]['Properties'][p] ):
            item = data['ResourceTypes'][d]['Properties'][p]['PrimitiveType']
 
        if ( 'PrimitiveItemType' in data['ResourceTypes'][d]['Properties'][p] ):
            item = data['ResourceTypes'][d]['Properties'][p]['PrimitiveItemType']
 

        if ( 'ItemType' in data['ResourceTypes'][d]['Properties'][p] ):
            item = data['ResourceTypes'][d]['Properties'][p]['ItemType']

        if ( 'Type' in data['ResourceTypes'][d]['Properties'][p] ):
            if ( data['ResourceTypes'][d]['Properties'][p]['Type'] == "List" ):
                itemList = 1
            else:
                itemList = 2
                item = data['ResourceTypes'][d]['Properties'][p]['Type']

        ###########################

        if (itemList == 0):
            body = body +  ( "\t\t" + p + ": " + item + "" )
            if (required):
                body = body + ( " #required\r\n" )
            else:
                body = body + ( "\r\n" )


        elif (itemList == 1):
            body = body +  ( "\t\t" + p + ":" + "" )
            if (required):
                body = body + ( " #required\r\n" )
            else:
                body = body + ( "\r\n" )

            body = body +  ( "\t\t\t- " + item + "\r\n")



        elif (itemList == 2):
            body = body +  ( "\t\t" + p + ":" + "" )
            if (required):
                body = body + ( " #required\r\n" )
            else: 
                body = body + ( "\r\n" )

            body = body +  ( "\t\t\t" + item + "\r\n")
        
        output[d] ={ "prefix" : prefix, "body" : body, "description" : description }

#print( json.dumps(output) )

with open(output_file, "w") as text_file:
    text_file.write( json.dumps(output))
    