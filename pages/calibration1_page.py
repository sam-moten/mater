import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import mobile_display, beep_timer
from helpers.gcp_connectors import upload_to_bucket
from datetime import datetime
import time
mobile_display()
from utils import side_bar_display
from config import hidden_side_bar, bucket_name
side_bar_display(hidden=hidden_side_bar)
from media.images import *

if "authentication_status" in st.session_state and st.session_state["authentication_status"]:
    
    st.subheader("Time Calibration")
    col1, col2 = st.columns(2)
    col1.info("Double tap one of the sensors")
    col2.image(gif_tap,width=120)
    sensor = st.selectbox("Select a sensor to tap", st.session_state["chosen_sensors"])
    
    col1, col2, col3 = st.columns(3)
    slot = st.empty()
    if col2.button("calibrate"):
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
        slot.info("**Double Tap NOW !**")
        now = datetime.now()
        timestamp = now.strftime("%d_%m_%Y_%H_%M_%S_%f")
        time.sleep(1)
        slot.empty()        
        st.success("DONE, Repeat the action if you're not sure")
        path_to_file = "mmg.txt"
        with open(path_to_file, 'w') as f:
            f.write(timestamp)
        mesure_id = st.session_state["launcher_session"] #st.session_state["launcher_study_id"]
        
        blob_name = f"calibration/{mesure_id}/mmg_{sensor}_{timestamp}.txt"
        print(blob_name)
        upload_to_bucket(blob_name, path_to_file, bucket_name)

        
    st.markdown("****")
    col1, col2, col3 = st.columns(3)
    if col3.button("Step 2/3 ➡"):
        switch_page("calibration2_page")
        
    if col1.button("Back"):
        #switch_page("place_tuto_page")
        switch_page("place_sensor_page")
else :
    st.error("You need to sign in to access this page")
    if st.button("Sign In"):
        switch_page("signin_page")