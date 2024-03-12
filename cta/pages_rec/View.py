import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid
import pandas as pd
import json
import utils as utl

def updateJourney(dataframe, token, dr_number): #takes us to the update_journey.py and executes the update function
    dataframe = pd.DataFrame(dataframe.selected_rows)
    dataframe = dataframe.to_dict('records')
    print(token)
    #sends the token and the selected record to be updated in the payload so that it can be picked up by the update function
    nav_script = """<meta http-equiv="refresh" content="0; url='%s'">""" % ('https://bgdaxjwbynxkobvuwmmt67.streamlit.app/?nav=Update_journey&payload='+str(dataframe)+'&token='+token+'&dr_number='+dr_number)
    st.write(nav_script, unsafe_allow_html=True)
def viewAndUpdateJourney(): #function gets executed when the view project and update journey button is clicked
    utl.sidebar_component() 
    query_params = st.experimental_get_query_params()
    #st.dataframe(dataframe)
    token=query_params['token'][0]
    if 'proj' in query_params:
        query_params1 = query_params['proj'][0]
        print(query_params)
        print("in if query params",query_params1)
    query_params1 = query_params1.replace("'", '"').replace('\\"', '"').replace("None", "null")
    print(query_params1,type(query_params1))         
    query_params1=json.loads(query_params1)
    st.header("Project:")
    col1,col2,col3,col4=st.columns(4)
    print(query_params['flag'][0],type(query_params['flag'][0]))
    if((query_params['flag'][0])=="False"):
        print("In the flag loop")
        print("this is queryparams1",query_params1)
        try:
            df= {key: value["0"] for key, value in query_params1.items()}
            df=pd.DataFrame(query_params1)
        except:
            df={key: value for key, value in query_params1.items()}
            df=pd.DataFrame(query_params1,index=[0])
    else:
        df={key: value for key, value in query_params1.items()}
        df=pd.DataFrame(query_params1,index=[0])
    st.write(df)
    print("query",query_params1)
    dr_number = query_params1["DR_Number"]
    if isinstance(dr_number, dict):
        dr_number = dr_number["0"]
    st.session_state["Table"] = "Journey"
    if len(query_params) > 0:
        if 'payload' in query_params:
            query_params = query_params['payload'][0]
            st.header("Journey:")
            coln1,coln2=st.columns(2)
            addjour=coln1.button("Add Journey")
            if addjour:
                nav_script = """
                    <meta http-equiv="refresh" content="0; url='%s'">
                """ % ('https://bgdaxjwbynxkobvuwmmt67.streamlit.app/get_dropdowns_journey?dr_number='+str(dr_number))
                st.write(nav_script, unsafe_allow_html=True)
            if(query_params=='[]'):
                st.write("No journey to display")
            else:
                query_params = query_params.replace("'", '"').replace('\\"', '"').replace("None", "null")
                query_params = json.loads(query_params)
                if query_params:
                    df = pd.DataFrame(query_params)
                    
                else:
                    st.write("No query parameters found.")

                substrings = ["cr7c7_", "_cr7c7_"]
                for substring in substrings:
                    df.columns = df.columns.str.replace(substring, '')
                
                print(df.columns)
                #columns = ["JourneyID", "Health", "Sales Handover Date", "PS Kick Off", "Planned Go Live", "Actual Go Live", "TTV", "Reason for dormancy", "On hold since", "SHO2", "ProjectID", "Reason for delay","State", "Cust kick off"]
                columns = ["JourneyID", "Event", "Date of event", "Comments"]    

                #columns_to_keep = ['name', 'health', 'event', "eventdate@OData.Community.Display.V1.FormattedValue",

                #                    'ttv', 'reason_for_dormancy', 'sho2', '_reason_for_delay_value', '_stateid_value']
                columns_to_keep = ['name','event', "eventdate@OData.Community.Display.V1.FormattedValue",'comments']
                df = df.loc[:, columns_to_keep]
                updatejour=coln2.button("Update Journey")
                df.columns = columns
                builder = GridOptionsBuilder.from_dataframe(df)
                builder.configure_selection(selection_mode="multiple", use_checkbox= True, rowMultiSelectWithClick=True)
                builder.configure_side_bar()
                go = builder.build()
                selected_items=AgGrid(df, gridOptions=go)
                if updatejour:
                    updateJourney(selected_items,token,dr_number)