import streamlit as st
import random

    
    
#class sensor containing names, battery levels
def detect_sensor():
    """
    java code ?
    get all info when detecting devices
    """
    # get_battery_lvl
    # get_ble_lvl
    
    return ["MOTEN_04","MOTEN_06","MOTEN_17","MOTEN_33","MOTEN_14"]

def activate_sensors(sensor_id_list):
    st.success(f"sensors {sensor_id_list} have been activated successfully")
    pass
def stop_sensors(sensor_id_list):
    st.success(f"sensors {sensor_id_list} have been stopped successfully")
    pass
def reset_sensors(sensor_id_list):
    st.success(f"sensors {sensor_id_list} have been reset successfully")
    pass
def info_sensors(sensor_id_list):
    st.success(f"sensors {sensor_id_list} information...")
    pass

def get_battery_lvl(sensor_name): # or include it in the detect sensor function
    # query sensor and get battery level
    # choose the img url based on level
    lvl_imgs = [
        #"https://cdn-icons-png.flaticon.com/512/5179/5179282.png",
        #       "https://cdn-icons-png.flaticon.com/512/5179/5179269.png",
        #       "https://cdn-icons-png.flaticon.com/512/5179/5179255.png",
        #       "https://cdn-icons-png.flaticon.com/512/5179/5179198.png",
        #       "https://cdn-icons-png.flaticon.com/512/5179/5179324.png",
               "https://cdn-icons-png.flaticon.com/512/7822/7822695.png",
               "https://cdn-icons-png.flaticon.com/512/7822/7822691.png",
               "https://cdn-icons-png.flaticon.com/512/7822/7822720.png",
               "https://cdn-icons-png.flaticon.com/512/7822/7822697.png",
               "https://cdn-icons-png.flaticon.com/512/7822/7822699.png",
               "https://cdn-icons-png.flaticon.com/512/7822/7822701.png"]
    battery_level_img_path = random.choice(lvl_imgs)
    return battery_level_img_path

def get_ble_lvl(sensor_name): # or include it in the detect sensor function
    # query bluetooth web api
    # choose the img url based on level
    lvl_imgs = ["https://cdn-icons-png.flaticon.com/512/5604/5604620.png",
               "https://cdn-icons-png.flaticon.com/512/5604/5604616.png",
               "https://cdn-icons-png.flaticon.com/512/5604/5604627.png",
               "https://cdn-icons-png.flaticon.com/512/5604/5604631.png"]
    level_img_path = random.choice(lvl_imgs)
    return level_img_path