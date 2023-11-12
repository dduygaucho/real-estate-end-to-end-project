import requests
import subprocess
import zipfile
import urllib.request
from urllib.request import urlretrieve
import os
import shutil
import urllib

LANDING_RELATIVE_DIR = '../data/landing/'

# # Check if landing data folder exists
# if not os.path.exists(LANDING_RELATIVE_DIR):
#     os.makedirs(LANDING_RELATIVE_DIR)

opener = urllib.request.URLopener()
opener.addheader('User-Agent', 'Mozilla/5.0')

# #--------------------------DOWNLOAD EXTERNAL FEATURES-------------------------

# #-----------------------------download schools data---------------------------
# Output directory path
output_relative_dir = LANDING_RELATIVE_DIR + 'schools/'

# Check if path exists
if not os.path.exists(output_relative_dir):
    os.makedirs(output_relative_dir)
    
url = ("https://discover.data.vic.gov.au/datastore/dump/97c05fd1-8671-4f0a-"
       "9f91-e8d57a1c1135?q=&plain=False&languagesimple&sort=_id+asc&filters="
       "%7B%7D&format=csv&fields=_id%2CEducation_Sector%2CEntity_Type%2"
       "CSCHOOL_NO%2CSchool_Name%2CSchool_Type%2CSchool_Status%2CAddress_Line_1"
       "%2CAddress_Line_2%2CAddress_Town%2CAddress_State%2CAddress_Postcode%2C"
       "Postal_Address_Line_1%2CPostal_Address_Line_2%2CPostal_Town%2CPostal_"
       "State%2CPostal_Postcode%2CFull_Phone_No%2CLGA_ID%2CLGA_Name%2CX%2CY")

output_dir = f"{output_relative_dir}dv309_schoollocations2021.csv"
urlretrieve(url, output_dir) 

#-----------------------------download ptv data---------------------------------
# In GTFS zip folder, we need to keep folders 1-6
# 1: Regional Trains
# 2: Metro Trains
# 3: Metro Trams
# 4: Metro Buses
# 5: Regional Coaches
# 6: Regional Buses

# Define variables
LANDING_DATA_DIR_PTV = LANDING_RELATIVE_DIR + "ptv"

url = "https://data.ptv.vic.gov.au/downloads/gtfs.zip"
output_dir = f"{LANDING_DATA_DIR_PTV}/gtfs.zip"

folders_keep = ["1", "2", "3", "4", "5", "6"]
folders_del = ["7", "8", "10", "11"]

folders_keep_rename = {"1": "reg_trains", "2": "metro_trains", 
                        "3": "metro_trams", "4": "metro_buses", 
                        "5": "reg_coaches", "6": "reg_buses"}

# Create `ptv` folder if doesn't exist
if not (os.path.exists(LANDING_DATA_DIR_PTV)):
    print("folder does not exist")
    os.makedirs(LANDING_DATA_DIR_PTV)
    print("folder created!")

# Download relevant folders from within largest zip folder
urlretrieve(url, output_dir)

with zipfile.ZipFile(output_dir, 'r') as zip_ref:
    zip_ref.extractall(LANDING_DATA_DIR_PTV)

os.remove(output_dir)

for folder in folders_del:
    shutil.rmtree(f"{LANDING_DATA_DIR_PTV}/{folder}")

# Extract files from within sub zip folders
for folder in folders_keep:

    # Make new folder
    new_folder = folders_keep_rename[folder]

    # Extract files in sub zip folder into new folder
    with zipfile.ZipFile(
        f"{LANDING_DATA_DIR_PTV}/{folder}/google_transit.zip", 'r'
    ) as zip_ref:
        zip_ref.extractall(f"{LANDING_DATA_DIR_PTV}/{new_folder}")

    shutil.rmtree(f"{LANDING_DATA_DIR_PTV}/{folder}")

#----------------------------download crime data--------------------------------
CRIME_DATA_URL = ("https://files.crimestatistics.vic.gov.au/2023-06/Data_"
                  "Tables_LGA_Recorded_Offences_Year_Ending_March_2023.xlsx")
output_dir = f"{LANDING_RELATIVE_DIR}crime_data.xlsx"

urlretrieve(CRIME_DATA_URL, output_dir) 

#--------------------------download healthcare data-----------------------------
HEALTHCARE_DATA_URL = ("https://www.healthcollect.vic.gov.au/HospitalLists/"
                       "ExportList.aspx?List=MainHospitalList")
output_dir = f"{LANDING_RELATIVE_DIR}healthcare_data.csv"
urlretrieve(HEALTHCARE_DATA_URL, output_dir) 

#--------------------------download population data-----------------------------
shape_link = ("https://www.abs.gov.au/statistics/people/population/regional"
              "-population/2021-22/32180DS0003_2001-22.xlsx")

# Local directory where you want to save the downloaded zip file
local_dir = LANDING_RELATIVE_DIR + "population.xlsx"

# Download the zip file using wget
subprocess.run(["wget", shape_link, "-O", local_dir])

#------------------------download historical income data------------------------
# URL
url = ("https://www.abs.gov.au/statistics/labour/"
       "earnings-and-working-conditions/personal-income-australia/"
       "2015-16-2019-20/6524055002_DO001.xlsx")

print("HISTORICAL")
file_path = f"{LANDING_RELATIVE_DIR}/historical_income_data.xlsx"
filename, headers = opener.retrieve(url, file_path)

# # Send an HTTP GET request
# response = requests.get(url)

# # Check if the request was successful
# if response.status_code == 200:
    
#     # Save
#     with open(file_path, "wb") as file:
#         file.write(response.content)
    
#------------------------------download income data-----------------------------
url = ("https://www.abs.gov.au/statistics/labour/earnings-and-working-"
       "conditions/personal-income-australia/2015-16-2019-20/"
       "6524055002_DO002.xlsx")
