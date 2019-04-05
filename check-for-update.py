#!/usr/bin/env python3
######################
# Azure pipeline runs on a schedule
# We get md5 hash of Amazon's spec file and compare to previous hash stored in file
# If it matches, exit 1 thus blocking the pipeline from continuing
# If it doesn't, update the file and git the file so next run will/won't be blocked

import hashlib
import requests
import sys

# md5 of last update stored in a file
hash_file="current-json-spec-hash"
# Specs from us-east-1 https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-resource-specification.html
url="https://d1uauaxba7bl26.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json"

# Load the source data and hash it
response = requests.get(url)
new_hash = hashlib.md5(response.content).hexdigest()

# Load the current hash
with open(hash_file, 'r') as text_file:
    old_hash = text_file.read()

# If we match previous run, die (blocking the pipeline)
if new_hash == old_hash:
    print("Hash matches, die")
    exit(1)

# echo out new hash so pipeline script can update azure variable
with open(hash_file, "w") as text_file:
    text_file.write(new_hash)