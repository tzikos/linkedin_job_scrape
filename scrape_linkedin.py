import subprocess
import os

os.environ["KEYWORDS"] = input('Search for: ')
os.environ["LOCATION"] = input('Location: ')

# Execute Script 1
subprocess.run(["python", "get_job_ids.py"])

# Execute Script 2
subprocess.run(["python", "get_job_data.py"])
