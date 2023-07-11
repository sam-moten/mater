import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_click_detector import click_detector # pb with css in logs
from utils import double_buttons, mobile_display
from helpers.gcp_connectors import fetch_activities
mobile_display()
from utils import side_bar_display
from config import hidden_side_bar
side_bar_display(hidden=hidden_side_bar)
from media.images import *

# delete created activity (p2)...
# create pages for defined activity (p2)...
if "authentication_status" in st.session_state and st.session_state["authentication_status"]:

    if "n_clicks" not in st.session_state:
        st.session_state["n_clicks"] = "0"
    id = str(int(st.session_state["n_clicks"]) + 1)
    username = st.session_state["username"]
    
    tab1, tab2 = st.tabs(["Created activities", "Defined Activities"])

    with tab1:    
        activities_list = fetch_activities(f"users/{username}/activities") 
        st.markdown(f"<h4 style='text-align: center; color: black;'>Created Activities</h4>", 
                    unsafe_allow_html=True)

        act_col1, act_col2 = st.columns(2)
        for act in activities_list : 
            with act_col1 : 
                st.info(f"{act}") 
            with act_col2 :
                content = f"<a href='#' id='{id}'><img src='{activities_list[act]['activity_icon']}' alt="" width='70' height='50'> </a>"
                clicked = click_detector(content, key=f"{act}act")
                if clicked != "" and clicked != st.session_state["n_clicks"]:
                    st.session_state["n_clicks"] = clicked
                    st.session_state["activity_info"] = activities_list[act]
                    switch_page("live_tracking_page") # just for the photo ...
                    
    with tab2:
        st.markdown(f"<h4 style='text-align: center; color: black;'>Defined Activities </h4>", unsafe_allow_html=True)  
        defined_activities = fetch_activities(f"activities") 

        col1, col2, col3 = st.columns(3)
        for i, act in enumerate(defined_activities):
            icon = defined_activities[act]['activity_icon']
            content = f"<a href='#' id='{id}'><img src='{icon}' alt="" width='70' height='70'> </a>"
            if i%3==0 :
                with col1 :
                    clicked = click_detector(content, key=f"{i}")    
            elif i%3==1 :
                with col2 :
                    clicked = click_detector(content, key=f"{i}")  
            elif i%3==2 :
                with col3 :
                    clicked = click_detector(content, key=f"{i}") 
            if clicked != "" and clicked != st.session_state["n_clicks"]:
                st.session_state["n_clicks"] = clicked
                #st.session_state["activity_info"] = defined_activities[act] ...
                switch_page("end_tracking_page")

    
    prev = {"Back":"tracking_choice_page"} 
    nxt = {"Create":"new_act_page"}

    st.session_state["task_button1"] = False
    st.session_state["task_button2"] = False
    st.session_state["task_button3"] = False
    st.session_state["task_counter"] = 0
    double_buttons(prev, nxt)

else :
    st.error("You need to sign in to access this page")
    if st.button("Sign In"):
        switch_page("signin_page")