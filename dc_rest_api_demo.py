###
# Builds a Job Report Identifying duplicates jobs and list all job statuses from SCH.
###
import json
import datetime
import requests
import os
import warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

cmd =f'cat ./cookie.txt | grep SSO | rev | grep -o \'^\S*\' | rev'
session_token=os.popen(cmd).read() 

headers = {}
headers['content-type']='application/json'
headers['X-Requested-By']='SDC'
headers['X-SS-REST-CALL']='true'
headers['X-SS-User-Auth-Token'] = session_token.strip()

# Add all your Datacollectors here
dc_list=[]
dc_list.append("https://localhost:18632")
dc_list.append("https://localhost:18634")

arr=[]
try:
    for dc in dc_list:
        restcmd="/rest/v1/pipelines/status"
        response = requests.get(dc+restcmd,headers=headers,verify=False)
        json_txt=response.json()
        for i in json_txt:
            one=(json_txt[i]['pipelineId'])
            two=(json_txt[i]['status'])
            arr.append([dc,one,two])
    
    duplicates=[]
    seen=[]
    for i in arr:
        if seen.count(i[1]) >= 1:
            duplicates.append(i[1])
        else:
            seen.append(i[1])

    duplist=[]
    for i in arr:
        if (i[1] in duplicates):
            duplist.append(i)
    
    ct = datetime.datetime.now()
    print('date:',ct)
    if len(duplist) > 1:
        print('\n\n===== Printing Duplicate Job List Report =====')
        for i in duplist:
            print(i)
    else:
        print('no duplicates found')

    # Example to Stop a Job via rest api
    #print(arr[1][0])
    #restcmd="/rest/v1/pipeline/" + arr[1][0] + "/stop?rev=0"
    #print(restcmd)
    #res=requests.post(url+rcmd,headers=headers,verify=False)

    # Build SCH Job Report:
    # curl -k -X GET https://cloud.streamsets.com/jobrunner/rest/v1/jobs 
    # --header "Content-Type:application/json" --header "X-Requested-By:SDC" --header "X-SS-REST-CALL:true" --header "X-SS-User-Auth-Token:$sessionToken" -i
    sch_response=requests.get('https://cloud.streamsets.com/jobrunner/rest/v1/jobs',headers=headers,verify=False)
    schresp=sch_response.json()
    
    arr=[]
    json_txt=sch_response.json()[0]
    for i in sch_response.json():
        #print(i['pipelineId'])
        #one=(i['name'])
        one=(i['pipelineId'])
        two=(i['currentJobStatus'])
        #for j in i['currentJobStatus'][0]:
        #    print(j)
        if two!=None:
            arr.append(two)
        #three=(i['labels'])
        #four=(i['numInstances'])
        #arr.append([one,two])

    # Print Report for SCH
    print('\n\n===== Printing SCH Report =====')

    for i in arr:
        if i['color']=='GREEN' or i['status']=='INACTIVE':
            print(i['jobId'],i['user'],i['color'],i['status'])

except Exception as e:
    pass
