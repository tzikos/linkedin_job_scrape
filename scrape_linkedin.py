import subprocess
import os

os.environ["KEYWORDS"] = input('Search for: ')
os.environ["LOCATION"] = input('Location: ')

subprocess.run(["python", 'get_proxies.py'])

subprocess.run(["python", 'check_proxies.py'])

subprocess.run(["python", "get_job_ids.py"])

subprocess.run(["python", "get_job_data.py"])

subprocess.run(["python", "data_for_gdrive.py"])

subprocess.run(["python", "push_to_gdrive.py"])