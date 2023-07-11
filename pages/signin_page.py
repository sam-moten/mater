import streamlit as st
import streamlit_authenticator as stauth
from streamlit_extras.switch_page_button import switch_page
from utils import mobile_display, fetch_creds
mobile_display()
from utils import side_bar_display, double_buttons
from config import hidden_side_bar
side_bar_display(hidden=hidden_side_bar)

config = fetch_creds()
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized'])

name, authentication_status, username = authenticator.login('Sign In', 'main') 
if st.session_state["authentication_status"]:
    switch_page("menu_page")   
elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect') 
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')
    
prev = {"Home Page":"app"}
nxt = {"Forget pwd":"fgt_pwd_page"}
double_buttons(prev, nxt)    
