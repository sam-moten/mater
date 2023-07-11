import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from helpers.gcp_connectors import fetch_stats
from utils import mobile_display
mobile_display()
from utils import side_bar_display
from config import hidden_side_bar
side_bar_display(hidden=hidden_side_bar)
from media.images import *

if "authentication_status" in st.session_state and st.session_state["authentication_status"]:
    ref_path = f"users/{st.session_state['username']}/protocols"
    stats = fetch_stats(ref_path, version="sami-0")
    if stats==(0,0): # if to be deleted , handle manon and sami protocols without owner attribut
        st.write("no stats for you, you need to create a new account")
    else :
        st.subheader(f"{st.session_state['username'].upper()}, \
                \nYou've done **{stats[1]}** protocols. Still **{stats[0]+stats[1]}** for a **Five Guys !**")
        st.progress(stats[1]/(stats[1]+stats[0]))
    st.image(img_5guys)
    runButton = st.button("Back")
    if runButton:
        switch_page("menu_page")
else :
    st.error("You need to sign in to access this page")
    if st.button("Sign In"):
        switch_page("signin_page")