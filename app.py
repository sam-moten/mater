import streamlit as st
st.set_page_config(page_title='moten.io',page_icon=":muscle:",initial_sidebar_state="collapsed")
from utils import double_buttons, mobile_display
mobile_display(ratio=25)

from utils import side_bar_display
from config import hidden_side_bar
side_bar_display(hidden=hidden_side_bar)
from media.images import *


st.markdown(f"<h1 style='text-align: center; color: #f7a71bff;'>M.A.T.E.R</h1>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center; color: #00a9dbff;'>Moten Activity TrackER</h1>", unsafe_allow_html=True)

# protocol : serrer poing, le hold est perturbant , penser à indexé l'icon de hold/ pause par rapport au protocols
# quand le protocol contient un choc , il faut bien le rappeler sur la page de tracking (final avec countdown)
# appli local ... is a must !
# pendant le protocol , essayer de changer le titre  (repx ...) par repaus ou hold ...
# stats to fix 






# image on local test
# session plus longue
# block when less than 5 sensors ?
### clean cash

#session stat : 
# name, authentication_status, username , logout
# new_username 
# navigation (saving,tracking, stats, manage)
# n_clicks
# tracking_exp = 'protocol' , free_activity , live_tracking
# protocol_info
# activity_info
# n_clicks (maybe probelmatic duplicate)
# protocols_list

# task_button1 bool
# task_button2 bool 
# task_button3 bool
# task_counter int (from 0 )

# active_sensors
# chosen_sensors
# detection_button
# sensor_muscle_side
# sensor_friction

# task_cycle
# timer

# speech
# comment


st.session_state['logout'] = True
st.session_state['name'] = None
st.session_state['username'] = None
st.session_state['authentication_status'] = None
st.session_state['protocols_list'] = None

#st.image(img_moten)
st.image("media/moten_img.jpeg")
prev = {"Sign In":"signin_page"}
nxt = {"Sign Up":"signup_page"}
double_buttons(prev, nxt)


