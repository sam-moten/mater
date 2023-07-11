import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import double_buttons, mobile_display, check_duplicates, protocol_display_section
from helpers.common_utils import reorder_list
from helpers.gcp_connectors import export_sheet, read_sheet
mobile_display()
from utils import side_bar_display
from config import hidden_side_bar
side_bar_display(hidden=hidden_side_bar)


if "authentication_status" in st.session_state \
    and st.session_state["authentication_status"] : 
    
    muscles = st.session_state["muscles"]
    
    if "sensor_muscle_side" not in st.session_state:
        st.session_state["sensor_muscle_side"] = {}
    if "sensor_friction" not in st.session_state:
        st.session_state["sensor_friction"] = {}


    sensor_muscle_side = {}
    sensor_friction = {}
    col1, col2 = st.columns(2)
    side_choice = col1.radio(f'Body side',
                             tuple(reorder_list(["Left","Right"],st.session_state["side_sensors"],0))
                             ,key=f'protocol_radio', 
                             horizontal=True,
                             label_visibility="visible")        
    if st.session_state["sensor_muscle_side"] \
            and set(list(st.session_state["sensor_muscle_side"].keys()))==\
                set(st.session_state["chosen_sensors"]) :
        #display saved choice
        for s in st.session_state["chosen_sensors"] :
            col1, col1bis, col2 = st.columns(3)
            col1bis.write(f'ID :  \n{s}')
            muscle_session = st.session_state["sensor_muscle_side"][s]
            first_muscle = muscle_session[muscle_session.find("_")+1:]
            muscles_names = list(muscles.keys())
            muscles_names = reorder_list(muscles_names,first_muscle,0)
            muscle_choice = col1.selectbox(f'Muscle group',
                                            muscles_names,
                                            key=f"{s}_muscle_{side_choice}")
            col2.image(muscles[muscle_choice],width=80)
            st.session_state["sensor_friction"][s] = True
            friction = st.checkbox("is sensor placed under clothes ?",
                                        st.session_state["sensor_friction"][s],
                                        key=f"{s}_check")
            sensor_friction[s] = friction
            sensor_muscle_side[s] = side_choice + "_" + muscle_choice
            st.markdown("***")
    else:
        #let user place sensors
        for s in st.session_state["chosen_sensors"] :
            col1, col1bis, col2 = st.columns(3)
            col1bis.write(f'ID :  \n{s}')
            muscles_names = list(muscles.keys())
            muscle_choice = col1.selectbox(f'Muscle group',
                                           muscles_names,
                                            key=f"{s}_muscle_{side_choice}")
            col2.image(muscles[muscle_choice],width=80)
            friction = st.checkbox("is sensor placed under clothes ?",True,key=f"{s}_check")
            sensor_friction[s] = friction
            sensor_muscle_side[s] = side_choice + "_" + muscle_choice
            st.markdown("***")
    
    col1, col2, col3 = st.columns(3)
    error_slot = st.empty()
    with col1:
        runButton = st.button("Back")
        if runButton:
            #switch_page("manage_sensors_page")
            switch_page("sensor_detect_page")
            
    with col3:
        runButton = st.button("Confirm")
        if runButton:
            if check_duplicates(sensor_muscle_side.values()):
                error_slot.error("Each sensor can be affected to **one** muscle only")
            else :
                st.session_state["sensor_muscle_side"] = sensor_muscle_side
                st.session_state["sensor_friction"] = sensor_friction
                #switch_page("place_tuto_page")
                switch_page("calibration1_page")

    
else :
    st.error("You need to sign in to access this page")
    if st.button("Sign In"):
        switch_page("signin_page")   

