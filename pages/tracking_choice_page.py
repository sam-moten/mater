import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import mobile_display
mobile_display() 
from utils import side_bar_display
from config import hidden_side_bar
side_bar_display(hidden=hidden_side_bar)
from media.images import *

if "authentication_status" in st.session_state and st.session_state["authentication_status"]:
        
    col1, col2, col3 = st.columns(3, gap="small")
    col1.image(img_op_proto, width=90)
    protocols_button = col1.button(f"Operate Protocols")
    col2.image(img_free_act, width=90)
    free_act_button = col2.button(f"Free Activities")
    col3.image(img_live, width=90)
    live_tracking_button = col3.button(f"Live Tracking") 


    if protocols_button:
        # go to stats page
        st.session_state["tracking_exp"] = 'protocol'
        switch_page("protocols_page")
    if free_act_button:
        # go to start tracking page
        st.session_state["tracking_exp"] = 'free_activity'
        switch_page("free_act_page")
    if live_tracking_button:
        # go to start tracking page
        st.session_state["tracking_exp"] = 'live_tracking'
        switch_page("live_tracking_page")
        
    if st.button("Back"):
        switch_page("menu_page")

else :
    st.error("You need to sign in to access this page")
    if st.button("Sign In"):
        switch_page("signin_page")



