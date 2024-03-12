import streamlit as st
import ast
import utils as utl
#import st_aggrid as ag
#from decimal import Decimal
#import json
#from pathlib import Path
#import os
#from datetime import datetime
#import sys
#import requests


#this is the function that gets called when the add journey button is clicked
def load_view():
    utl.sidebar_component() #This function displays the navbar in this page
    st.header("Enter the journey details")
    st.info("Please fill in all the flagged fields")
    col1, col2, col3, col4= st.columns(4)
    query_params = st.experimental_get_query_params() #get the parameters from the url query
    if "drnumber" in query_params:
        dr_number = query_params["drnumber"][0]
    if "payload" in query_params:
        query_params = query_params["payload"][0]
        query_params = ast.literal_eval(query_params)
        query_params[1].append(None)

    with st.form("addForm", clear_on_submit=True):
        
        #journey = col1.text_input(":triangular_flag_on_post: Journey ID")
        
        event = col2.selectbox(":triangular_flag_on_post: Event", query_params[0])
        date_event = col3.date_input(":triangular_flag_on_post: Date of event")
        #the next few fields have been commented as they are not used in the journey table anymore
        #if needed in the future can add them back
        #health = col3.text_input("Health")
        #ttv = col1.text_input("TTV")
        #dormancy = col2.text_input("Reason for dormancy")
        #sho2 = col3.text_input("SHO2")
        #delay = col1.selectbox("Reason for delay", query_params[1])
        #state = col2.selectbox("State", query_params[2])
        comments = col2.text_input("Comments")

        form_filled = True
        if not (event and date_event):
            form_filled = False
            st.error("Please fill all the mandatory fields before clicking on the add button")

        submit_button = st.form_submit_button("Add")
        #the below function can be used in the future if needed 
        # to convert the form data into json format
        """def form_to_json(form_data):
            data = {}
            for element in form_data:
                if isinstance(element, tuple):
                    key = element[0]
                    value = element[1]
                    data[key] = value
            return data"""
        if submit_button and form_filled:
            print(date_event, date_event.strftime("%Y%m%d"))
            # Process the form data here
            #the below commented version is to process the columns in the old journey table
            #data = {"Health":health, "Event":event, "Date":date_event.strftime("%Y%m%d"),
            #"TTV":ttv, "Reason_for_dormancy":dormancy,"SHO2":sho2, "Reason_for_delay":delay, "State":state, "ProjectID":dr_number}
            #new journey table has only these 3 fields being processed
            data = {"Event":event, "Date":date_event.strftime("%Y%m%d"), "Comments": comments, "ProjectID":dr_number}
            #st.write always write the info onto the screen print() writes it onto the terminal
            st.write(data) 
            #the meta tag takes us to the mentioned url page. Here we're sending the form data we just collected as parameters to the html page through a payload that will pass it on to the backend(views.py)
            #views.py has a function that will put the data into the database
            nav_script = """
                <meta http-equiv="refresh" content="0; url='%s'">
            """ % ('https://bgdaxjwbynxkobvuwmmt67.streamlit.app/auth/add_journey?payload='+str(data))
            #navscript will be executed in the below st.write, the unsafe_allow_html must be true for it to be executable
            st.write(nav_script, unsafe_allow_html=True)
            #st.write("The record has been added successfully")
