import streamlit as st
import streamlit_authenticator as stauth
from streamlit_extras.switch_page_button import switch_page
from utils import mobile_display, fetch_creds
from helpers.notifier import send_mail
from helpers.gcp_connectors import export_firestore
import time
mobile_display()
from utils import side_bar_display
from config import hidden_side_bar
side_bar_display(hidden=hidden_side_bar)
from media.images import *

st.image(pwd_gif, width=300)    

config = fetch_creds()    
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized'])

try:
    username, email = authenticator.forgot_username('Forgot password')
    info_slot = st.empty()
    if username:
        info_slot.info("sending new password to mail adress...")
        random_pwd = authenticator._set_random_password(username)
        authenticator._update_password(username, random_pwd) 
        hashed_password = stauth.Hasher([random_pwd]).generate()[0]
        export_firestore({u'password': hashed_password}, 
                          f"users/{username}", update=True)
            
        text = f"""Hello {authenticator.credentials["usernames"][username]["name"]},\
        \n\nWe have received your request to reset your password. \
        \nUsername : {username}\
        \nTemporary password : {random_pwd}\
        \n\nTo update your password : sign In >> User profile >> Reset pwd.  \
        \n\nRegards
        """
        mail_context = {"subject": "Reset Password",
                        "text": text,
                        "sender_email":"moten.notifier@gmail.com",
                        "password":"ffdrdhuuvvpvucxm",
                        "receiver_email":[email]}
        send_mail(mail_context)
        info_slot.success('New password sent securely')
    elif username == False:
        st.error('Email not found')
except Exception as e:
    st.error(e)
    
if st.button("Home page"):
        switch_page("app")