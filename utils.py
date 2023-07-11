import streamlit as st
import streamlit_authenticator as stauth
from streamlit_extras.switch_page_button import switch_page
from datetime import datetime, timedelta
import time
from helpers.gcp_connectors import export_firestore, get_last_doc, get_user_info, get_users
import traceback
from helpers.logging import logger
from math import ceil
#from beepy import beep
from st_click_detector import click_detector # prb with css here. ?
from media.images import *


gif_3s_timer = "https://media.tenor.com/J_6Rv7jZ5K4AAAAC/cinema-321.gif"
gif_5s_timer = "https://i.pinimg.com/originals/c2/3f/d6/c23fd60d83d100af7e04641c78465de1.gif"


def side_bar_display(hidden=True):
    if hidden:
        st.markdown("""
                <style>
                    [data-testid="collapsedControl"] {
                        display: none
                    }
                </style>
                    """,
                    unsafe_allow_html=True)
    else :
        pass

def save_data(protocol_info) :
    """
    send experiment cycles info to firestore database
    TO DO : delete exception
    """
    task = f"{protocol_info['protocol_id']}" 
    exp_id = protocol_info['protocol_id']  
    exp_type = "protocol" 
    username = st.session_state["username"]
    # send data
    try :
        chosen_sensors = st.session_state["chosen_sensors"]
        sensor_friction = st.session_state["chosen_sensors"] 
        sensor_muscle_side = st.session_state["sensor_muscle_side"]
    except : # to delete after blocking access in protocol_desc page
        #st.error("No sensor chosen for this session")
        chosen_sensors = "" 
        sensor_friction = ""
        sensor_muscle_side = ""

    vals = st.session_state["task_cycle"][task]
    cycle_id = list(vals.keys())[1] 
    cycle_details = list(vals.values())[1]
    cycle_nb = list(vals.values())[0]

    cycle_data = {"exp_id":exp_id,
            "exp_type":exp_type,
            "username":username,
            "chosen_sensors" : chosen_sensors,
            "sensor_muscle_side":sensor_muscle_side,
            "sensor_friction": sensor_friction,
            "cycle":cycle_details}

    cycle_fs_ref = f"experiments/{exp_id}/{username}/{cycle_id}"
    export_firestore(cycle_data, cycle_fs_ref, update=True)

    protocol_data = {x: protocol_info[x] for x in protocol_info if x not in {"username","status"}}
    protocol_fs_ref = f"experiments/{exp_id}"
    export_firestore(protocol_data, protocol_fs_ref, update=True)


def beep_timer(secs):
    """
    countdown beep function depending on seconds
    only 3 and 5 secs for now 
    """
    if secs==3:
        gif = gif_3s_timer
    elif secs==5:
        gif = gif_5s_timer
    img_slot = st.empty()
    img_slot.image(gif, width=350)
    beg = time.time()
    for i in range(secs):
        #beep(sound=1)
        #time.sleep(0.33)
        time.sleep(1) # replacement
        
    img_slot.empty()


def cycle(n):
    if n%2==0:
        return 0 #2
    else :
        return 1

img1 = "https://img.icons8.com/?size=512&id=116643&format=png"
img2 = "https://img.icons8.com/?size=512&id=116607&format=png"
img3 = "https://img.icons8.com/?size=512&id=116609&format=png"
img4 = "https://img.icons8.com/?size=512&id=116615&format=png"
img5 = "https://img.icons8.com/?size=512&id=116620&format=png"
img_hold = "https://cdn-icons-png.flaticon.com/512/5261/5261318.png"
list_chrono_imgs = [img5, img4, img3, img2, img1] 


def protocol_progress(rep,contraction, cycles ,sp, slp=3):
    """
    experiment cycle progress bar with countdown
    TO
    """
    count_slot = st.empty()
    bar_slot = st.empty()
    col1, col2, col3 = st.columns(3)
    image_slot = col2.empty()
    image_stop_slot = col1.empty()
    if contraction=="dynamic":
        reps = 2*rep
    else:
        reps = rep
        #slp = 5

    for i in range(1, reps+1):
        if contraction=="isometric":
            count_slot.subheader(f"rep **{i}**")
        else:
            count_slot.subheader(f"rep **{ceil(i/2)}** - **{cycles[cycle(i)]}** ") 
        progress(bar_slot,sleep=0.01*sp, speed=10)
        time.sleep(0.5)
        for j in range(slp):
            gif_timer = list_chrono_imgs[j]
            
            image_slot.image(gif_timer, width=80)
            image_stop_slot.image(img_hold, width=80) 
            time.sleep(1)
            
        count_slot.empty()
        image_slot.empty()
        image_stop_slot.empty()
        bar_slot.empty()
        time.sleep(0.1)   
    
    
