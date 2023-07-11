import pandas as pd
import google.auth
from google.cloud import firestore
import warnings
import os
warnings.filterwarnings('ignore')

current_dir = os.getcwd()
creds_path = current_dir + "/secrets/customer-moten-technologies-fe0c6072bf6a.json"
credentials, project = google.auth.load_credentials_from_file(creds_path)
db = firestore.Client(project, credentials)
df = pd.DataFrame()


ref_path = f"experiments"
ref = db.collection(ref_path)
query_ref= ref.where("gesture_contraction","==","neutral")
experiments = query_ref.get()
for exp in experiments:
    collections = db.collection('experiments').document(exp.id).collections()
    for collection in collections:
        for doc in collection.stream():
            dict_new = {"username":doc.to_dict()["username"],
                        "protocol":doc.to_dict()["exp_id"],
                        "cycle":doc.id,
                        "start":doc.to_dict()["cycle"]["start"],
                        "duration":doc.to_dict()["cycle"]["duration"]}
            df = df.append(dict_new, ignore_index=True)
df.to_csv("experiments.csv", index=False)