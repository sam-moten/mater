import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import double_buttons, mobile_display
from helpers.gcp_connectors import read_sheet
mobile_display(ratio=25)
from utils import side_bar_display
from config import hidden_side_bar
side_bar_display(hidden=hidden_side_bar)
from media.images import *

if "authentication_status" in st.session_state and st.session_state["authentication_status"]:
    
    slot = st.empty()
    slot.info("Loading user data ...")
    if "muscles" not in st.session_state :
        df = read_sheet(spreadsheet="DOE", sheet_name="muscles")
        tdf = df.T
        muscles = dict(tdf.rename(columns=tdf.iloc[0]).iloc[1])
        launcher_muscles = dict(tdf.rename(columns=tdf.iloc[2]).iloc[0])
        st.session_state["launcher_muscles"] = launcher_muscles
        st.session_state["muscles"] = muscles
    slot.empty()
    
    col1, col2 = st.columns(2, gap="small")
    col1.image(img_manage_sensors, width=90)
    manage_sensors_button = col1.button(f"Manage sensors")
    col2.image(img_start_tracking, width=90)
    start_tracking_button = col2.button(f"Start tracking")
    col1.image(img_save_tracking, width=90)
    save_tracking_button = col1.button(f"Save session")
    col2.image(img_stats, width=90)
    stats_button = col2.button(f"Statistics")
    col1.image(img_user_setting, width=90)
    user_setting_button = col1.button(f"User setting")
    col2.image(img_exit, width=90)
    exit_button = col2.button(f"Log out")     

    if stats_button:
        # go to stats page
        st.session_state["navigation"] = 'stats'
        switch_page("stats_page")
    elif start_tracking_button:
        # go to start tracking page
        st.session_state["navigation"] = 'tracking'
        #switch_page("tracking_choice_page")
        switch_page("protocols_page")
        
    elif save_tracking_button:
        # go to save tracking page
        st.session_state["navigation"] = 'saving'
        switch_page("save_tracking_page")
    elif manage_sensors_button:
        # go to manage sensors page
        st.session_state["navigation"] = 'manage'
        switch_page("sensor_detect_page")
    elif user_setting_button:
        # go to user setting page
        st.session_state["navigation"] = 'setting'
        switch_page("setting_page")
    elif exit_button:
        # go to user setting page
        st.session_state["navigation"] = 'exit'
        switch_page("app")
            
else :
    st.error("You need to sign in to access this page")
    if st.button("Sign In"):
        switch_page("signin_page")