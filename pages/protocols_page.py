import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import mobile_display, progress ,style_button_row
from helpers.gcp_connectors import execute_bigquery, fetch_undone_protocol
mobile_display() 
from utils import side_bar_display, ChangeButtonColour
from config import hidden_side_bar
side_bar_display(hidden=hidden_side_bar)
from media.images import *


st.markdown(f"<h4 style='text-align: center; color: black;'>Operate Protocols</h4>", unsafe_allow_html=True)

if "authentication_status" in st.session_state and st.session_state["authentication_status"]:
    if "protocols_list" not in st.session_state:
        st.session_state["protocols_list"] = {}
        
    if "n_clicks" not in st.session_state:
        st.session_state["n_clicks"] = "0"
    id = str(int(st.session_state["n_clicks"]) + 1)
    weight_range = st.slider('Select a range of weights at your disposal',0, 15, (0, 10))    
    noise = True
    gyro = False #st.checkbox("Only Manon's protocols")
    
    bar_slot = st.empty()
    butt3, butt2, butt1 = st.columns(3)
    if butt1.button("search") : 
        progress(bar_slot, sleep=0.01)
        bar_slot.empty()
        protocols_fs_path = f"users/{st.session_state['username']}/protocols"
        filters = {"weight_range":weight_range,
                   "noise":noise,
                   "gyro":gyro}
        # limit hard coded for manon....
        protocols_list = fetch_undone_protocol(protocols_fs_path,filters,limit=10)
        st.session_state["protocols_list"] = protocols_list
        if len(protocols_list)==0 :
            st.error("No protocol found, please try other set of filters")

    if st.session_state["protocols_list"]: 
        protocols_list = st.session_state["protocols_list"]
        for i in protocols_list:
            name = protocols_list[i]["protocol_name"]
            col1, col2 = st.columns(2)
            info_display = f"{protocols_list[i]['protocol_name']}  \
            \n{protocols_list[i]['protocol_weight']} kg - \
            {protocols_list[i]['protocol_speed']} s/rep  \
            \n{protocols_list[i]['protocol_noise']} \
            {protocols_list[i]['protocol_noise_intensity']}"
            with col1 :
                if protocols_list[i]["status"] == "done":
                    st.success(f"{info_display} ✅")
                else:
                    st.warning(f"{info_display}")
            with col2 :
                go_button = st.button("⇨", 
                                      on_click=style_button_row, 
                                      kwargs={'clicked_button_ix': 1, 'n_buttons': 4}, 
                                      key=f'{i}')
                ChangeButtonColour("⇨", 'white', 'red') 
                if go_button :
                    protocols_list[i]["protocol_id"] = i                    
                    st.session_state["protocol_info"] = protocols_list[i]
                    switch_page("protocol_desc_page")    
        
    if butt3.button("Back"):
        #switch_page("tracking_choice_page")
        switch_page("menu_page")

else :
    st.error("You need to sign in to access this page")
    if st.button("Sign In"):
        switch_page("signin_page")