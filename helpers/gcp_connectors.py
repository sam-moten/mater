import pygsheets
from google.cloud import bigquery
from google.cloud import storage 
from google.cloud import firestore
from google.cloud import pubsub_v1
import json
import os
import google.auth
from jinja2 import Environment, FileSystemLoader
import pandas as pd

current_dir = os.getcwd()

scopes = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/bigquery",
    "https://www.googleapis.com/auth/spreadsheets"
]


default_creds_path = current_dir + "/secrets/moten-consulting-dev-a53884c8e28c.json"
credentials, project = google.auth.load_credentials_from_file(default_creds_path, scopes)


# change creds once new gcp project created ...
fs_creds_path = current_dir + "/secrets/customer-moten-technologies-fe0c6072bf6a.json"
fs_credentials, fs_project = google.auth.load_credentials_from_file(fs_creds_path)
db = firestore.Client(fs_project, fs_credentials)


def pubsub_publisher(msg, topic_name):  
    # put credentials var ...
    publisher = pubsub_v1.PublisherClient(credentials=credentials)
    try:
        topic_path = publisher.topic_path(project, topic_name)
        message_json = json.dumps(msg)        
        message_bytes = message_json.encode('utf-8')
        publish_future = publisher.publish(topic_path, data=message_bytes)
        publish_future.result()  
        # add logger ..
        return f'Message published. {msg}'
    except Exception as e:
        print(e)
        # add logger ..
        return f'Message IS NOT published. {msg}'


def get_users(ref_path):
    ref = db.collection(ref_path)
    docs = ref.get()
    users = []
    for doc in docs :
        users.append(doc.id)
    return users
    
    
def get_user_info(username):
    #maybe with filters after addinf username field ...
    ref = db.collection("users").document(username)
    doc = ref.get()
    if doc.exists:
        return doc.to_dict()
    else :
        return {}   

def fetch_activities(ref_path):
    ref = db.collection(ref_path)
    docs = ref.stream()
    activities_list = {}
    for doc in docs:
        activities_list[doc.id] = doc.to_dict()
    return activities_list


def update_array_fs(ref_path, filed, data): 
    ref = db.document(ref_path)
    ref.update({filed: firestore.ArrayUnion([data])})


    
def fetch_stats(ref_path, version="sami-v0"):
    ref = db.collection(ref_path)
    dones = ref.where("protocol_owner","==",version)\
                    .where("status","==","done").get()
    undones= ref.where("protocol_owner","==",version)\
                    .where("status","==","undone").get()
    return len(undones) , len(dones)


def fetch_undone_protocol(ref_path,filters, limit=10):
    ref = db.collection(ref_path)

    if filters["noise"] :
        query_ref= ref.where("status","==","undone").\
                        where("protocol_weight","<=",filters["weight_range"][1]).\
                            where("protocol_weight",">=",filters["weight_range"][0]).\
                                where("gesture_contraction", "in", ["dynamic", "isometric"])
    #else :
    #    query_ref= ref.where("status","==","undone").\
    #                    where("protocol_weight","<=",filters["weight_range"][1]).\
    #                        where("protocol_weight",">=",filters["weight_range"][0]).\
    #                            where("gesture_contraction","in",["dynamic", "isometric"]).\
    #                               where("protocol_noise_intensity","==","no clothes")
    
    if filters["gyro"]==True:
        query_ref= ref.where("gesture_contraction","==","neutral")
        
    # create componud index

    docs = query_ref.get()
    protocols_list = {}
    for i, doc in enumerate(docs):
        protocols_list[str(i)] = doc.to_dict()
   
    df = pd.DataFrame.from_dict(protocols_list,orient="index")
    
    #### for demo
    #df = df.query("protocol_name=='flexion coude'")
    #### end 
    
    res = {}
    
    if len(df)>0 :
        limit = min(limit,len(df))
        df.sort_values(by=['articulation_name',
                           'gesture_type',
                           'protocol_weight',
                           'protocol_speed',
                           'protocol_noise',
                           'protocol_noise_intensity'],inplace=True)
        res = df.sample(limit).set_index('protocol_id').T.to_dict('dict')
        
    return res


def get_last_doc(ref_path, field):
    ref = db.collection(ref_path)
    docs_query = ref.order_by(field,direction=firestore.Query.DESCENDING).limit(1)
    last_doc_id = docs_query.get()[0].id 
    return last_doc_id


def export_random_doc_fs(ref_path, data):
    db.collection(ref_path).add(data)

def export_firestore(data, ref_path, update=True):
    """
    """
    db.document(ref_path).set(data,merge=update)

def find_sheet(sh, sheet_name):
    """
        to be deleted
    """
    i = 0
    out = False
    while i < len(sh.worksheets()) and out==False:
        if sh.worksheets()[i].title==sheet_name :
            index = sh.worksheets()[i].index
            out = True
        else :
            i += 1
    return sh[index]


def export_sheet(df, spreadsheet, sheet_name, append=False):
    """
    add logger
    catch exception
    """
    gc = pygsheets.authorize(service_account_file=default_creds_path,
                             scopes=scopes)
    sh = gc.open(spreadsheet)
    wks = sh.worksheet_by_title(sheet_name) 
    if append :
        for i in range(len(df)):
            values = df.values[i].tolist()
            wks.append_table(values=values, 
                             start="A1",
                             dimension="rows", 
                             overwrite=False)
    else :
        wks.set_dataframe(df,(1,1))
        
        
def read_sheet(spreadsheet, sheet_name):
    """
    add logger
    catch exception
    """
    gc = pygsheets.authorize(service_account_file=default_creds_path,
                             scopes=scopes)
    sh = gc.open(spreadsheet)
    wks = sh.worksheet_by_title(sheet_name)
    df = wks.get_as_df()
    return df


def execute_bigquery(query):
    query_job = bigquery.Client(credentials=credentials).query(query)
    results = query_job.to_dataframe()
    return results

def execute_bigquery_pd(query):
    """
    execute bq job on prod env
    to be deleted once all connectors are merged in the same project
    """
    query_job = bigquery.Client(credentials=fs_credentials).query(query)
    results = query_job.to_dataframe()
    return results


def query_render(query_name, params):
    env = Environment(loader=FileSystemLoader("queries/"))
    template = env.get_template(name=query_name)
    return template.render(params)

def upload_to_bucket(blob_name, path_to_file, bucket_name):
    
    bucket = storage.Client(credentials=credentials).get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(path_to_file)