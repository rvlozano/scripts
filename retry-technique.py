# Technique on handling retries upon failed requests.
import time
MAX_RETRIES = 3  # Maximum number of retries
RETRY_DELAY = 5  # Delay between retries (in seconds)
retry_count = 0
while retry_count < MAX_RETRIES:
    try:
        # Your code here
        print("Hello",retry_count)
        raise ValueError('A very specific bad thing happened.')
    except Exception as e:
        time.sleep(RETRY_DELAY)  # Wait before retrying 
        retry_count += 1  # Increment retry_count
    else:
        break  # Exit the loop if no exception occurs 

Hello 0
Hello 1
Hello 2 
