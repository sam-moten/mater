import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import mobile_display
from helpers.gcp_connectors import get_user_info
from helpers.common_utils import reorder_list
import time
mobile_display()
from utils import side_bar_display
from config import hidden_side_bar
side_bar_display(hidden=hidden_side_bar)
from media.images import *


if "authentication_status" in st.session_state and st.session_state["authentication_status"]:
    username = st.session_state["username"]

    col1, col2, col3 = st.columns(3, gap="small")
    col1.image(img_pwd, width=90)
    reset_pwd_button = col1.button(f"Password")
    col2.image(img_user_info, width=90)
    update_info_button = col2.button(f"User info")
    col3.image(img_support, width=90)
    support_button = col3.button(f"Support")
    if reset_pwd_button:
        switch_page("reset_pwd_page")
    elif update_info_button:
        st.session_state["user_info"] = get_user_info(username)
        st.session_state["user_info"] = {"born" : st.session_state["user_info"]["born"], 
                                         "sex" : reorder_list(list(('Male', 'Female')),
                                                              st.session_state["user_info"]["sex"],0),
                                         "activity": reorder_list(list(('Low (< 1h)','Medium (1-3h)','High (> 3h)')),
                                                              st.session_state["user_info"]["activity"],0), 
                                         "weight":st.session_state["user_info"]["weight"], 
                                         "bicep_size_nc":st.session_state["user_info"]["bicep_size_nc"],
                                         "bicep_size_c":st.session_state["user_info"]["bicep_size_c"],
                                         "forearm_size":st.session_state["user_info"]["forearm_size"],
                                         "username":username,
                                         "comment":st.session_state["user_info"]["comment"]}

        switch_page("user_form_page")
    elif support_button:
        switch_page("support_page")
        
    if st.button("Back"):
        switch_page("menu_page")    

else :
    st.error("You need to sign in to access this page")
    if st.button("Sign In"):
        switch_page("signin_page")
