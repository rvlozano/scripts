# SDC Log Summary Report for Saleforce Stage

## Report Analysis:
```bash
$ grep "4444K00000NLAmkQAH" sdc.log.2023-03-29-09 | grep "INFO  ForceBulkReader - Waiting" | head -1
2023-03-29 09:06:38,336 [user:*edh_cdl_prod_svc@bsci.com] [pipeline:PIPELINENAME] [runner:] [thread:PIPELINENAME] [stage:] INFO  ForceBulkReader - Waiting 2000 milliseconds for job 4444K00000NLAmkQAH

$ grep "4444K00000NLAmkQAH" sdc.log.2023-03-29-09 | grep "INFO  ForceBulkReader - Waiting" | tail -1
2023-03-29 09:09:23,993 [user:*edh_cdl_prod_svc@bsci.com] [pipeline:PIPELINENAME [runner:] [thread:PIPELINENAME] [stage:] INFO  ForceBulkReader - Waiting 2000 milliseconds for job 4444K00000NLAmkQAH
```

## Pseudo Code
I want to query the first instance waiting and last instance waiting for a particular .</br>
```
Get all job IDs. for waiting.  
for loop thru all IDS.
	get begining 
	get end
```

## Build report.

```
rm waiting.txt joblist.txt report.txt
grep "INFO  ForceBulkReader - Waiting .* milliseconds for job " sdc.log.* > waiting.txt
grep -o "job.*" waiting.txt | awk '{ print $2 }' | sort | uniq > joblist.txt

for jobid in $(cat joblist.txt)
do
    echo $jobid
    begin=$(grep --no-f $jobid sdc.log.* | grep "Waiting" | awk '{ print $2 }' | sort | head -1)
    end=$(grep --no-f $jobid sdc.log.* | grep "Waiting" | awk '{ print $2 }' | sort | tail -1)
    echo $jobid $begin $end>> report.txt
done
```

# Example output
```
FORCEJOBID          found_first   found_last
7502K00000TGFE5QAP, 09:04:53,138, 09:07:20,019
7502K00000TGFh1QAH, 09:18:21,354, 09:19:22,425
7502K00000TGFlgQAH, 09:06:38,336, 09:09:23,993
7502K00000TGFptQAH, 09:03:36,864, 09:11:51,559
7502K00000TGFzEQAX, 09:22:44,747, 09:26:21,057
7502K00000TGG14QAH, 09:03:56,601, 09:05:16,260
7502K00000TGG3tQAH, 09:03:23,881, 09:05:07,54
...
...
```
