import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import time
import random
from helpers.gcp_connectors import execute_bigquery_pd, execute_bigquery, query_render
from helpers.sensors import detect_sensor, get_battery_lvl, get_ble_lvl, activate_sensors
from utils import mobile_display
mobile_display()
from utils import side_bar_display
from config import hidden_side_bar, min_sensor
side_bar_display(hidden=hidden_side_bar)



if "authentication_status" in st.session_state and st.session_state["authentication_status"]:
    
    if st.button("Refresh"):
        
        try: # case run refresh before vars created
            del st.session_state["active_sensors"]
            del st.session_state["side_sensors"]
            del st.session_state["list_study_ids"]
            del st.session_state["launcher_study_id"]  
            del st.session_state["launcher_session"]
        except :
            pass
    
    if "active_sensors" not in st.session_state:
        st.session_state["active_sensors"] = []
    if "side_sensors" not in st.session_state:
        st.session_state["side_sensors"] = "Left"
  
    if "list_study_ids" not in st.session_state : 
        slot = st.empty()
        slot.info("Loading metadata from Launcher...")
        query = query_render("launcher_metadata.sql", 
                             params={"project_id": "moten-saas-prod"})
        df_study_ids = execute_bigquery(query) 
        list_study_ids = list(df_study_ids.id.unique())
        list_study_ids.append("...")
        slot.empty()
        st.session_state["df_study_ids"] = df_study_ids
        st.session_state["list_study_ids"] = list_study_ids

    if "launcher_study_id" not in st.session_state :
        st.session_state["launcher_study_id"] = "..."
        st.session_state["launcher_session"] = ""

    study = st.selectbox('Select the same created study on your Launcher',
                         st.session_state["list_study_ids"],
                        st.session_state["list_study_ids"]\
                         .index(st.session_state["launcher_study_id"]))
    sensors_right = []
    sensors_left = []
    sensors = []
    side = "Left"
    try : 
        sensors_right = st.session_state["df_study_ids"].\
                              query(f"id=='{study}'").\
                                  muscles_right.unique()[0].split(',')
        sensors_left = st.session_state["df_study_ids"].\
                              query(f"id=='{study}'").\
                                  muscles_left.unique()[0].split(',')
    except :
        pass

    if sensors_right!=[''] and sensors_left!=['']: 
        st.error("You need to choose one side only")
        sensors = []
    elif sensors_right!=['']:
        sensors = sensors_right
        side = "Right"
    elif sensors_right!=['']:
        sensors = sensors_left
        side = "Left"
        
    st.session_state["side_sensors"] = side
    launcher_muscles = st.session_state["launcher_muscles"]

    sensor_muscle_side = {}
    active_sensors = list()

    if sensors==[]:
        st.error("you need to choose an ongoing measure")
    elif len(sensors)<min_sensor: 
        st.warning(f"you need 5 sensors to operate protocols, you only have {len(sensors)} in this study")
    if sensors!=[] and  len(sensors)>=min_sensor : 
        for s in sensors :
            active_sensors.append("MOTEN-" + s.split('-')[1])
            sensor_muscle_side["MOTEN-" + s.split("-")[1]] = side + "_" + launcher_muscles[s.split("-")[0]]

        st.session_state["sensor_muscle_side"] = sensor_muscle_side
        st.session_state["active_sensors"] = active_sensors

        st.session_state["launcher_study_id"] = study
        
        sessions = st.session_state["df_study_ids"][["id","session"]].set_index('id').to_dict()['session']
        st.session_state["launcher_session"] = sessions[study]
        st.write(f"Chosen session :  \n{st.session_state['launcher_study_id']}")   
        st.markdown("***")
        chosen_sensors = st.multiselect(
        'Choose activated sensors',
        st.session_state["active_sensors"],
        st.session_state["active_sensors"]) 

        col1, col2, col3 = st.columns(3)
        if col2.button("Confirme Choice") :
            st.session_state["chosen_sensors"] = chosen_sensors
            #switch_page("manage_sensors_page")
            switch_page("place_sensor_page") 
    st.markdown("***")
    

    if st.button("Back"):
        if st.session_state["navigation"] == "tracking" :
            switch_page("tracking_choice_page")
        elif st.session_state["navigation"] == "saving" :
            switch_page("save_tracking_page")
        elif st.session_state["navigation"] == "manage" :
            switch_page("menu_page")
else :
    st.error("You need to sign in to access this page")
    if st.button("Sign In"):
        switch_page("signin_page")   


