import streamlit as st
from datetime import datetime
import json
import ast
import requests
import utils as utl

#function executed upon clicking the update journey button in the view page
def update():
    utl.sidebar_component() #add the navbar to the page top
    data = st.experimental_get_query_params()
    dataframe = data["payload"][0] #get the journey record to be updataed through the payload
    token = data["token"][0]
    dr_number = data["dr_number"][0] 
    #st.empty()
    dataframe = ast.literal_eval(dataframe)

    st.write("Update journey")
    #st.write(dataframe[0])
    headers = {
        
            "Content-Type": "application/json",
            "OData-Version": "4.0",
            "OData-MaxVersion": "4.0",
            "Access-Control-Allow-Origin":"*",
            "Prefer": "return=representation, odata.include-annotations=OData.Community.Display.V1.FormattedValue"
        }
    resp = requests.get("http://localhost:8000/get_dropdowns_journey_update", params = {"token":token}, headers=headers)
    #get all the dropdowns to update the record directly from backend 
    if resp.status_code == 200:
        data = resp.json()
        print(data)
    query_params = data
    query_params[1].append(None)
    query_params[2].append(None)
    #displaying the column fields 
    dataframe = dataframe[0]
    journey_id = dataframe["JourneyID"]
    date_format = '%m/%d/%Y'
    col1, col2, col3, col4 = st.columns(4)
    with st.form("updateForm", clear_on_submit=True):
        #event = col2.selectbox(":triangular_flag_on_post: Event", query_params[0], index = query_params[0].index(dataframe["Event"]))
        event = col2.selectbox("Event", [dataframe["Event"]])
        date_event = col3.date_input(":triangular_flag_on_post: Date of event", datetime.strptime(dataframe["Date of event"], date_format))
        '''health = col3.text_input("Health", value=dataframe["Health"])
        ttv = col1.text_input("TTV", value=dataframe["TTV"])
        dormancy = col2.text_input("Reason for dormancy", value=dataframe["Reason for dormancy"])
        sho2 = col3.text_input("SHO2", value=dataframe["SHO2"])
        delay = col1.selectbox("Reason for delay", query_params[1], index=query_params[1].index(dataframe["Reason for delay"]))
        state = col2.selectbox("State", query_params[2], index=query_params[2].index(dataframe["State"]))
        '''
        comments = col2.text_input("Comments", value=dataframe["Comments"])
        form_filled = True
        if not (event and date_event):
            form_filled = False
            st.error("Please fill all the mandatory fields")

        submit_button = st.form_submit_button("Update Journey")
        if submit_button and form_filled:
        
            # Process the form data here
            #data = {"Health":health, "Event":event, "Date":date_event.strftime("%Y%m%d"),
            #        "TTV":ttv, "Reason_for_dormancy":dormancy,"SHO2":sho2, "Reason_for_delay":delay, "State":state, "ProjectID":dr_number}

            data = {"Event":event, "Date":date_event.strftime("%Y%m%d"),"Comments":comments,"ProjectID":dr_number}
            print(data)
            st.write(data)
            nav_script = """
                <meta http-equiv="refresh" content="0; url='%s'">
            """ % ('http://localhost:8000/auth/update_journey?payload='+str(data)+'&id='+journey_id)
            st.write(nav_script, unsafe_allow_html=True) #send the update fields to the backend for updating through the update_journey.html