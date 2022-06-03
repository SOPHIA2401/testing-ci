import argparse
import shutil
import json
import os

class OperationFilter:
    def __init__(self, operations, output):
        self.operations = operations
        self.output = output

    def filter_operation(self):
        # Creating a copy of original opensearch.smithy file for altering operations.
        original = r'../model/opensearch.smithy'
        target = r'opensearch_temp.smithy'

        shutil.copyfile( original, target)

        command = 'sed "s/operations:.*$/operations: [' + self.operations +  ']/" opensearch_temp.smithy > ../model/opensearch.smithy'
        os.system(command)
        os.system('gradle build')

        # Replacing opensearch.smithy file with original content.
        shutil.copyfile( target, original)

        # Removing temporary file.
        os.remove("opensearch_temp.smithy") 

    def parse_example(openapi_data , model_data):  
        dict = {}
        # Parsing examples corresponding to operation-ids from the model json file.
        for operation in model_data['shapes'].keys():
            # Checking operation-ids in Model json file.
            if  model_data['shapes'][operation]['type']=='operation':
                if 'traits' in model_data['shapes'][operation].keys():
                    # Checking examples for operation-id
                    if 'smithy.api#examples' in model_data['shapes'][operation]['traits'].keys():
                        # Storing operation-id and examples in a dictionary.
                        dict[operation] = model_data['shapes'][operation]['traits']['smithy.api#examples']
        print(dict)
        # Checking URL endpoint in OpenAPI json file.
        for endpoint in openapi_data['paths'].keys():
            # Checking URL method in OpenAPI json file.
            for method in openapi_data['paths'][endpoint].keys():
                # Checking OperationId and title in OpenAPI json file and forming
                # operation name.
                title = openapi_data['info']['title']
                op_id = openapi_data['paths'][endpoint][method]['operationId']
                op_name = title + "#" + op_id
                if op_name in dict.keys():
                    print(op_name)
                    print(dict[op_name])
                    for example in dict[op_name]:
                        # Adding examples for Input params
                        if 'input' in example:
                            for key in example['input']:
                                for param in openapi_data['paths'][endpoint][method]['parameters']:
                                    if key == param['name']:
                                        param['example'] = example['input'][key]
                        # Adding examples for Output params
                        if 'output' in example:
                            op_out_name = op_id + 'ResponseContent'
                            if op_out_name in openapi_data['components']['schemas'].keys():
                                openapi_data['components']['schemas'][op_out_name]['example'] = example['output']   

    def file_conversion(self):
        # Coverting JSON file to yaml file.
        command = "openapi-format " + self.output + "/model.openapi.json -o " + self.output +"/model.openapi.yaml" + " --no-sort"
        os.system(command)

        # Removing temporary file.
        file_path = self.output + "/model.openapi.json"
        os.remove(file_path) 



# Parsing command line arguments:
parser = argparse.ArgumentParser()

# Operation Agrument is required to specify operation-id's to be filtered out.
parser.add_argument('--operation', type=str, required=True)
parser.add_argument('--output', type=str, required=True)
args = parser.parse_args()

# Checking values for Arguments.
obj = OperationFilter(args.operation,args.output)

# Building smithy models as per user mentioned operation.
obj.filter_operation()

# Opening OpenAPI JSON file for checking operation ID.
openapi_file_obj = open(
    ".../build/smithyprojections/opensearch-api-specification/source/openapi/OpenSearch.openapi.json",
    mode='r',
    encoding='utf-8')
openapi_data = json.load(openapi_file_obj)

# Opening Model JSON file for checking examples.
model_file_obj = open(
    "../build/smithyprojections/opensearch-api-specification/source/model/model.json",
    mode='r',
    encoding='utf-8')
model_data = json.load(model_file_obj)

# calling parse function.
obj.parse_example(openapi_data , model_data)

# Creating new JSON file for copying existing OpenAPI data and adding examples.
model_openapi_file_obj = open(
    args.output + "/model.openapi.json",
    mode='w',
    encoding='utf-8')

# Coverting python dictionary to JSON object.
json_data = json.dumps(openapi_data, indent=1)
model_openapi_file_obj.write(json_data)

# Closing all files
openapi_file_obj.close()
model_file_obj.close()
model_openapi_file_obj.close()

# Converting json to yaml file.
obj.file_conversion()


# import json
# import os

# def parse_example():  
    
#     dict = {}

