import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import create_task_timer_widget, mobile_display, create_task_countdown_widget2
import time
from utils import progress, comment_section, protocol_display_section, protocol_progress, save_data
from datetime import datetime
from helpers.gcp_connectors import export_firestore, export_random_doc_fs, update_array_fs
mobile_display(ratio=25) 
from utils import side_bar_display
from config import hidden_side_bar
side_bar_display(hidden=hidden_side_bar)
from media.images import *


if "authentication_status" in st.session_state \
    and st.session_state["authentication_status"] :   
    username = st.session_state["username"]
                
    if "task_cycle" not in st.session_state :
        st.session_state["task_cycle"] = {}  
    protocol_info = st.session_state["protocol_info"]
    protocol_display_section(protocol_info, section='optim') 
    protocol_id = protocol_info["protocol_id"]

    col1, col2, col3 = st.columns(3)
    col1.image(img_test_speed, width=80)
    col2.image(img_chrono, width=80)
    col3.image(img_stop, width=80)

    slot_info = st.empty()

    if "start_button" not in st.session_state:
        st.session_state["start_button"]=False
    if col3.button("cancel"):                
        st.session_state["start_button"] = False
        st.experimental_rerun()
    elif col2.button("start"):

        slot_info.info("starting in **3**")
        time.sleep(1)
        slot_info.info("starting in **2**")
        time.sleep(1)
        slot_info.info("starting in **1**")
        time.sleep(1)
        slot_info.empty() 


        st.session_state["start_button"]=True
        create_task_countdown_widget2(protocol_info)
    elif col1.button("Essai"):
        protocol_progress(rep=1,
                          contraction="isometric",
                          cycles=[],
                          sp=protocol_info["protocol_speed"], 
                          slp=5)
    st.markdown("***")
    col1, col2, col3, col4 = st.columns(4)
    if st.session_state["start_button"]==True:
        # try to put image in slot and empty it when button clicked ...
        col2.image(img_restart, width=50)
        col3.image(img_valid, width=50)
        reco = col2.button("restart") 
        done = col3.button("save")         
        if reco :
            st.session_state["start_button"] = False
            st.experimental_rerun() 

        if done :
            st.session_state["start_button"] = False
            save_data(protocol_info)
            st.session_state["protocols_list"][protocol_id]["status"] = "done"
            users_fs_ref = f"users/{st.session_state['username']}/protocols/{protocol_id}"
            export_firestore({'status':'done'}, 
                             users_fs_ref, 
                             update=True)
            switch_page("protocols_page")        

    st.markdown("****")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Back"):
            switch_page("protocol_desc_page")
    with col3:
        if st.button("Protocols"):
            switch_page("protocols_page")
else :
    st.error("You need to sign in to access this page")
    if st.button("Sign In"):
        switch_page("signin_page")   

