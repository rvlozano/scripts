###
# Written by: rlozano@streamsets.com
# Description: Builds a Report from SCH-APPS API output json.
# Example: http://SCH_URL:SCHPORT/security/rest/v1/organization/admin/components?componentTypeId=dpm-system&orderBy=ID
###

import json
import datetime

json_file_path = './apiresponse.json'

with open(json_file_path) as file:
    data = json.load(file)

def convert_epoch(epoch_time):
    converted_time = datetime.datetime.utcfromtimestamp(int(epoch_time) / 1000)
    formatted_time = converted_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

record_list = []
for item in data:
    if 'scheduler' in item['id']:
        record = [
            convert_epoch(str(item['authTokenGeneratedOn'])),
            item['id'],
            #convert_epoch(str(item['registeredOn'])),
            #item['type'],
            #convert_epoch(str(item['lastValidatedOn'])),
            #convert_epoch(str(item['attributesUpdatedOn'])),
            item['attributes']['baseHttpUrl']
        ]
        record_list.append(', '.join(record))
    print('\n'.join(record_list))


