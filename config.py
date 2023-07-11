import os
import logging

# set ENV variable : "prod" vs "dev"
ENV = "prod"


if ENV=="dev":
    hidden_side_bar = False
elif ENV=="prod" :
    hidden_side_bar = True 

CWD = os.getcwd()

# set logging level by ENV variable
LOGLEVEL = logging.INFO


#project_id = os.getenv("PROJECT_ID")
spreadsheet = "DOE"
user_sheet = "users"
user_protocols_sheet = "user_protocols"
exp_sheet = "experiments"
topic_name = "new_user_pbsb"
bucket_name = "moten-protocols"


min_sensor = 1