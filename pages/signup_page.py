import streamlit as st
import streamlit_authenticator as stauth
from streamlit_extras.switch_page_button import switch_page
from utils import mobile_display, fetch_creds
from helpers.common_utils import mail_exist, mail_valid
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

try:
    if authenticator.register_user('New user', preauthorization=False):
        new_username = list(config.get("credentials")['usernames'].keys())[-1]
        if (" " in new_username) or ("/" in new_username) :
            config["credentials"]["usernames"].pop(new_username, None)
            st.error("spaces and / are not allowed in username")            
        new_mail = config["credentials"]["usernames"][new_username]["email"]
        if mail_exist(config, new_mail) :
            #config["credentials"]["usernames"].pop(new_username, None)
            #st.error("Email adress already used")
            # to let people use the same mail !
            pass
        if not mail_valid(new_mail):
            config["credentials"]["usernames"].pop(new_username, None)
            st.error("Invalid email adress")
            
        else:
            st.success('User registered successfully')
            st.session_state["new_username"] = list(config.get("credentials")\
                                                    ['usernames'].keys())[-1]
            export_firestore({'password': authenticator.credentials['usernames'][new_username]['password'],
                              'email':authenticator.credentials['usernames'][new_username]['email'],
                              'name':authenticator.credentials['usernames'][new_username]['name']}, 
                              f"users/{new_username}", update=True)
            time.sleep(1)
            switch_page("user_form_page")
                   
except Exception as e:
    st.error(e)
    
col1, col2, col3 = st.columns(3)
with col3:
    runButton = st.button("Home Page")
    if runButton:
        switch_page("app")
