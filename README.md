# Streamsets scripts
Miscellaneous Scripts.

## Disclaimer
All scripts listed here are for non-production and for demonstration purposes only. There are no guarantees with these scripts. Use at your own risk. Please Read codes for what functionalities they will do.

--- 
# Descriptions:

### dc_rest_api_demo.py 
```
$ python3 dc_rest_api_demo.py 
date: 2022-02-04 20:57:36.208062

===== Printing Duplicate Job List Report =====
['https://localhost:18632', 'userThree - testPipeline Dev2Trash__96f3928f-edf2-4fad-b485-c643cd7f5756__dpmclient.dp', 'RUNNING']
['https://localhost:18634', 'userThree - testPipeline Dev2Trash__96f3928f-edf2-4fad-b485-c643cd7f5756__dpmclient.dp', 'RUNNING']

===== Printing SCH Report =====
96f3928f-edf2-4fad-b485-c643cd7f5756:dpmclient.dp userThree@dpmclient.dp GREEN ACTIVE
6f643b17-135a-4a19-b01f-b8725ebda5f6:dpmclient.dp userOne@dpmclient.dp GRAY INACTIVE
a695efbe-b2b7-400b-98c4-a95db019c2ff:dpmclient.dp userOne@dpmclient.dp GRAY INACTIVE
3f43e92b-e1b9-4bc2-a2d6-b14784acae23:dpmclient.dp userTwo@dpmclient.dp GRAY INACTIVE
fffc8680-2093-4faa-aa88-92af1de1968f:dpmclient.dp userTwo@dpmclient.dp GRAY INACTIVE
20846f03-e368-4052-b1fc-13feae7d010d:dpmclient.dp userTwo@dpmclient.dp GRAY INACTIVE
c13a167b-4c21-4a34-8aba-0c0409bebcce:dpmclient.dp userTwo@dpmclient.dp GRAY INACTIVE
00c1b518-cf0f-4a98-8571-51b32a6f12e2:dpmclient.dp userOne@dpmclient.dp GRAY INACTIVE
74ca1ae4-d584-4002-a734-6a6da6656b0d:dpmclient.dp userOne@dpmclient.dp GRAY INACTIVE
bb254d5f-c129-49cf-8a45-0703fafed2b0:dpmclient.dp userOne@dpmclient.dp RED INACTIVE
da4d25d4-68fd-40f0-8e68-3112b972d26f:dpmclient.dp userOne@dpmclient.dp GRAY INACTIVE
07412b77-1df1-4b1c-88c0-527870a9f55c:dpmclient.dp userTwo@dpmclient.dp GRAY INACTIVE
73dcea51-e899-4cb9-a0d2-28a6263008aa:dpmclient.dp userTwo@dpmclient.dp RED INACTIVE
e610b8d8-bbca-4f3d-82c3-b06af5136b00:dpmclient.dp userTwo@dpmclient.dp RED INACTIVE
ee93bd24-0b6a-4cd3-84a4-67eb78328a60:dpmclient.dp userTwo@dpmclient.dp GRAY INACTIVE
725c161d-39b8-41d4-b8cb-41c0d8e36707:dpmclient.dp userTwo@dpmclient.dp GRAY INACTIVE
65bceee8-bac3-483a-8963-4ba454493dc8:dpmclient.dp userOne@dpmclient.dp GRAY INACTIVE
```


---
### filesopend.sh
BASH Script to periodicly check available files that are available using ulimit..

```
$ lsof -p 95609 > /tmp/during_event_file_descriptors.txt
$ jstack 95609 > /tmp/during_event_threaddump.txt
$ ulimit -Hn
$ ulimit -Sn

$ /tmp/filesopend.sh -p 95609 -t 1 -f /tmp/output
$ cat /tmp/output 
2023-01-06 14:10:15 1113484
2023-01-06 14:14:13 1113483
2023-01-06 14:15:07 1113484
2023-01-06 14:15:17 1113484
2023-01-06 14:17:00 1113482
2023-01-06 14:18:01 1113484
```
