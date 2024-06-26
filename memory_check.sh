# Checks memory, if greater than threshold
# it will log to file Data and ProcessList.
# Should add to cron job.

total=$(free | grep Mem: | awk '{print $2}')
used=$(free | grep Mem: | awk '{print $3}')

percent=$(echo "print(int(($used/$total)*100))" | python3) # Uses Python3
# percent=$(echo "scale=2; ($used / $total) * 100" | bc)   # Uses BC most linux distros have this by default

if [[ $percent > 95 ]]
then
	echo $(date) $(free) >> /tmp/checkmem.log
	echo "$(ps -o pid,user,%mem,command ax | sort -b -k3 -r)" >> /tmp/checkmem.log
fi
