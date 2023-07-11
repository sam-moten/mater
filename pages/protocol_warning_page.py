import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import mobile_display
mobile_display()



st.markdown(f"<h4 style='text-align: center; color: black;'>⚠️ Protocol's Warning ⚠️</h4>", unsafe_allow_html=True)

if "authentication_status" in st.session_state and st.session_state["authentication_status"]:
    
    
    protocol_name = st.session_state["protocol_info"]["protocol_name"]
    if protocol_name=="flexion coude":
        st.image("media/flexion_coude_bad.png")
        st.image("media/flexion_coude_good.png")
    elif protocol_name=="flexion epaule":
        st.image("media/flexion_epaule.png")
    elif protocol_name=="abduction epaule":
        st.image("media/abduction_epaule.png")
    elif protocol_name in ["flexion poignet", "rotation poignet", "serrer poignet"]:
        st.image("media/poignet.png")
    elif protocol_name=="porter charge":
        st.image("media/porter_charge.png")
    else :
        st.error("unrecognized protocol's name")    
    
    col1, col2, col3 = st.columns(3)
    if col3.button("Next ➡"):
        switch_page("tracking_start_page")
    if col1.button("Back"):
        switch_page("protocol_desc_page")
else :
    st.error("You need to sign in to access this page")
    if st.button("Sign In"):
        switch_page("signin_page")
        
        
