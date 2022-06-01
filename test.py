import argparse
import json
import os
import shutil

# Parsing command line arguments:
parser = argparse.ArgumentParser()

# Operation Agrument is required to specify operation-id's to be filtered out.
parser.add_argument('--operation', type=str, required=True)
args = parser.parse_args()
operations = args.operation

# Creating a copy of original opensearch.smithy file for altering operations.
original = r'model/opensearch.smithy'
target = r'opensearch_temp.smithy'

shutil.copyfile( original, target)

command = 'sed "s/operations:.*$/operations: [' + operations +  ']/" opensearch_temp.smithy > model/opensearch.smithy'
os.system(command)
os.system('gradle build')


# Replacing opensearch.smithy file with original content.
shutil.copyfile( target, original)

# Removing temporary file.
os.remove("opensearch_temp.smithy") 

