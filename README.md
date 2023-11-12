# Real Estate 
### Group Members:
* Ngoc Duy Tran: ngocduyt@student.unimelb.edu.au

# Structure of Directory
    .  
    ├── real-estate-industry-project-open-source-industry-project-40  
    │   ├── data  
    │   │   ├── curated  
    │   │   ├── landing  
    │   │   └── raw  
    │   ├── Meeting Minutes  
    │   ├── models  
    │   │   ├── modelling.ipynb  
    │   │   └── train_test_partition  
    │   ├── notebooks  
    │   │   ├── analysis 
    │   │   ├── download 
    │   │   ├── geopandas_dependencies  
    │   │   ├── preprocessing  
    │   │   └── supporting_notebooks
    │   ├── plots  
    │   ├── scripts  
    │   │   ├── __init__.py  
    │   │   ├── download_external_factors.py  
    │   │   └── scrape.py  
    │   ├── README.md  
    │   └── requirements.txt  
    └──  

# Pipeline
In order to replicate the files, visualisations, models, etc. produced throughout this project, the following actions should be executed in the order as outlined below. Don't run any other files except these files in the pipeline.

## 1. DOWNLOADING DATA

Please first run the following files, all located within the `scripts` folder:
- `download_external_factors.py` (about 10 mins)
- `scrape.py` (this one will take a long time to run): Note that this script takes a long time to run and running this script at different time will result in different versions of scraped data because domain.com constantly updates their property listings.

For reproducibility, please just only run `download_external_factors.py` only. I have already included our scraped version in this script so that you can actually reproduce our work with same results. To run these scripts using the terminal:
`cd real-estate-industry-project-open-source-industry-project-40`
`cd scripts`
`python download_external_factors.py`

## 2. PREPROCESSING
### 2.1 Real Estate related data
- Run `notebooks/download/postcode_to_suburb.ipynb`: Note that this notebook might not work as this scrapes the ABS Census website. This notebook has been recorded not working properly one time (05/10/2023) when the server is under maintenance due to increasing volume. However, this is not our fault, it's ABS's issue. It might also take about 30 mins (on my computer) to finish.
- Run `notebooks/preprocessing/raw_real_estate.ipynb`: landing --> raw for real estate data
- Run `notebooks/preprocessing/raw_ptv_data.ipynb` (prereq for aggregate_feature notebook): landing --> raw for ptv data
- Run `notebooks/preprocessing/aggregate_feature.ipynb`: aggrgate external features for merging with real estate data
- Run `notebooks/preprocessing/real_estate_preprocessing-checkpoint.ipynb`: raw --> curated for real estate. Finished merging with external features

## 3. MODELLING
- Run `models/train_test_partition.ipynb`: train test split (80: 20)
- Run `models/modelling.ipynb`: modelling with LASSO and LightGBM. Also covers inference for 2026

## 4. VISUALISATIONS AND ANALYSIS
- Run `notebooks/analysis/preprocess_historical.ipynb`: visualizations for question 2
- Run `notebooks/analysis/question_1.ipynb`: some viz for question 1
- Run `notebooks/analysis/affordability.ipynb`: affordability calculation
- Run `notebooks/analysis/liveability.ipynb`: liveability calculation
- Run `notebooks/analysis/question_3.ipynb`: viz for question 3


## 5. SUMMARY NOTEBOOK
- The summary notebook is located under `notebooks/SUMMARY_NOTEBOOK.ipynb`. 
- In case Github couldn't display the images properly, like images do not come up, please use `SUMMARY_NOTEBOOK.pdf`, which is the pdf version of the notebook. Note that the anchor links in jupyter notebook might not work properly on Github website (due to their weird rendering process), but it works perfectly fine on the pdf file.


# NOTES
- Please do not run any other files apart from the files specified above. We'll explain below:
- The `notebooks/supporting_notebooks` acts like a supporting folder which helps us achieve the results in the above-specified folders. In other words, it acts like a playground for us to have an overview of the data and acts like an intermediate layer before we integrate the code into other folders such as preprocessing, download, ...
- This folder also contains some of the future work that we specified in the summary_notebook/future_exploration such as integrating property area as a feature. If you run wanna this, you will need to manually order and retrieve from the data.vic
- notebooks/supporting_notebooks is not part of the pipeline, so do not run this folder. Although it is irrelevant to the main pipeline specified above, I decided to keep these notebooks in case we need to continue to work on this project in the future.
- notebooks/preprocessing/income_population_projection is the previous version of notebooks/download/postcode_to_suburb.ipynb. The former is by SA2 while the latter is by postcodee, which is much smaller and better. We still decided to keep this `notebooks/preprocessing/income_population_projection` as a backup plan because the ABS Census website that the newer version is working on has been recorded to be under maintenance on 05/10/2023, which makes the newer version fail to work. Also do not run this as well because we haven't specified the order of running.


# CONTACT
- Should you have any questions during running this repo, please contact me via the emails above.