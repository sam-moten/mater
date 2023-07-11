import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from helpers.gcp_connectors import export_firestore
from utils import mobile_display
mobile_display()
from utils import side_bar_display
from config import hidden_side_bar
side_bar_display(hidden=hidden_side_bar)
from media.images import *



# share activity with other users (by mail ?) / when a user make update (new task...) how the other user will get the newest version (save activities otherwise) ?...
# update activity (modify name, new tasks, update old tasks ...) ...

if "authentication_status" in st.session_state and st.session_state["authentication_status"]:

    act_name = st.text_input("Activity's name")
    act_desc = st.text_area("Activity description")
    st.subheader("Create tasks")
    ### 3 label add only (for more ,add label here and session variable to be defined in free_act_page)
    task1 = ""
    task2 = ""
    task3 = ""

    form = st.form(key="1")
    task1 = form.text_input("label", label_visibility="hidden")
    if form.form_submit_button(label='Add task'):
        if task1!='' :
            st.session_state["task_button1"] = not st.session_state["task_button1"]
            #st.session_state["task_counter"] += 1
        else :
            st.warning("Please enter a task name")
        
    if st.session_state["task_button1"] : 
        form = st.form(key="2")
        task2 = form.text_input("label", label_visibility="hidden")
        if form.form_submit_button(label='Add task'):
            if task2!='' :
                st.session_state["task_button2"] = not st.session_state["task_button2"]
                #st.session_state["task_counter"] += 1
            else :
                st.warning("Please enter a task name")
            
    if st.session_state["task_button1"] and st.session_state["task_button2"] :
        form = st.form(key="3")
        task3 = form.text_input("label", label_visibility="hidden")
        if form.form_submit_button(label='Add task'):
            if task3!='' :
                st.session_state["task_button3"] = not st.session_state["task_button3"]
                #st.session_state["task_counter"] += 1
            else :
                st.warning("Please enter a task name")
    else :
        st.warning("Please enter a task name")
        
    if st.session_state["task_button3"]:
        st.error("**You can add 3 tasks maximum for now**")


    col1, col2, col3 = st.columns(3)
    info_slot = st.empty()
    with col1:
        if st.button("Back"):
            switch_page("free_act_page")
    with col3 :
        if st.button("Create"):
            if act_name=="" :
                info_slot.error("Please enter the activity name")
                # check if act exist in fs ....
            elif act_desc=="" :
                info_slot.error("Please enter the activity description")
            elif task1=="" :
                info_slot.error("Please enter at least one task")
                
            else :
                task_counter = st.session_state["task_counter"]
                info_slot.success(f"\n{task_counter} tasks created")
                tasks = list(set([task1, task2, task3]))
                tasks = [i for i in tasks if i != ""]
                # delete tasks "" more properly ....
                # think of a way to create "add task widget more properly...
                # handle unique task more properly when creating wiget ...
                
                username = st.session_state["username"]
                ref_path = f"users/{username}/activities/{act_name}"
                data = {"activity_id":act_name,
                        "activity_icon": img_new_act,
                        "activity_name":act_name,
                       "activity_desc":act_desc,
                       "activity_tasks":tasks}
                
                export_firestore(data, ref_path)
                switch_page("free_act_page")

else :
    st.error("You need to sign in to access this page")
    if st.button("Sign In"):
        switch_page("signin_page")
    


