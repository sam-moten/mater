import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from datetime import date, datetime
from utils import mobile_display, progress
from config import spreadsheet, user_sheet, user_protocols_sheet, topic_name
from helpers.gcp_connectors import export_sheet, pubsub_publisher, export_firestore
import pandas as pd
import time
mobile_display()
from utils import side_bar_display
from config import hidden_side_bar
side_bar_display(hidden=hidden_side_bar)
from media.images import *




#process when updating widget :
# create widget with session state input as default value
# update session_state["user_info"] in userform and setting pages
# update firestore data

st.subheader("User information")
st.info("User info can be **updated** in the app settings")
if ("authentication_status" in st.session_state \
    and st.session_state["authentication_status"]) \
        or "new_username" in st.session_state :
    if st.session_state["authentication_status"] \
        and "user_info" in st.session_state \
            and st.session_state["username"]==st.session_state["user_info"]["username"]  :
        #logger old user
        pass
    else:
        #logger new user
        st.session_state["user_info"] = {"born" : "1991-06-21", 
                                         "sex" : ['Male', 'Female'], 
                                         "activity": ['Low (< 1h)','Medium (1-3h)','High (> 3h)'],
                                         "weight":0, 
                                         "bicep_size_nc":0,
                                         "bicep_size_c":0,
                                         "forearm_size":0,
                                         "comment":""}
    with st.form(key='my_form'):
        date_birthday = st.date_input("Birthday",
                                      datetime.strptime(st.session_state["user_info"]["born"],
                                                        "%Y-%m-%d"))
        col1, col2 = st.columns(2)
        with col1:
            sex = st.radio("Sex",tuple(st.session_state["user_info"]["sex"]))
        with col2:
            activity = st.radio("Sport activity / week",tuple(st.session_state["user_info"]["activity"]))
        weight = st.slider(label='Weight (kg)', 
                           min_value=0, 
                           max_value=150,
                           value=st.session_state["user_info"]["weight"])
        col1, col2 = st.columns(2)

        
        bicep_size_nc = col1.slider(label='Bicep (no contraction)', 
                           min_value=10, 
                           max_value=60,
                           value=st.session_state["user_info"]["bicep_size_nc"],
                           help="User can always update infos in the app settings")
        col2.image(img_bicep_size_nc, width=120)
        
        bicep_size_c = col1.slider(label='Bicep (with contraction)', 
                           min_value=10, 
                           max_value=60,
                           value=st.session_state["user_info"]["bicep_size_c"],
                           help="User can always update infos in the app settings")
        col2.image(img_bicep_size_c, width=120) 
        
        forearm_size = col1.slider(label='Forearm size (cm)', 
                           min_value=10, 
                           max_value=60,
                           value=st.session_state["user_info"]["forearm_size"],
                           help="User can always update infos in the app settings")
        col2.image(img_forearm_size, width=120)
        
        comment = st.text_area("Comment",value=st.session_state["user_info"]["comment"])
        

        submit_button = st.form_submit_button(label='Submit')
        st.warning('Please click submit to finish registration')
        if submit_button:
            user_info = {"born" : date_birthday.strftime("%Y-%m-%d"),
                        "sex" : sex,
                        "activity": activity,
                        "weight":weight,
                        "bicep_size_nc":bicep_size_nc,
                        "bicep_size_c":bicep_size_c,
                        "forearm_size":forearm_size,
                        "updated_at":time.time(),
                        "comment":comment}
            bar_slot = st.empty()            
            if "authentication_status" in st.session_state \
                and st.session_state["authentication_status"] : 
                users_fs_path = f"users/{st.session_state['username']}"
                export_firestore(user_info, users_fs_path, update=True)
                progress(bar_slot, sleep=0.01)
                st.success(f'User information has been succesfully updated ')
                switch_page("setting_page")    
            elif "new_username" in st.session_state :
                user_info["username"] = st.session_state["new_username"]
                users_fs_path = f"users/{st.session_state['new_username']}"
                export_firestore(user_info, users_fs_path, update=True)
                pubsub_publisher({"username":st.session_state['new_username']},topic_name)
                progress(bar_slot, sleep=0.01)
                st.success(f"User {st.session_state['new_username']} has been succesfully regitred")
                st.session_state["authentication_status"] = True
                st.session_state["username"] = st.session_state["new_username"]
                switch_page("menu_page")
else :
    st.error("You need to sign up to access this page")
    if st.button("Sign Up"):
        switch_page("signup_page")
