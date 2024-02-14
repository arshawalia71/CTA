import streamlit as st
from datetime import datetime
import ast
import requests
import utils as utl
#function is called when the update project record button is clicked
def update():
    utl.sidebar_component() #displays navbar component
    data = st.experimental_get_query_params()
    dataframe = data["payload"][0] #gets the record details of the selected record to be updated
    token = data["token"][0]
    #st.empty()
    dataframe = ast.literal_eval(dataframe)

    st.write("Update project")
    #st.write(dataframe[0])
    headers = {
        
            "Content-Type": "application/json",
            "OData-Version": "4.0",
            "OData-MaxVersion": "4.0",
            "Access-Control-Allow-Origin":"*",
            "Prefer": "return=representation, odata.include-annotations=OData.Community.Display.V1.FormattedValue"
        }
    #fetches the dropdowns of the different fields from the backend(views.py)
    resp = requests.get("http://localhost:8000/get_dropdowns_update", params = {"token":token}, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        print(data)
    query_params = data
    query_params[13].append(None)
    dim_tables = ["bcs", "aes", "budgettypes", "csms", "gdcpms", "gdcstatuses", "gdctas", "industryverticals",
                "onshorepms", "pmreviews", "projectengagements", "scs", "subscriptions", "tcs", "tiers"]
    print("dataframe",dataframe)
    dataframe = dataframe[0]
    #dataframe = dataframe.iloc[0,:]
    date_format = '%m/%d/%Y'
    col1, col2, col3,col4 = st.columns(4)
    # Existing code
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    quarters = {12: 'Q1', 1: 'Q1', 2: 'Q1', 3: 'Q2', 4: 'Q2', 5: 'Q2', 6: 'Q3', 7: 'Q3', 8: 'Q3', 9: 'Q4', 10: 'Q4', 11: 'Q4'}
    if currentMonth == 12:
        year = currentYear + 1
        prevYear = currentYear
    else:
        year = currentYear
    if quarters[currentMonth] == 'Q1':
        prevYear = currentYear - 1
    else:
        prevYear = currentYear

    # Check if the quarter is in the list and add it if not
    quarter = dataframe["Quarter"]

    correct_currentMonth = 0
    if((currentMonth - 3)==-2):
        correct_currentMonth = 10
    elif((currentMonth - 3)==-1):
        correct_currentMonth = 11
    elif((currentMonth - 3)==0):
        correct_currentMonth = 12
    else:
        correct_currentMonth = currentMonth-3

    if quarter not in [quarters[currentMonth] + " " + str(year), quarters[correct_currentMonth] + " " + str(prevYear)]:
        # Add the quarter to the list
        quarters_added = [quarter] + [quarters[currentMonth] + " " + str(year), quarters[correct_currentMonth] + " " + str(prevYear)]
    else:
        quarters_added = [quarters[currentMonth] + " " + str(year), quarters[correct_currentMonth] + " " + str(prevYear)]

    # Continue with your form creation
    with st.form("updateForm", clear_on_submit=True):
        dr_no = col1.text_input(":triangular_flag_on_post: DR #", value=dataframe["DR_Number"])
        region = col2.text_input(":triangular_flag_on_post: Region", value=dataframe["Region"])
        quarter = col3.selectbox(":triangular_flag_on_post: Quarter", quarters_added, index=quarters_added.index(quarter))

        vertical = col4.selectbox(":triangular_flag_on_post: Industry Vertical", query_params[7], index=query_params[7].index(dataframe["Vertical"]))
        project = col1.text_input(":triangular_flag_on_post: Project Name", value=dataframe["Project_Name"])
        tier = col2.selectbox(":triangular_flag_on_post: Tier", query_params[14], index=query_params[14].index(dataframe["Tier"]))
        contract_start_date = col4.date_input(":triangular_flag_on_post: Contract start date", value=datetime.strptime(dataframe["Contract_start_date"], date_format))
        contract_end_date = col1._date_input(":triangular_flag_on_post: Contract end date", value=datetime.strptime(dataframe["Contract_end_date"], date_format))
        budget_start_date = col2.date_input(":triangular_flag_on_post: Budget start date", value=datetime.strptime(dataframe["Budget_start_date"], date_format))
        budget_end_date = col3.date_input(":triangular_flag_on_post: Budget end date", value=datetime.strptime(dataframe["Budget_end_date"], date_format))
        ownership = col3.text_input(":triangular_flag_on_post: Ownership", value=dataframe["Ownership"])
        project_type = col4.selectbox("Project Type", query_params[10], index=query_params[10].index(dataframe["Project type"]))
        subscription = col4.selectbox("Subscription", query_params[12], index=query_params[12].index(dataframe["Subscription"]))
        stage = col1.text_input("Stage", value=dataframe["Stage"])
        onshore_pm = col2.selectbox("Onshore PM", query_params[8], index=query_params[8].index(dataframe["Onshore PM"]))
        gdc_pm = col3.selectbox("GDC PM", query_params[4], index=query_params[4].index(dataframe["GDC PM"]))
        gdc_ta = col4.selectbox("GDC TA", query_params[6], index=query_params[6].index(dataframe["GDC TA"]))
        # print("This is PRINTttttttttttttttttttttttttttttttttttttttttttttttttttttt", query_params)
        tc1 = col1.selectbox("TC1", query_params[13], index=query_params[13].index(dataframe["TC 1"]))
        tc2 = col2.selectbox("TC2", query_params[13], index=query_params[13].index(dataframe["TC 2"]))
        
        #bc_as_pm = col3.text_input("BC as PM", value=dataframe["DR_Number"])
        bc = col3.selectbox("BC", query_params[0], index=query_params[0].index(dataframe["BC"]))
        ae = col1.selectbox("AE", query_params[1], index=query_params[1].index(dataframe["AE"]))
        sc = col2.selectbox("SC", query_params[11], index=query_params[11].index(dataframe["SC"]))
        csm = col3.selectbox("CSM", query_params[3], index=query_params[3].index(dataframe["CSM"]))
        budget_type = col4.selectbox("Budget type", query_params[2], index=query_params[2].index(dataframe["Budget_type"]))
        total_budget = col1.number_input("Total budget",step=1,format="%d", value=dataframe["Total_budget"])
        budget_year = col2.number_input("Budget Year",step=1,format="%d", value=dataframe["Budget_year"])
        region_handoff_date = col3.date_input("Region Handoff Date", value=datetime.strptime(dataframe["Region_handoff_date"], date_format))
        im_handoff_date = col4.date_input("IM Handover Date", value=datetime.strptime(dataframe["IM_handover_date"], date_format))
        actual_cust_interaction_date = col1.date_input("Actual customer interaction date", value=datetime.strptime(dataframe["Actual_customer_interaction_date"], date_format))
        #cust_kickoff = col2.date_input("Customer Kick Off", value=datetime.strptime(dataframe["Cust_kick_off"], date_format))
        golive = col3.text_input("Go live", value=dataframe["Go_live"])
        fwr = col4.text_input("FWR", value=dataframe["FWR"])
        hours_actuals = col1.number_input("Hours actuals",step=1,format="%d", value=dataframe["Hours_actuals"])
        term = col2.number_input("Term",step=1,format="%d", value=dataframe["Term"])
        tenure_buckets = col3.text_input("Tenure buckets", value=dataframe["Tenure_buckets"])
        #y = col1.text_input("Y")
        #z = col2.text_input("Z")
        gdc_status = col3.selectbox("GDC Status", query_params[5], index=query_params[5].index(dataframe["GDC Status"]))
        pm_review = col4.selectbox("PM Review", query_params[9], index=query_params[9].index(dataframe["PM review"]))
        resource_assigned = col2.text_input("Resource assigned", value=dataframe["Resource_assigned"])
        comments = col1.text_input("Comments", value=dataframe["Comments"])

        form_filled = True
        if not (contract_start_date and contract_end_date and budget_end_date and budget_start_date and ownership and dr_no and region and quarter and vertical and project):
            form_filled = False
            st.error("Please fill all the mandatory fields")

        submit_button = st.form_submit_button("Update Project")
        if submit_button and form_filled:
            
            # Process the form data here
            data = {"DR_Number":dr_no, "Region":region, "Quarter":quarter, "Project_Name":project, "Stage":stage, "Vertical":vertical, "Project type":project_type, "Subscription":subscription, "Tier":tier, "Contract_start_date": contract_start_date.strftime("%Y%m%d"),
                    "Contract_end_date":contract_end_date.strftime("%Y%m%d"), "Budget_start_date":budget_start_date.strftime("%Y%m%d"), "Budget_end_date":budget_end_date.strftime("%Y%m%d"),
                    "Total_budget":total_budget, "Budget_year":budget_year, "Budget_type":budget_type, "Region_handoff_date":region_handoff_date.strftime("%Y%m%d"), "IM_handover_date":im_handoff_date.strftime("%Y%m%d"), "Actual_customer_interaction_date":actual_cust_interaction_date.strftime("%Y%m%d"),
                    "Go_live":golive, "FWR":fwr, "Hours_actuals":hours_actuals, "Term":term, "Tenure_buckets":tenure_buckets,
                    "Ownership":ownership, "GDC Status":gdc_status, "PM review":pm_review, "Resource_assigned":resource_assigned, "Comments":comments, "BC":bc, "AE":ae, "CSM":csm, "SC":sc, "Onshore PM":onshore_pm, "GDC PM":gdc_pm, "GDC TA":gdc_ta, "TC 1":tc1, "TC 2":tc2}
            print(data)
            
            st.write(data)
            nav_script = """
                <meta http-equiv="refresh" content="0; url='%s'">
            """ % ('http://localhost:8000/auth/update?payload='+str(data)+'&token='+token)
            st.write(nav_script, unsafe_allow_html=True) #sends the updated record fields to the backend