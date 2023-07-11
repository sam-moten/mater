import streamlit as st
import streamlit_authenticator as stauth
from streamlit_extras.switch_page_button import switch_page
from utils import mobile_display, fetch_creds
from helpers.gcp_connectors import export_firestore
import time
mobile_display()
from utils import side_bar_display
from config import hidden_side_bar
side_bar_display(hidden=hidden_side_bar)

    
config = fetch_creds()    
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized'])

if "authentication_status" in st.session_state and st.session_state["authentication_status"]:
    username = st.session_state["username"]
    try :
        if authenticator.reset_password(username, 'Reset password'):
            export_firestore({u'password': authenticator.credentials['usernames'][username]['password']}, 
                              f"users/{username}", update=True)            
            st.success('Password modified successfully')
            time.sleep(1)
            switch_page("setting_page")
    except Exception as e : 
        print(e)
        st.error('Passwords do not match')
        
    if st.button("Back"):
        switch_page("setting_page")    

else :
    st.error("You need to sign in to access this page")
    if st.button("Sign In"):
        switch_page("signin_page")
