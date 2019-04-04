#!/usr/bin/env python3

import hashlib
import requests
import sys

# md5 of last update stored in azure pipeline variables
old_hash=sys.argv[1]
# Specs from us-east-1 https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-resource-specification.html
url="https://d1uauaxba7bl26.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json"

# Load the source data and hash it
response = requests.get(url)
new_hash = hashlib.md5(response.content).hexdigest()

# If we match previous run, die (killing the pipeline)
if new_hash == old_hash:
    exit(1)

# echo out new hash so pipeline script can update azure variable
print(new_hash)
print("##vso[task.setvariable variable=compare.md5]",new_hash)