def protocol_progress2(rep,contraction, cycles ,sp, slp=5):
    """
    experiment cycle progress bar with countdown
    TO
    """
    count_slot = st.empty()
    bar_slot = st.empty()
    col1, col2, col3 = st.columns(3)
    image_slot = col2.empty()
    image_stop_slot = col1.empty()
    if contraction=="dynamic":
        reps = 2*rep
        gif_timer = gif_3s_timer
        
    elif contraction=="isometric":
        reps = rep
    else:
        reps = rep
        slp = 5
        gif_timer = gif_5s_timer 


    for i in range(1, reps+1):
        if contraction=="isometric":
            count_slot.subheader(f"rep **{i}**")
        else:
            count_slot.subheader(f"rep **{ceil(i/2)}** - **{cycles[cycle(i)]}** ") 
        progress(bar_slot,sleep=0.01*sp, speed=10)
        time.sleep(0.5)
        image_slot.image(gif_timer, width=150)
        image_stop_slot.image(img_hold, width=80) 
        time.sleep(slp)
        count_slot.empty()
        image_slot.empty()
        image_stop_slot.empty()
        bar_slot.empty()
        time.sleep(0.1)   


def protocol_display_section(protocol_info,section="all"):
    """
    display a protocol information or summary
    """
    
    if section=="small":
        st.subheader(f"Protocol : {protocol_info['protocol_name']}")
        col1, col2, col3 = st.columns(3, gap="small")
        col1.info(f"{protocol_info['protocol_weight']} kg ")
        col2.info(f"{protocol_info['protocol_speed']} sec")
        col3.info(f"{protocol_info['protocol_repetition']} reps")
        st.info(f"Noise : {protocol_info['protocol_noise']} -  \
             {protocol_info['protocol_noise_intensity']} ")
    elif section=="optim":
        st.info(f"Protocol : **{protocol_info['protocol_name']}** \
                \nNoise : {protocol_info['protocol_noise']} -  \
             {protocol_info['protocol_noise_intensity']} ")
        col1, col2, col3 = st.columns(3, gap="small")
        col1.info(f"{protocol_info['protocol_weight']} kg ")
        col2.info(f"{protocol_info['protocol_speed']} sec")
        col3.info(f"{protocol_info['protocol_repetition']} reps")
    elif section=="all0" :
        st.subheader(f"Protocol : {protocol_info['protocol_name']}")
        st.info(f'**repetion** : {protocol_info["protocol_repetition"]} x  \
            \n**excution speed** : {protocol_info["protocol_speed"]} s  \
            \n**weight to lift** : {protocol_info["protocol_weight"]} kg') 
        st.info(f'**Noise** : {protocol_info["protocol_noise"]} -  \
             {protocol_info["protocol_noise_intensity"]}')
        st.info(f'**Description** : {protocol_info["protocol_desc"]}')
        st.image(protocol_info["protocol_tuto"])
    elif section=="all1" :
        st.subheader(f"Protocol : {protocol_info['protocol_name']}")
        st.info(f'**repetion** : {protocol_info["protocol_repetition"]} x  \
            \n**excution speed** : {protocol_info["protocol_speed"]} s  \
            \n**weight to lift** : {protocol_info["protocol_weight"]} kg  \
            \n**Noise** : {protocol_info["protocol_noise"]} -  \
             {protocol_info["protocol_noise_intensity"]}') 
        st.info(f'**Description** : {protocol_info["protocol_desc"]}')
        st.image(protocol_info["protocol_tuto"])
    elif section=="all" :
        st.image(protocol_info["protocol_tuto"])
        noise = f'{protocol_info["protocol_noise"]} - {protocol_info["protocol_noise_intensity"]}'
        if "sans" not in noise :
            noise = f"⚠️ {noise}" 
        st.info(f'**protocol** : {protocol_info["protocol_name"]}  \
            \n**repetion** : {protocol_info["protocol_repetition"]} x  \
            \n**excution speed** : {protocol_info["protocol_speed"]} s  \
            \n**weight to lift** : {protocol_info["protocol_weight"]} kg  \
            \n**Noise** : {noise}') 
        st.info(f'**Description** : {protocol_info["protocol_desc"]}')
        
        
def comment_section():
    """
    custom widget : comment form
    """
    form = st.form(key="comment_form",clear_on_submit=True) 
    comment = form.text_area("Comment",value="")
    submition_button = form.form_submit_button(label='Submit')
    if submition_button :
        st.session_state["comment"] = comment
    else :
        st.session_state["comment"] = ""  
    return st.session_state["comment"], submition_button
    # modify output wherever this function is used
        
