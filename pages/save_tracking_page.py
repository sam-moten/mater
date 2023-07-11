import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import time
from utils import mobile_display , progress, comment_section
mobile_display(25)
from utils import side_bar_display
from config import hidden_side_bar
side_bar_display(hidden=hidden_side_bar)

if "authentication_status" in st.session_state \
    and st.session_state["authentication_status"] :
    
    uploaded_file = st.file_uploader("Upload a third party data (e.g Cardiac, Motion...)",label_visibility="visible")
    if uploaded_file is not None:
        try :
            import pandas as pd
            dataframe = pd.read_csv(uploaded_file)
            # handle other file type (in helpers.common_utils )
            st.write(dataframe.head())
        except:
            pass
    comment = comment_section()
    

    col1, col2, col3 = st.columns(3)
    bar_slot = st.empty()
    with col1:
        runButton = st.button("Back")
        if runButton:
            switch_page("menu_page")

    if col3.button("Upload file"):
        # send file to storage ...
        # add comment to session in firestore ...
        progress(bar_slot)         
        st.success("File successfully uploaded")

else :
    st.error("You need to sign in to access this page")
    if st.button("Sign In"):
        switch_page("signin_page")

