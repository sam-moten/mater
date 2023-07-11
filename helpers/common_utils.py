import pandas as pd
import re 

def mail_exist(config, mail):
    data = list(config["credentials"]["usernames"].values())
    df = pd.DataFrame.from_records(data)
    if df.email.value_counts()[mail]>1:
        return True
    else :
        return False
    

def reorder_list(lst, elt, pos):
    if len(lst)>=pos:
        lst.remove(elt)
        lst.insert(pos, elt)
        return lst
    else:
        print("position out of list lenght")
        
        
def mail_valid(email): 
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' 
    
    if(re.fullmatch(regex, email)):  
        return True
    else:   
        return False