# print("hello")

import json
import os

# Opening OpenAPI JSON file for checking operation ID.
openapi_file_obj = open(
    "model/opensearch.smithy",
    mode='r',
    encoding='utf-8')
# openapi_data = json.load(openapi_file_obj)
# print(openapi_data)

for x in openapi_file_obj:
    print(x)
    print("\n><><><><><><<><><><><\n")