def progress(slot, sleep=0.05, speed=10):
    """
    custom widget : progress bar
    """
    bar = slot.progress(0)
    for percent_complete in range(speed*10):
        time.sleep(sleep)
        bar.progress(percent_complete + 1)

        
def check_duplicates(item_list):
    """
    Check if given list contains any duplicates 
    """    
    item_set = set()
    for elem in item_list:
        if elem in item_set:
            return True
        else:
            item_set.add(elem)         
    return False


def mobile_display(ratio=33):
    """
    Force display ratio for dynamic display on mobile size screen
    """
    
    if ratio == 33 :
        st.write('''<style>[data-testid="column"] {width: calc(33% - 1rem) !important;flex: 1 1 calc(33% - 1rem) !important;min-width: calc(33% - 1rem) !important;}</style>''', 
                 unsafe_allow_html=True)
    elif ratio == 25 :
        st.write('<style>[data-testid="column"] {width: calc(25% - 1rem) !important;flex: 1 1 calc(25% - 1rem) !important;min-width: calc(25% - 1rem) !important;}</style>', 
                 unsafe_allow_html=True)
    elif ratio == 20 :
        st.write('<style>[data-testid="column"] {width: calc(20% - 1rem) !important;flex: 1 1 calc(20% - 1rem) !important;min-width: calc(20% - 1rem) !important;}</style>', 
                 unsafe_allow_html=True)
    elif ratio == 16 :    
        st.write('<style>[data-testid="column"] {width: calc(16% - 1rem) !important;flex: 1 1 calc(16% - 1rem) !important;min-width: calc(16% - 1rem) !important;}</style>', 
                 unsafe_allow_html=True)

        
def double_buttons(prev, nxt): 
    """
    custom widget : double button with a switch page logic 
    to be used for navigation purpose only
    """
    
    prev_name = list(prev.keys())[0]
    previous_page =  prev[prev_name]
    next_name = list(nxt.keys())[0]
    next_page = nxt[next_name]
    col1, col2, col3 = st.columns(3)
    with col1:
        runButton = st.button(prev_name)
        if runButton:
            switch_page(previous_page)

    with col3:
        runButton = st.button(next_name)
        if runButton:   
            switch_page(next_page)
            
            
def create_task_timer_widget(activity_info):
    """
    custom widget : create timer start and stop for tasks
    for free activity
    TO DO :  ending logic to be recoded
    """
    started_time = datetime.now().strftime('%Y-%m-%d')
    for task in reversed(activity_info["activity_tasks"]) : 
        st.info(f"**{task}**")
        col1, col2, col3, col4 = st.columns(4)
        col1.image(img_chrono, width=40)
        st.session_state["timer"] = col3.markdown(f"<h4 style='text-align: center; color: black;'>{00:02d}:{00:02d} </h4>", 
                               unsafe_allow_html=True)
        timer = st.session_state["timer"]
        start_button = col2.button("start", key=f"{task}_start")
        end_button = col4.button("end", key=f"{task}_end")


        if task not in st.session_state["task_cycle"].keys():
            cycle_num = 0
            cycle_start = None
            secs = 0
            st.session_state["task_cycle"][f"{task}"] = {}
            st.session_state["task_cycle"][f"{task}"][f"cycle_{cycle_num}"] = {"start":cycle_start, "duration":secs}


        if start_button:

            cycle_num = max([int(item.split('_', 1)[1]) for item in list(st.session_state["task_cycle"][f"{task}"].keys())]) + 1
            cycle_start = datetime.now()
            for secs in range(0,3600*60,1):
                mm, ss = secs//60, secs%60
                timer.markdown(f"<h4 style='text-align: center; color: black;'>{mm:02d}:{ss:02d} </h4>", 
                               unsafe_allow_html=True)
                time.sleep(1)
                st.session_state["task_cycle"][f"{task}"][f"cycle_{cycle_num}"] = {"start":cycle_start, "duration":secs}
            if end_button:
                st.session_state["timer"].empty()
        
    st.session_state["task_cycle"]["started_time"] = started_time
    st.markdown("****")
    
           
