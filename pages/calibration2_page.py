import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import mobile_display, progress
from helpers.gcp_connectors import upload_to_bucket
from datetime import datetime
mobile_display()
import time
from utils import side_bar_display
from config import hidden_side_bar, bucket_name
side_bar_display(hidden=hidden_side_bar)
from media.images import *

if "authentication_status" in st.session_state and st.session_state["authentication_status"]:
    
    if "cam_button" not in st.session_state: 
        st.session_state["cam_button"] = False
    
    st.subheader("Posture Calibration") 
    st.info("**Step 1** : Put your back on the **wall**  \n**Step 2** : Maintain the pose for **5 secondes**")
    col1, col2 = st.columns(2)
    col1.image(img_pose1, width=160)
    col2.image(img_pose2, width=160)
    
    col1, col2, col3 = st.columns(3)
    start_button = col2.button("start")
    slot = st.empty()
    if start_button:
        slot.info("starting in **5**")
        time.sleep(1)
        slot.info("starting in **4**")
        time.sleep(1)
        slot.info("starting in **3**")
        time.sleep(1)
        slot.info("starting in **2**")
        time.sleep(1)
        slot.info("starting in **1**")
        time.sleep(1)
        slot.empty()
        start = datetime.now()
        bar_slot = st.empty()
        progress(bar_slot, sleep=0.05, speed=10)
        end = datetime.now()
        bar_slot.empty()
        st.success("Mouvement calibration saved")
        start_timestamp = start.strftime("%d_%m_%Y_%H_%M_%S_%f")
        end_timestamp = end.strftime("%d_%m_%Y_%H_%M_%S_%f")
        path_to_file = "posture.txt"        
        with open(path_to_file, "wb") as binary_file:
            binary_file.write(bytes(start_timestamp+end_timestamp, 'utf-8'))
            
        with open(path_to_file, 'w') as f:
            f.write(start_timestamp + "-" + end_timestamp)
        mesure_id = st.session_state["launcher_session"] #st.session_state["launcher_study_id"]
        blob_name = f"calibration/{mesure_id}/posture_{start_timestamp}.txt"
        upload_to_bucket(blob_name, path_to_file, bucket_name)
                
    col1, col2, col3 = st.columns(3)
    if col3.button("Step 3/3 ➡"):
        switch_page("calibration3_page")
    if col1.button("⬅ step 1/3"):
        switch_page("calibration1_page")
else :
    st.error("You need to sign in to access this page")
    if st.button("Sign In"):
        switch_page("signin_page")