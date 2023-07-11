import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import mobile_display, comment_section
from helpers.notifier import send_mail
mobile_display()
from utils import side_bar_display
from config import hidden_side_bar
side_bar_display(hidden=hidden_side_bar)
from media.images import *

if "authentication_status" in st.session_state and st.session_state["authentication_status"]:
    comment, sub = comment_section()
    info_slot = st.empty()
    col1, col2, col3 = st.columns(3)
    send_slot = col2.empty()
    if sub :
        info_slot.warning("sending your comment...")
        text = f"""Hello Support Team,\
        \n\nThis is a comment sent by {st.session_state["username"]}. \
        \n{comment}  \
        \n\nRegards
        """
        mail_context = {"subject": f"[MATER-SUPPORT] - {st.session_state['username']}",
                        "text": text,
                        "sender_email":"moten.notifier@gmail.com",
                        "password":"ffdrdhuuvvpvucxm",
                        "receiver_email":["sassili@moten-tech.com",]}
        send_mail(mail_context)
        info_slot.success('Comment sent successfully to the support team')
        send_slot.image(img_mail, width=80)
    runButton = st.button("Back")
    if runButton:
        switch_page("setting_page")
else :
    st.error("You need to sign in to access this page")
    if st.button("Sign In"):
        switch_page("signin_page")