import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid
import requests
import base64
import io
import datetime
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import streamlit as st
from urllib.parse import quote
import utils as utl

#the below function can be used in the future if needed
#It can be used to provide a template so that users can download it and create their excel document to be uploaded in the same format
"""def get_excel_download_link(df, file_name):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.close()
    output.seek(0)
    excel_file = output.read()
    b64 = base64.b64encode(excel_file).decode()
    download_link = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{file_name}">template.xlsx</a>'
    return download_link"""

def UpdateProject(dataframe, token): #takes us to the update page while sending the selected record as payload so that it can be displayed
    dataframe = pd.DataFrame(dataframe.selected_rows) 
    dataframe = dataframe.to_dict('records')
    nav_script = """<meta http-equiv="refresh" content="0; url='%s'">""" % ('https://bgdaxjwbynxkobvuwmmt67.streamlit.app/?nav=update&payload='+str(dataframe)+'&token='+token)
    st.write(nav_script, unsafe_allow_html=True)
def viewHistory(dataframe): #sends the selected record to the backend to fetch its history
    dataframe = pd.DataFrame(dataframe.selected_rows)
    dataframe = dataframe.iloc[0,:]
    dr_no = dataframe["DR_Number"]
    nav_script = """
                    <meta http-equiv="refresh" content="0; url='%s'">
                """ % ('https://bgdaxjwbynxkobvuwmmt67.streamlit.app/auth/audit?payload='+str(dr_no)) #send the dr_no to query in the backend for history of that particular record
    st.write(nav_script, unsafe_allow_html=True)

def get_data(token):

    headers = {

       

            "Content-Type": "application/json",

            "OData-Version": "4.0",

            "OData-MaxVersion": "4.0",

            "Access-Control-Allow-Origin":"*",

            "Prefer": "return=representation, odata.include-annotations=OData.Community.Display.V1.FormattedValue"

        }

    global data

    if "Search" not in st.session_state:

        resp = requests.get("https://bgdaxjwbynxkobvuwmmt67.streamlit.app/get_tables", params = {"token":token}, headers=headers)

        if resp.status_code == 200:

            data = resp.json()

        st.session_state["Search"] = True

    return data
