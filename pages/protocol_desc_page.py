import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import double_buttons, mobile_display, protocol_display_section
mobile_display() 
from utils import side_bar_display
from config import hidden_side_bar, min_sensor
side_bar_display(hidden=hidden_side_bar)
from media.images import *

# block when prod and propose to go to manage sensors...
if "authentication_status" in st.session_state \
        and st.session_state["authentication_status"]:
    protocol_info = st.session_state["protocol_info"]
    protocol_display_section(protocol_info, section="all")
    col1, col2, col3 = st.columns(3)
    if col1.button("Back"):
        switch_page("protocols_page")
    st.warning(f"You need at least **{min_sensor} sensors** to operate a protocol")
    if col3.button("Got it !"):
        if "chosen_sensors" not in st.session_state :
            st.warning("No sensor selected")
            switch_page("protocol_warning_page")
        elif len(st.session_state["chosen_sensors"]) <= min_sensor :
            st.warning(f"You need at least **{min_sensor} sensors** to operate a protocol")
            # block when prod and propose to go to manage sensors...
            switch_page("protocol_warning_page")  
        else :
            switch_page("protocol_warning_page")
    
else :
    st.error("You need to sign in to access this page")
    if st.button("Sign In"):
        switch_page("signin_page")

    


