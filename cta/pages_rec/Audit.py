import streamlit as st
import ast
import pandas as pd
import json
import utils as utl

#this function is called when the view record history button is clicked in search page
def load_view(): #it gets the audit history from the backend and displays it as a dataframe
    utl.sidebar_component() #add the navbar
    params = st.experimental_get_query_params() #get the parameters from url
    params = params["payload"][0] #get the values being passed to the payload variable
    data = ast.literal_eval(params) #converts the string to a list so that it can be iterated through
    
    # appendng the items with the old value and new value 
    for i in range(len(data)):
        data[i]["changes"] = []
        d = data[i]["changedata"]
        #print(d)
        if d != "False":
            d = d.replace("'", '"').replace('\\"', '"').replace("None", "null") #preprocessing so that the string can be converted into a dictionary or json format
            changed_data = json.loads(d)["changedAttributes"]
            for j in changed_data:
                l = [j["logicalName"], j["oldValue"], j["newValue"]]
                data[i]["changes"].append(l)
            

    # Create an empty list to hold the data for the DataFrame
    records = []

    # Iterate through each dictionary in the data list
    for item in data:
        if "changes" in item:
            user = item["_userid_value@OData.Community.Display.V1.FormattedValue"]
            action = item["operation@OData.Community.Display.V1.FormattedValue"]
            date = item["createdon@OData.Community.Display.V1.FormattedValue"]
            changes = item["changes"]

            # Iterate through each change in the 'changes' list and create a tuple for the MultiIndex
            for change in changes:
                attribute, old_val, new_val = change
                records.append((user, action, date, attribute, old_val, new_val))
    # Create a MultiIndex from the list of tuples
    index = pd.MultiIndex.from_tuples(records, names=["Modified by", "Action", "Date", "Attribute", "Old", "New"])
    df = pd.DataFrame(records, columns=["Modified by", "Action", "Date", "Attribute", "Old", "New"])
    st.write(df)