#     # Parsing examples corresponding to operation-ids from the model json file.
#     for operation in model_data['shapes'].keys():
#         # Checking operation-ids in Model json file.
#         if  model_data['shapes'][operation]['type']=='operation':
#             if 'traits' in model_data['shapes'][operation].keys():
#                 # Checking examples for operation-id
#                 if 'smithy.api#examples' in model_data['shapes'][operation]['traits'].keys():
#                     # Storing operation-id and examples in a dictionary.
#                     dict[operation] = model_data['shapes'][operation]['traits']['smithy.api#examples']
#     print(dict)

#     # Checking URL endpoint in OpenAPI json file.
#     for endpoint in openapi_data['paths'].keys():
#         # Checking URL method in OpenAPI json file.
#         for method in openapi_data['paths'][endpoint].keys():
#             # Checking OperationId and title in OpenAPI json file and forming
#             # operation name.
#             title = openapi_data['info']['title']
#             op_id = openapi_data['paths'][endpoint][method]['operationId']
#             op_name = title + "#" + op_id
#             if op_name in dict.keys():
#                 print(op_name)
#                 print(dict[op_name])
#                 for example in dict[op_name]:
#                     # Adding examples for Input params
#                     if 'input' in example:
#                         for key in example['input']:
#                             for param in openapi_data['paths'][endpoint][method]['parameters']:
#                                 if key == param['name']:
#                                     param['example'] = example['input'][key]
#                     # Adding examples for Output params
#                     if 'output' in example:
#                         op_out_name = op_id + 'ResponseContent'
#                         if op_out_name in openapi_data['components']['schemas'].keys():
#                             openapi_data['components']['schemas'][op_out_name]['example'] = example['output']                

#     # # Checking URL endpoint in OpenAPI json file.
#     # for endpoint in openapi_data['paths'].keys():
#     #     # Checking URL method in OpenAPI json file.
#     #     for method in openapi_data['paths'][endpoint].keys():
#     #         # Checking OperationId and title in OpenAPI json file and forming
#     #         # operation name.
#     #         title = openapi_data['info']['title']
#     #         op_id = openapi_data['paths'][endpoint][method]['operationId']
#     #         op_name = title + "#" + op_id
#     #         # OperationName in Model json file.
#     #         if op_name in model_data['shapes'].keys():
#     #             # Checking traits exists in Model json file for a
#     #             # OperationName.
#     #             if 'traits' in model_data['shapes'][op_name].keys():
#     #                 # Checking examples exists in Model json file for a
#     #                 # OperationName.
#     #                 if 'smithy.api#examples' in model_data['shapes'][op_name]['traits'].keys():
#     #                     op_examples = model_data['shapes'][op_name]['traits']['smithy.api#examples']
#     #                     for example in op_examples:
#     #                         # Adding examples for Input params
#     #                         if 'input' in example:
#     #                             for key in example['input']:
#     #                                 for param in openapi_data['paths'][endpoint][method]['parameters']:
#     #                                     if key == param['name']:
#     #                                         param['example'] = example['input'][key]
#     #                         # Adding examples for Output params
#     #                         if 'output' in example:
#     #                             op_out_name = op_id + 'ResponseContent'
#     #                             if op_out_name in openapi_data['components']['schemas'].keys():
#     #                                 openapi_data['components']['schemas'][op_out_name]['example'] = example['output']


# # Opening OpenAPI JSON file for checking operation ID.
# openapi_file_obj = open(
#     "build/smithyprojections/testing-ci/source/openapi/OpenSearch.openapi.json",
#     mode='r',
#     encoding='utf-8')
# openapi_data = json.load(openapi_file_obj)

# # Opening Model JSON file for checking examples.
# model_file_obj = open(
#     "build/smithyprojections/testing-ci/source/model/model.json",
#     mode='r',
#     encoding='utf-8')
# model_data = json.load(model_file_obj)

# # Creating new JSON file for copying existing OpenAPI data and adding examples.
# model_openapi_file_obj = open(
#     "build/smithyprojections/testing-ci/source/openapi/model.openapi.json",
#     mode='w',
#     encoding='utf-8')

# # calling parse function.
# parse_example()

# # Coverting python dictionary to JSON object.
# json_data = json.dumps(openapi_data, indent=1)
# model_openapi_file_obj.write(json_data)

# # Closing all files
# openapi_file_obj.close()
# model_file_obj.close()
# model_openapi_file_obj.close()

# # Coverting JSON file to yaml file.
# os.system("openapi-format build/smithyprojections/testing-ci/source/openapi/model.openapi.json -o build/smithyprojections/testing-ci/source/openapi/model.openapi.yaml --no-sort")