#this function gets executed when the search button is clicked in the navbar
def search():
    utl.sidebar_component() #adds the navbar
    st.title("Search")
    query_params = st.experimental_get_query_params()
    if len(query_params) > 0:
        if 'token' in query_params:
            token = query_params['token'][0] 
    st.session_state["token"]=token
    col1, col2, col3,col4,col5 = st.columns(5)
    # Create sample data
    button_style = """
    .button-text {
        font-size: 14px;
    }
    """
    # checkbox1 = "Single record"
    # conditionCheck1 = (checkbox1 == "Single record")
    # conditionCheck2 = (checkbox1 == "Multiple records")
    # Apply custom CSS using st.markdown
    st.markdown(f"<style>{button_style}</style>", unsafe_allow_html=True)
    # Create buttons with custom CSS class
    selected_items=pd.DataFrame()
    audit=col3.button("View record history")
    #adding a place holder that displays the doenload button once export is clicked on 
    pl=col5.empty()
    downall=col5.button("Export all to csv")
    button2=col2.button("View/update journey",help="View and Update the journies for the selected record",key="view_update_journey")
    addUsecase = col1.button("Add/View Usecases", key="add_usecases")
    
    update = col1.button("Update Project Record", key="update_project")
    #adding a place holder that displays the doenload button once export is clicked on 
    placeholder=col4.empty()
    downFilterRecords=col2.button("Download Filter Records",help="Download all the filtered rows",key="down_filter_records")
    download=placeholder.button("Export selected details" )
    error_msg=st.empty()
    query_params = st.experimental_get_query_params()
    #df = pd.read_excel("Template.xlsx")
        
    if len(query_params) > 0:
        if 'token' in query_params:
            query_params = query_params['token'][0] #fetch the token from the url query

    data = get_data(token) #need to use the token in the backend so send it here and gets the data from the project tables 
    df = pd.DataFrame(data)
    substrings = ["cr7c7_", "_cr7c7_"]
    for substring in substrings:
        df.columns = df.columns.str.replace(substring, '') #removing the cr7c7
    #if st.session_state["Table"] == "Project":
    #the below code replaces the column names from the database into column names of our choice
    columns = ["DR_Number", "Region", "Quarter", "Project_Name", "Stage", "Vertical", "Project type", "Subscription", "Tier", "Contract_start_date", "Contract_end_date", "Budget_start_date", "Budget_end_date",
            "Total_budget", "Budget_year", "Budget_type", "Region_handoff_date", "IM_handover_date", "Actual_customer_interaction_date", "Cust_kick_off", "Go_live", "FWR", "Hours_actuals", "Term", "Tenure_buckets",
            "Ownership", "GDC Status", "PM review", "Resource_assigned", "Comments", "BC", "AE", "CSM", "SC", "Onshore PM", "GDC PM", "GDC TA", "TC 1", "TC 2"]

    columns_to_keep = ['name', 'region', 'quarter', 'project_name', 'stage', 'industry_vertical', 'project_type', 'subscription', 'tier', 'contract_start_date@OData.Community.Display.V1.FormattedValue',
                    'contract_end_date@OData.Community.Display.V1.FormattedValue', 'budget_start_date@OData.Community.Display.V1.FormattedValue', 'budget_end_date@OData.Community.Display.V1.FormattedValue', 
                    'total_budget', 'budget_year', 'budget_type', 'region_handoff_date@OData.Community.Display.V1.FormattedValue', 'im_handover_date@OData.Community.Display.V1.FormattedValue','actual_customer_interaction_date@OData.Community.Display.V1.FormattedValue',
                    'cust_kick_off@OData.Community.Display.V1.FormattedValue', 'go_live', 'fwr', 'hours_actuals', 'term', 'tenure_buckets', 'ownership', 'gdc_status', 'pmreview', 'resource_assigned', 'comments', '_bc_id_value', 'ae',
                    'csm', 'sc', 'onshore_pm', '_gdcpm_value', 'gdc_ta', '_tc_id_value', '_tc2_id_value']

    df = df.loc[:, columns_to_keep]
    
    df.columns = columns


    # df['Contract_end_date'] = pd.to_datetime(df['Contract_end_date'])
    # view_expired = st.checkbox("View Expired Projects")
    # if view_expired:
    #     # Filter and display expired projects
    #     expired_projects = df[df['Contract_end_date'] < datetime.datetime.now()]
    #     builder = GridOptionsBuilder.from_dataframe(expired_projects)
    #     # Set the number of columns to be visible on load
    #     builder.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False, filter=True, resizable=True, suppressAutoSize=False, maxWidth=110,tooltip=True)
    #     builder.configure_side_bar()
    #     builder.configure_grid_options(domLayout='normal')  # Adjust the maxHeight and width as needed
    #     builder.configure_pagination(enabled=True,paginationPageSize=5)
    #     exp = builder.build()
    #     selected_items = AgGrid(df, gridOptions=exp)
    


    if 'button_state' not in st.session_state:
        st.session_state.button_state = False   
    #provides radio buttons that lets user choose their selection mode
    checkbox1=st.radio("Choose the selection mode ",horizontal=True,options=["Single record","Multiple records"],index=0)
    
    select_all = st.checkbox("Select All")
    

    #configuring the agGrid settings and building the agGrid to display the records

    builder = GridOptionsBuilder.from_dataframe(df)
    # Set the number of columns to be visible on load
    builder.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False, filter=True, resizable=True, suppressAutoSize=True, maxWidth=100,tooltip=True)
    builder.configure_side_bar()
    builder.configure_grid_options(domLayout='normal')  # Adjust the maxHeight and width as needed
    builder.configure_pagination(enabled=True,paginationPageSize=10)
    
    if(checkbox1=="Multiple records"):
        builder.configure_selection(selection_mode="multiple", use_checkbox=True, rowMultiSelectWithClick=False)
        go1=builder.build()
        selected_items = AgGrid(df, gridOptions=go1) #stores the agGrid state. The filter/selected columns/selected records etc
        print(" multiple: ",selected_items)
    else:
        builder.configure_selection(selection_mode="single", use_checkbox=True, rowMultiSelectWithClick=False)
        go = builder.build()
        selected_items = AgGrid(df, gridOptions=go)
        sel_col=(selected_items.column_state)
        print(" single: ",selected_items)
    
    
    #saves the state of the agGrid to use in the export functionality
    final_selected_items=selected_items
    final_all=selected_items
    #checks for the condition it only a single record is chosen when the View and update journey button is clicked
    if( button2 and (checkbox1=='Single record')): 
        selected_items1 = pd.DataFrame(selected_items.selected_rows) #gets the selected record
        selected_items1 = selected_items1.drop("_selectedRowNodeInfo", axis=1) #drops unwanted column
        #get the dr number of the record to fetch it's journey details by processing the info
        dr_number=selected_items1["DR_Number"]
        dr_number=str(dr_number).split()
        dr_number=dr_number[1] 
        #convert the record into json format to send it as a payload across to the backend as the project record needs to be displayed in the view page
        selected_items1=selected_items1.to_json()
        payload = selected_items1
        #quote function just converts it intoproper url format
        nav_script = """
            <meta http-equiv="refresh" content="0; url='%s'">
        """ % ('https://bgdaxjwbynxkobvuwmmt67.streamlit.app/auth/journey?data='+quote(str(payload))+'&dr_number='+quote(str(dr_number))+'&token='+quote(str(token)))

        st.write(nav_script, unsafe_allow_html=True) #sends the record along with its DR number to the journey.html file that sends it to backend
    
    

    if( addUsecase and (checkbox1=='Single record')): 
        selected_items1 = pd.DataFrame(selected_items.selected_rows) #gets the selected record
        selected_items1 = selected_items1.drop("_selectedRowNodeInfo", axis=1) #drops unwanted column
        #get the dr number of the record to fetch it's journey details by processing the info
        dr_number=selected_items1["DR_Number"]
        dr_number=str(dr_number).split()
        dr_number=dr_number[1] 
        
        #convert the record into json format to send it as a payload across to the backend as the project record needs to be displayed in the view page
        selected_items1=selected_items1.to_json()
        payload = selected_items1
        #quote function just converts it intoproper url format
        nav_script = """
            <meta http-equiv="refresh" content="0; url='%s'">
        """ % ('https://bgdaxjwbynxkobvuwmmt67.streamlit.app/get_usecases?data='+quote(str(payload))+'&dr_number='+quote(str(dr_number))+'&token='+quote(str(token)))

        st.write(nav_script, unsafe_allow_html=True) #sends the record along with its DR number to the journey.html file that sends it to backend
    
    
    
    # if downFilterRecords: 
    #     # When the "Export Selected Details" button is clicked 
    #     sel_col = None
    #     while sel_col is None:
    #         sel_col = final_selected_items.column_state

    #     sel_col = final_selected_items.column_state
    #     list1 = []

    #     # Get the selected rows into a DataFrame
    #     final_selected_items = pd.DataFrame(final_selected_items.selected_rows)

    #     # Check if "_selectedRowNodeInfo" column exists before dropping it
    #     if "_selectedRowNodeInfo" in final_selected_items.columns:
    #         final_selected_items = final_selected_items.drop("_selectedRowNodeInfo", axis=1)

    #     # Loop to identify columns to hide
    #     for i in sel_col:
    #         if i['hide'] == True:
    #             list1.append(i['colId'])

    #     # Drop the columns user doesn't want to see from the DataFrame
    #     for i in list1:
    #         final_selected_items.drop([i], axis=1, inplace=True)

    #     # Save the DataFrame to the user-specified location after converting it to CSV
    #     csv_data1 = final_selected_items.to_csv(index=False)
    #     placeholder.download_button("Download", data=csv_data1, mime="text/csv")

    #     # When the "Export Filtered Records" button is clicked 
    #     filters_applied = final_selected_items.query('_selectedRowNodeInfo.notna()')
        
    #     if not filters_applied.empty:
    #         # Export filtered records only if filters are applied
    #         csv_data_filtered = filters_applied.to_csv(index=False)
    #         placeholder.download_button("Download Filtered Records", data=csv_data_filtered, mime="text/csv")

    
    
    if download: #when export selected details button is clicked 
        sel_col=None
        while(sel_col==None):
            sel_col = final_selected_items.column_state
        sel_col=final_selected_items.column_state
        #above loop gets the column state from the agGrid
        list1=[]
        final_selected_items = pd.DataFrame(final_selected_items.selected_rows) #only the rows the user has selected is converted into a dataframe
        final_selected_items = final_selected_items.drop("_selectedRowNodeInfo", axis=1) #drops the initial unwanted column that displays the node index info
        #below loop adds all the columns the user has choosen to hide into a list
        for i in sel_col:
            if i['hide'] == True:
                list1.append(i['colId'])
        for i in list1:
            final_selected_items.drop([i],axis=1,inplace=True) #drop the columns user doesn't want to see from dataframe
        # Save the dataframe to the user-specified location after converting it to csv
        csv_data1=final_selected_items.to_csv(index=False)
        placeholder.download_button("Download",data=csv_data1,mime="text/csv")

    # if downFilterRecords:
        
    if downall: #when export all to csv is clicked
        #the commented code uses tkinter to give a dialog box but it needs to be in the main loop else cn click download button only once
        #root = tk.Tk()
        #root.withdraw()
        #file_path=filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        sel_col1=None
        #the below loop fetches all the columns that are in the agGrid displayed
        while(sel_col1==None):
            sel_col1 = final_all.column_state
        sel_col1=final_all.column_state
        list2=[]
        #appends all thecolumns the user has choosen to hide from the agGrid view
        for i in sel_col1:
            if i['hide'] == True:
                list2.append(i['colId'])
        for i in list2: #drop all the hidden columns from the dataframe
            df.drop([i],axis=1,inplace=True)
        csv_data=df.to_csv(index=False) #convert dataframe into a csv and download it to the user specified location
        pl.download_button("Download",data=csv_data,mime="text/csv")
    #takes care whether only the single record selection mode is ticked and calls the update project funtion else throws error msg
    #we also send the selected record along with the token as an argument to the function
    if update:
        if(checkbox1=='Single record'):

            UpdateProject(selected_items, token)
        else:
            error_msg.error("Only one record must be updated at a time. Please select a single record")
    #takes care whether only the single record selection mode is ticked and calls the viewhistory funtion else throws error msg
    if audit:
        if(checkbox1=='Single record'):
            viewHistory(selected_items) #send the selected record as an argument to the function
        else:
            error_msg.error("Only one record must be viewed at a time. Please select a single record")
