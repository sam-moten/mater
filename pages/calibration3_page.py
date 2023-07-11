import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import mobile_display, beep_timer
from helpers.gcp_connectors import upload_to_bucket
from datetime import datetime
mobile_display()
import time
from utils import side_bar_display
from config import hidden_side_bar
side_bar_display(hidden=hidden_side_bar)

if "authentication_status" in st.session_state and st.session_state["authentication_status"]:
    
    if "cam_button" not in st.session_state: 
        st.session_state["cam_button"] = False
    
    st.subheader("Launcher Offset") 
    st.info("Take a photo of the **launcher's** clock")
    
    col1, col2, col3 = st.columns(3)
    cam_button = col2.button('Open camera')
    if cam_button:
        st.session_state["cam_button"] = True
    if st.session_state["cam_button"] == True:
        picture = st.camera_input("Open Camera", label_visibility="hidden")
        slot = st.empty()
        if picture:
            now = datetime.now()
            timestamp = now.strftime("%d_%m_%Y_%H_%M_%S_%f")
            slot.warning("sending calibration image ...")
            path_to_file = f"posture.txt"
            with open(path_to_file, "wb") as binary_file:
                binary_file.write(picture.getvalue())
            mesure_id = st.session_state["launcher_session"] #st.session_state["launcher_study_id"]
            bucket_name = "moten-protocols"
            blob_name = f"calibration/{mesure_id}/launcher_clock_{timestamp}.txt"
            upload_to_bucket(blob_name, path_to_file, bucket_name)
            time.sleep(1)
            slot.success("Calibration successful.")
            st.session_state["cam_button"] = False
        
    col1, col2, col3 = st.columns(3)
    if col3.button("Menu"):
        switch_page("menu_page")
    if col1.button("⬅ step 2/3"):
        switch_page("calibration2_page")
else :
    st.error("You need to sign in to access this page")
    if st.button("Sign In"):
        switch_page("signin_page")