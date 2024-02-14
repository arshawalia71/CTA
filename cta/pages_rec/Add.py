import streamlit as st
from datetime import datetime, date
import utils as utl
import ast
#import st_aggrid as ag
#from decimal import Decimal
#import json
#from pathlib import Path
#import os
#import sys
#import requests

#this is the function that gets called when the add button is clicked in the navbar
def load_view():
    # Assuming utl.sidebar_component() is a function
    

    utl.sidebar_component() #adds the navbar to the top of the page
    #the below code takes care of the condition that contract end date must be atleast a year after start date
    today = date.today()
    endDate = date(today.year + 1, today.month, today.day)
    endDate = today.replace(today.year + 1)

    #collect the project details
    st.header("Enter the project details")
    st.info("Please fill in all the flagged fields")
    col1, col2, col3,col4 = st.columns(4)
    
    query_params = st.experimental_get_query_params() #gets the parameters from query url
    token = query_params["token"][0] #Is being used to direct us back to the view page and in views.py
    if "payload" in query_params:
        query_params = query_params["payload"][0]
        query_params = ast.literal_eval(query_params)
        query_params[13].append(None)
    
    dim_tables = ["bcs", "aes", "budgettypes", "csms", "gdcpms", "gdcstatuses", "gdctas", "industryverticals",
                "onshorepms", "pmreviews", "projectengagements", "scs", "subscriptions", "tcs", "tiers"]
    #The below code takes care of all the quaters that need to be displayed as a dropdown
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    quarters = {12:'Q1', 1:'Q1', 2:'Q1', 3:'Q2', 4:'Q2', 5:'Q2',6:'Q3', 7:'Q3', 8:'Q3', 9:'Q4', 10:'Q4', 11:'Q4'}
    if currentMonth == 12:
        year = currentYear + 1
        prevYear = currentYear
    else:
        year = currentYear
    
    if quarters[currentMonth] == 'Q1':
        prevYear = currentYear - 1
    else:
        prevYear = currentYear

    if((currentMonth - 3)==-2):
        correct_currentMonth = 10
    elif((currentMonth - 3)==-1):
        correct_currentMonth = 11
    elif((currentMonth - 3)==0):
        correct_currentMonth = 12
    else:
        correct_currentMonth = currentMonth-3


    with st.form("addForm", clear_on_submit=True):
        #the queryparams[x] is where we're fetching the values of the dimension tables that we got in our payload
        dr_no = col1.text_input(":triangular_flag_on_post: DR #")
        region = col2.selectbox(":triangular_flag_on_post: Region", ["AMER", "EMEA", "APAC"])
        quarter = col3.selectbox(":triangular_flag_on_post: Quarter", [quarters[currentMonth]+" "+str(year), quarters[correct_currentMonth]+" "+str(prevYear)])
        vertical = col4.selectbox(":triangular_flag_on_post: Industry Vertical", query_params[7])
        project = col1.text_input(":triangular_flag_on_post: Project Name")
        tier = col2.selectbox(":triangular_flag_on_post: Tier", query_params[14])
        contract_start_date = col3.date_input(":triangular_flag_on_post: Contract start date")
        contract_end_date = col4._date_input(":triangular_flag_on_post: Contract end date", value=endDate)
        budget_start_date = col1.date_input(":triangular_flag_on_post: Budget start date")
        budget_end_date = col2.date_input(":triangular_flag_on_post: Budget end date")
        ownership = col3.text_input(":triangular_flag_on_post: Ownership")
        project_type = col4.selectbox("Project Type", query_params[10])
        subscription = col1.selectbox("Subscription", query_params[12])
        stage = col2.text_input("Stage")
        onshore_pm = col3.selectbox("Onshore PM", query_params[8])
        gdc_pm = col4.selectbox("GDC PM", query_params[4])
        gdc_ta = col1.selectbox("GDC TA", query_params[6])
        tc1 = col2.selectbox("TC1", query_params[13])
        tc2 = col3.selectbox("TC2", query_params[13], index = len(query_params[13])-1)
        #bc_as_pm = col4.text_input("BC as PM")
        bc = col4.selectbox("BC", query_params[0])
        ae = col1.selectbox("AE", query_params[1])
        sc = col2.selectbox("SC", query_params[11])
        csm = col3.selectbox("CSM", query_params[3])
        budget_type = col4.selectbox("Budget Type", query_params[2])
        total_budget = col1.number_input("Total budget",value=0,step=1,format="%d")
        budget_year = col2.number_input("Budget Year",value=0,step=1,format="%d")
        region_handoff_date = col3.date_input("Region Handoff Date")
        im_handoff_date = col4.date_input("IM Handoff Date")
        actual_cust_interaction_date = col1.date_input("Actual customer interaction date")
        #cust_kickoff = col2.date_input("Customer Kick Off")
        golive = col3.text_input("Go live")
        fwr = col4.text_input("FWR")
        hours_actuals = col1.number_input("Hours actuals",value=0,step=1,format="%d")
        term = col2.number_input("Term",value=0,step=1,format="%d")
        #tenure_buckets = col3.text_input("Tenure buckets")
        #y = col1.text_input("Y")
        #z = col2.text_input("Z")
        gdc_status = col3.selectbox("GDC Status", query_params[5])
        pm_review = col4.selectbox("PM Review", query_params[9])
        # resource_assigned = col2.text_input("Resource assigned")
        comments = col2.text_input("Comments")

        form_filled = not (
            contract_start_date and contract_end_date and budget_end_date and budget_start_date and ownership and dr_no and region and quarter and vertical and project
        )

        
        if form_filled:
            st.error("Please fill all the mandatory fields before clicking on the add button")

        submit_button = st.form_submit_button("Add", disabled=form_filled)
        # Convert form data to JSON
        """def form_to_json(form_data):
            data = {}
            for element in form_data:
                if isinstance(element, tuple):
                    key = element[0]
                    value = element[1]
                    data[key] = value
            return data"""
        if submit_button and form_filled:
            
            # Process the form data here
            data = {"DR_Number":dr_no, "Region":region, "Quarter":quarter, "Project_Name":project, "Stage":stage, "Vertical":vertical, "Project type":project_type, "Subscription":subscription, "Tier":tier, "Contract_start_date": contract_start_date.strftime("%Y%m%d"),
                    "Contract_end_date":contract_end_date.strftime("%Y%m%d"), "Budget_start_date":budget_start_date.strftime("%Y%m%d"), "Budget_end_date":budget_end_date.strftime("%Y%m%d"),
                    "Total_budget":total_budget, "Budget_year":budget_year, "Budget_type":budget_type, "Region_handoff_date":region_handoff_date.strftime("%Y%m%d"), "IM_handover_date":im_handoff_date.strftime("%Y%m%d"), "Actual_customer_interaction_date":actual_cust_interaction_date.strftime("%Y%m%d"), "Go_live":golive, "FWR":fwr, "Hours_actuals":hours_actuals, "Term":term, 
                    "Ownership":ownership, "GDC Status":gdc_status, "PM review":pm_review, "Comments":comments, "BC":bc, "AE":ae, "CSM":csm, "SC":sc, "Onshore PM":onshore_pm, "GDC PM":gdc_pm, "GDC TA":gdc_ta, "TC 1":tc1, "TC 2":tc2}
            
            #st.write(data)
            #sending the data and the token through the request to the add.html page that will send it to the backend
            nav_script = """
                <meta http-equiv="refresh" content="0; url='%s'">
            """ % ('http://localhost:8000/auth/add?payload='+str(data)+'&token='+token)
            st.write(nav_script, unsafe_allow_html=True)

    