import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import mobile_display
mobile_display()
from utils import side_bar_display
from config import hidden_side_bar
side_bar_display(hidden=hidden_side_bar)
from media.images import *

if "authentication_status" in st.session_state and st.session_state["authentication_status"]:
    st.image(img_wip)
    runButton = st.button("Back")
    if runButton:
        switch_page("free_act_page")
else :
    st.error("You need to sign in to access this page")
    if st.button("Sign In"):
        switch_page("signin_page")