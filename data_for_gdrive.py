import gdown
import pandas as pd
import os

url = 'https://drive.google.com/uc?id=1yt81JE3_4bXd45mRoiDbEmsWhcxfyLCB'
output = '/Users/tzikos/Desktop/python tasks/linkedin_job_scrape/expo/FOR_GOOGLE_DRIVE/Data.csv'
gdown.download(url, output, quiet=False)

def latest_file_in_folder(folder_path='/Users/tzikos/Desktop/python tasks/linkedin_job_scrape/expo/csv'):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)
    # Filter out directories, if any
    files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
    if not files:
        return None  # No files in the folder

    # Get the latest created file based on creation time
    latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(folder_path, f)))
    return '/Users/tzikos/Desktop/python tasks/linkedin_job_scrape/expo/csv/'+latest_file

downloaded_df = pd.read_csv('/Users/tzikos/Desktop/python tasks/linkedin_job_scrape/expo/FOR_GOOGLE_DRIVE/Data.csv')
new_data = pd.read_csv(latest_file_in_folder())

new_df = pd.concat([downloaded_df,new_data],axis=0)

new_df.to_csv('/Users/tzikos/Desktop/python tasks/linkedin_job_scrape/expo/FOR_GOOGLE_DRIVE/DATA_FOR_GDRIVE.csv',index=False,header=True,encoding='utf-8')