def create_task_countdown_widget2(protocol_info):
    """
    custom widget : create timer progression
    for protocols
    """
    if "n_clicks" not in st.session_state:
        st.session_state["n_clicks"] = "0"
    id = str(int(st.session_state["n_clicks"]) + 1)
    task = f"{protocol_info['protocol_id']}" 
    exp_id = protocol_info['protocol_id']       
    exp_type = "protocol" 
    username = st.session_state["username"]
    col1, col2, col3 = st.columns(3)
    if task not in st.session_state["task_cycle"].keys():
        try :
            fs_path = f"experiments/{exp_id}/{username}"
            field = "cycle.start"
            last_cycle = int(get_last_doc(fs_path,field).split("_")[1])
        except :
            last_cycle = 0
        
        st.session_state["task_cycle"][f"{task}"] = {f"cycle_{last_cycle}":{"start":None,
                                                                            "duration":0},
                                                     "cycle":last_cycle}
    st.session_state["task_cycle"][f"{task}"]["cycle"] += 1
    cycle_num = st.session_state["task_cycle"][f"{task}"]["cycle"]
    #beep_timer(secs=3)
    cycle_start = datetime.now() 
    dic_update = {"cycle":cycle_num,
                  f"cycle_{cycle_num}":{"start":cycle_start, 
                                        "duration":None}} 
    protocol_progress(rep=protocol_info["protocol_repetition"],
                      contraction=protocol_info["gesture_contraction"], 
                      cycles=[protocol_info["gesture_type_bis"], ### for demo, inversed cycles
                             protocol_info["gesture_type"]],
                      sp=int(protocol_info["protocol_speed"]),
                      slp=5)
    dic_update[f"cycle_{cycle_num}"]["duration"] = round((datetime.now() - cycle_start).total_seconds())  
    st.session_state["task_cycle"][f"{task}"] = dic_update
    
    
    
    
def style_button_row(clicked_button_ix, n_buttons):
    def get_button_indices(button_ix):
        return {
            'nth_child': button_ix,
            'nth_last_child': n_buttons - button_ix + 1
        }

    clicked_style = """
    div[data-testid*="stHorizontalBlock"] > div:nth-child(%(nth_child)s):nth-last-child(%(nth_last_child)s) button {
        border-color: rgb(255, 75, 75);
        color: rgb(255, 75, 75);
        box-shadow: rgba(255, 75, 75, 0.5) 0px 0px 0px 0.2rem;
        outline: currentcolor none medium;
    }
    """
    unclicked_style = """
    div[data-testid*="stHorizontalBlock"] > div:nth-child(%(nth_child)s):nth-last-child(%(nth_last_child)s) button {
        pointer-events: none;
        cursor: not-allowed;
        opacity: 0.65;
        filter: alpha(opacity=65);
        -webkit-box-shadow: none;
        box-shadow: none;
    }
    """
    style = ""
    for ix in range(n_buttons):
        ix += 1
        if ix == clicked_button_ix:
            style += clicked_style % get_button_indices(ix)
        else:
            style += unclicked_style % get_button_indices(ix)
    st.markdown(f"<style>{style}</style>", unsafe_allow_html=True)
        
            
def fetch_creds():
    config = {'cookie':{},
              'preauthorized':{},
              'credentials':{'usernames':{}}}

    config['cookie']['name'] = 'some_cookie_name'
    config['cookie']['key'] = 'some_signature_key'
    config['cookie']['expiry_days'] = 30
    config['preauthorized'] = {'emails': ['sassili@moten-tech.com']}
    users = get_users("users")
    for user in users :
        user_info = get_user_info(user)
        config['credentials']['usernames'][user] = {'email': user_info['email'],
                                                    'name':user_info['name'],
                                                    'password':user_info['password']}
    return config


def time_hold(hold, img_chrono):

    img1 = "https://img.icons8.com/?size=512&id=116643&format=png"
    img2 = "https://img.icons8.com/?size=512&id=116607&format=png"
    img3 = "https://img.icons8.com/?size=512&id=116609&format=png"
    img4 = "https://img.icons8.com/?size=512&id=116615&format=png"
    img5 = "https://img.icons8.com/?size=512&id=116620&format=png"
    img_hold = "https://cdn-icons-png.flaticon.com/512/5261/5261318.png"
    list_chrono_imgs = [img5, img4, img3, img2, img1]
    col0, col1, col2 = st.columns(3)
    with col0:
        hold.image(img_hold, width=60)
        
    with col1:
        img_chrono.image()


        
import streamlit.components.v1 as components

def ChangeButtonColour(widget_label, font_color, background_color='transparent'):
    htmlstr = f"""
        <script>
            var elements = window.parent.document.querySelectorAll('button');
            for (var i = 0; i < elements.length; ++i) {{ 
                if (elements[i].innerText == '{widget_label}') {{ 
                    elements[i].style.color ='{font_color}';
                    elements[i].style.background = '{background_color}'
                }}
            }}
        </script>
        """
    components.html(f"{htmlstr}", height=0, width=0)