file_path = '../data/landing/income_data'
print("INCOME")
filename, headers = opener.retrieve(url, file_path)

# # Send an HTTP GET request
# response = requests.get(url)

# # Check if the request was successful
# if response.status_code == 200:
    
#     # Save
#     with open(file_path, "wb") as file:
#         file.write(response.content)
        
#------------------------DOWNLOAD GEOGRAPHY-RELATED FILES-----------------------

#----------------------------download district data-----------------------------
shape_link = ("https://www.abs.gov.au/statistics/standards/australian"
              "-statistical-geography-standard-asgs-edition-3/jul2021-"
              "jun2026/access-and-downloads/digital-boundary-files/"
              "SA2_2021_AUST_SHP_GDA2020.zip")
local_dir = f"{LANDING_RELATIVE_DIR}district_locations"
zip_file_path = f"{local_dir}/SA2_2021_AUST_SHP_GDA2020.zip"

# Ensure the directory exists or create it if it doesn't
os.makedirs(local_dir, exist_ok=True)

# Download the zip file using wget
subprocess.run(["wget", shape_link, "-P", local_dir])

# Extract contents contents in zipped folder
try:
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(local_dir)   
except Exception as e:
    print(f"An error occurred while extracting the zip file: {e}")

# Remove the zip file
os.remove(zip_file_path)

#------------------------------download vic map---------------------------------
url = ("https://data.gov.au/data/dataset/af33dd8c-0534-4e18-9245-fc64440f742e"
       "/resource/4494abe0-64ea-4fa6-931a-d1a389a14e57/download/"
       "vic_loc_gda2020.zip")
output_dir = f"{LANDING_RELATIVE_DIR}vic_loc_gda20.zip"

# Download relevant folders from within largest zip folder
urlretrieve(url, output_dir)

with zipfile.ZipFile(output_dir, 'r') as zip_ref:
    zip_ref.extractall(LANDING_RELATIVE_DIR)

os.remove(output_dir)

# Move all files out of folder `GDA2020`
all_files = os.listdir(f"{LANDING_RELATIVE_DIR}GDA2020")

for file in all_files:
    source_path = os.path.join(f"{LANDING_RELATIVE_DIR}GDA2020", file)
    dest_path = os.path.join(f"{LANDING_RELATIVE_DIR}", file)
    shutil.move(source_path, dest_path)
    
shutil.rmtree(f"{LANDING_RELATIVE_DIR}GDA2020")

#---------------------------download suburb data--------------------------------
shape_link = ("https://data.gov.au/data/dataset/af33dd8c-0534-4e18-9245"
              "-fc64440f742e/resource/4494abe0-64ea-4fa6-931a-d1a389a14e57/"
              "download/vic_loc_gda2020.zip")
zip_file_path = f"{LANDING_RELATIVE_DIR}vic_loc_gda2020.zip"

# Download the zip file using wget
subprocess.run(["wget", shape_link, "-P", LANDING_RELATIVE_DIR])

# Extract contents of zip folder
try:
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(LANDING_RELATIVE_DIR)
except Exception as e:
    print(f"An error occurred while extracting the zip file: {e}")

# Remove the zip file
os.remove(zip_file_path)

#-----------------------download sa2 to suburb mapping data---------------------
url = ("https://communityinsightaustralia.org/wp-content/uploads/"
                   "2020/06/list-of-sa2s-showing-which-sa3-they-lie-in.xlsx")
output_dir = f"{LANDING_RELATIVE_DIR}sa2_mapping.xlsx"

filename, headers = opener.retrieve(url, output_dir)

#-----------------------download postcode mapping data--------------------------
url = ("https://www.matthewproctor.com/Content/postcodes/"
                     "australian_postcodes.xlsx")
output_dir = f"{LANDING_RELATIVE_DIR}postcode_mapping.csv"

filename, headers = opener.retrieve(url, output_dir)

#---------------------------download openspace data-----------------------------
shape_link = ("https://opendata.arcgis.com/datasets/"
              "da1c06e3ab6948fcb56de4bb3c722449_0.zip")
local_dir = LANDING_RELATIVE_DIR + "openspace_locations"
zip_file_path = f"{local_dir}/da1c06e3ab6948fcb56de4bb3c722449_0.zip"

# Ensure the directory exists or create it if it doesn't
os.makedirs(local_dir, exist_ok=True)

# Download the zip file using wget
subprocess.run(["wget", shape_link, "-P", local_dir])

# Extract contents of zip folder
try:
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(local_dir)
except Exception as e:
    print(f"An error occurred while extracting the zip file: {e}")

# remove the zip file
os.remove(zip_file_path)

#---------------------------download apm data-----------------------------------
# this dataset is not publicly available, and require consent to acquire 
# this dataset. Upload to github for automatic download purposes
apm_link = ("https://media.githubusercontent.com/media/dduygaucho/"
            "PRSA/main/apm-restricted-vic-apm-point-for-rent-vic-na.csv")

local_dir = f"{LANDING_RELATIVE_DIR}historical_data"
output_dir = f"{local_dir}/apm-restricted-vic-apm-point-for-rent-vic-na.csv"
os.makedirs(local_dir, exist_ok=True)

filename, headers = opener.retrieve(apm_link, output_dir)

#---------------------------download scraped data-------------------------------
# this dataset is not publicly available, and require consent to acquire 
# this dataset. Upload to github for automatic download purposes
domain_link = ("https://media.githubusercontent.com/media/dduygaucho/"
            "PRSA/main/domain_scraped_data%20(1).csv")

output_dir = f"{LANDING_RELATIVE_DIR}/domain_scraped_data (1).csv"

filename, headers = opener.retrieve(domain_link, output_dir)