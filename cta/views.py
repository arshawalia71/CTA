#for documentation of the code refer to the technical guide

from django.shortcuts import render
from django.conf import settings
import requests
import django
from pathlib import Path
from django.shortcuts import redirect
from pyDataverse.api import NativeApi, Api
from .ms_dataverse import DataverseORM
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpRequest
import json
import streamlit as st
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import pandas as pd
from datetime import datetime, timedelta, time, date
from decimal import Decimal
import streamlit as st
import logging
from ast import literal_eval
logging.basicConfig(filename='example.log')
logging.debug('This message should go to the log file')

#from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

import os
import sys
from django.core.wsgi import get_wsgi_application
PROJECT_ROOT_DIR = Path(os.path.abspath(__file__)).parents[1]
DJANGO_ROOT_DIR = PROJECT_ROOT_DIR / "cta"

dims=[]

ms_identity_web = settings.MS_IDENTITY_WEB
@ms_identity_web.login_required
def name_details(request):
    print(request)
    username = request.identity_context_data.username
    return username

def index(request):
    """ms_identity_web.acquire_token_silently()
    global orm
    orm = DataverseORM(dynamics_url="https://org47c81eb7.crm.dynamics.com", access_token=ms_identity_web.id_data._access_token)
    user = name_details(request)
    print(user)
    return render(request, "auth/home.html", {'context':user})
    #return True
    #return render(request, "auth/status.html")"""
    if(request.identity_context_data.authenticated):

        ms_identity_web.acquire_token_silently()
        global orm
        orm = DataverseORM(dynamics_url="https://org47c81eb7.crm.dynamics.com", access_token=ms_identity_web.id_data._access_token)
        user = name_details(request)

        print(user)

        dim_tables = ["bcs", "aes", "budgettypes", "csms", "gdcpms", "gdcstatuses", "gdctas", "industryverticals",

                        "onshorepms", "pmreviews", "projectengagements", "scs", "subscriptions", "tcs", "tiers"]

        dim_tables = ["cr7c7_" + i for i in dim_tables]

    

        BC = []; AE = []; BudgetType = []; CSM = []; GDCPM = []; GDC_Status = []; GDCTA = []; Vertical = []; OnshorePM = [];

        PM_review = []; Project_type = []; SC = []; Subscription = []; TC = []; Tier = []

        global dims

        dims = [BC, AE, BudgetType, CSM, GDCPM, GDC_Status, GDCTA, Vertical, OnshorePM, PM_review, Project_type, SC, Subscription, TC, Tier]

        for m in range(len(dim_tables)):

    

            bc = orm.entity(dim_tables[m])

            bc = bc.query()

        

            for i in bc:

                if dim_tables[m] == "cr7c7_pmreviews":

                    dims[m].append(i["cr7c7_review"])

                elif dim_tables[m] == "cr7c7_gdcstatuses":

                    dims[m].append(i["cr7c7_gdc_status"])

                elif dim_tables[m] == "cr7c7_projectengagements":

                    dims[m].append(i["cr7c7_project_type"])

                elif dim_tables[m] == "cr7c7_budgettypes":

                    dims[m].append(i["cr7c7_budget_type"])
                elif dim_tables[m] == "cr7c7_subscriptions":

                    dims[m].append(i["cr7c7_subscription_type"])

                else:

                    name_cols = [k for k in list(i.keys()) if k.endswith("name")]

                

                    if len(name_cols) > 0:

                        dims[m].append(i[name_cols[0]])

        return render(request, "auth/home.html", {'context':user})
    else:
        return render(request, "auth/home_initial.html")
@ms_identity_web.login_required
def token_details(request):
    return render(request, 'auth/token.html')

@ms_identity_web.login_required
def call_ms_graph(request):
    ms_identity_web.acquire_token_silently()
    graph = 'https://graph.microsoft.com/v1.0/users'
    authZ = f'Bearer {ms_identity_web.id_data._access_token}'
    results = requests.get(graph, headers={'Authorization': authZ}).json()

    # trim the results down to 5 and format them.
    if 'value' in results:
        results ['num_results'] = len(results['value'])
        results['value'] = results['value'][:5]
    else:
        results['value'] =[{'displayName': 'call-graph-error', 'id': 'call-graph-error'}]
    return render(request, 'auth/call-graph.html', context=dict(results=results))

@ms_identity_web.login_required
def get_entities(request):
    ms_identity_web.acquire_token_silently()
    graph = 'https://org4a3a1dd4.api.crm.dynamics.com/api/data/v9.2/cr148_s2s_tables'
    authZ = f'Bearer {ms_identity_web.id_data._access_token}'
    results = requests.get(graph, headers={'Authorization': authZ}).json()

    # trim the results down to 5 and format them.
    if 'value' in results:
        pass
    else:
        results['value'] =[{'displayName': 'call-graph-error', 'id': 'call-graph-error'}]
    print(results['value'][0])
    query_params = '&'.join([f'name={item["name"]}' for item in results['value']])
    url = f'https://bgdaxjwbynxkobvuwmmt67.streamlit.app/Show?{query_params}'
    print(url)
    return render(request, 'auth/entities.html', {'url': url})


@ms_identity_web.login_required

def get_bulk(request):

    ms_identity_web.acquire_token_silently()

    orm = DataverseORM(dynamics_url="https://org47c81eb7.crm.dynamics.com", access_token=ms_identity_web.id_data._access_token)

    print("Request: ", request)

    df = pd.read_excel("C:\\Users\\arshaw\\Downloads\\call-graph\\cta\\Book2.xlsx", engine="openpyxl")
# C:\Users\arshaw\Downloads\call-graph\cta\Book2.xlsx
    data = df.to_json(orient='records')

    #data = json.loads(data)

    print(data)
            # project table name
    account = orm.entity("cr7c7_table3")

    '''

    columns= ['name', 'region', 'quarter', 'project_name', 'stage', 'industry_vertical', 'project_type', 'subscription', 'tier', 'contract_start_date@OData.Community.Display.V1.FormattedValue',

                'contract_end_date@OData.Community.Display.V1.FormattedValue', 'budget_start_date@OData.Community.Display.V1.FormattedValue', 'budget_end_date@OData.Community.Display.V1.FormattedValue',

                'total_budget', 'budget_year', 'budget_type', 'region_handoff_date@OData.Community.Display.V1.FormattedValue', 'im_handover_date@OData.Community.Display.V1.FormattedValue','actual_customer_interaction_date@OData.Community.Display.V1.FormattedValue',

                'cust_kick_off@OData.Community.Display.V1.FormattedValue', 'go_live', 'fwr', 'hours_actuals', 'term', 'tenure_buckets', 'ownership', 'gdc_status', '_review_id_value', 'comments', '_bc_id_value', 'ae',

                'csm', 'sc', 'onshore_pm', '_gdcpm_value', 'gdc_ta', '_tc_id_value', '_tc2_id_value']

    '''

    #dim_tables = ["bcs", "gdcpms", "pmreviews", "tcs"]  
# tcs,bcs,gdcpms
    dim_tables = ["table1", "table2", "table6"]

    dim_tables = ["cr7c7_" + i for i in dim_tables]

    columns= ['name', 'region', 'quarter', 'project_name', 'stage', 'industry_vertical', 'project_type', 'subscription', 'tier', 'contract_start_date',

                'contract_end_date', 'budget_start_date', 'budget_end_date',

                'total_budget', 'budget_year', 'budget_type', 'region_handoff_date', 'im_handover_date','actual_customer_interaction_date',

                'go_live', 'fwr', 'hours_actuals', 'term', 'ownership', 'gdc_status', 'pmreview',  'comments', 'BC_id@odata.bind', 'ae',

                'csm', 'sc', 'onshore_pm', 'GDCPM@odata.bind', 'gdc_ta', 'TC_id@odata.bind', 'TC2_id@odata.bind']

    columns = ["cr7c7_" + i for i in columns]

    data = json.loads(data)

    dates = ['Contract_start_date','Contract_end_date', 'Budget_start_date', 'Budget_end_date',

                'Region_handoff_date', 'IM_handover_date','Actual_customer_interaction_date']

    epoch = datetime(1970, 1, 1)

    for m in dim_tables:

 

        bc = orm.entity(m)

        #print(m)

        #print(accounts)

        field = m[6:]
# for tc
        if m == "cr7c7_table1":

            field = "tcid"
#for bcs
        elif m == "cr7c7_table2":

            field = "bcid"
# for gdcpm 
        elif m == "cr7c7_table6":

            field = "gdcpmid"

        keys = {"bcid":"BC", "gdcpmid":"GDC PM", "tcid":"TC 1"}

       

        for i in range(len(data)):

           

            if keys[field] in data[i].keys():

                name = data[i][keys[field]]

                if name is not None:

                   

                    if m == "cr7c7_table1":

                        filter_exp = "cr7c7_tc_name" + " eq '" + name + "'"  

                    elif m == "cr7c7_table2":

                        filter_exp = "cr7c7_bc_name" + " eq '" + name + "'"

                    elif m == "cr7c7_table6":

                        filter_exp = "cr7c7_gdc_pm_name" + " eq '" + name + "'"

                    q = bc.query(filter_expression = filter_exp)

                    print(q[0])

                    data[i][keys[field]] = "/"+m+"("+q[0]["cr7c7_"+field]+")"

                    #print("/"+m+"("+q[0]["cr7c7_"+field + "id"]+")")

                    if m == "cr7c7_tcs":

                       

                        if "TC 2" in data[i].keys() and data[i]["TC 2"] is not None:

                            name = data[i]["TC 2"]

                            filter_exp = "cr7c7_tc_name" + " eq '" + name + "'"  

                            q = bc.query(filter_expression = filter_exp)

 

                            data[i][keys[field]] = "/"+m+"("+q[0]["cr7c7_"+field]+")"

    for x in range(len(data)):

        for date_x in dates:

            if data[x][date_x] is not None:

               

                edm_decimal = Decimal(data[x][date_x])

 

                date_string = str(edm_decimal)

                year = int(date_string[:4])

                month = int(date_string[4:6])

                day = int(date_string[6:8])

                date_object = epoch + timedelta(milliseconds=data[x][date_x])

                #date_object = date(year, month, day)

                #datetime_object = datetime.combine(date_object, time_object)

                #datetime_object = datetime_object.strftime("%m-%d-%Y %I:%M %p")

                datetime_object = date_object.strftime("%m-%d-%Y")

                print(datetime_object)

               

                data[x][date_x] = datetime_object

               

    columns = dict(zip(data[0].keys(), columns))

 

    for k, v in columns.items():

        for i in range(len(data)):

            for old_name in data[i].copy():

                if old_name == 'TC 2' and data[i]['TC 2'] is None:

                    data[i]["cr7c7_TC2_id"] = data[i].pop(old_name)

                elif k == old_name:

                    data[i][v] = data[i].pop(old_name)

   

    print(data)

    created_account  = account.create(data)

    url = f'https://bgdaxjwbynxkobvuwmmt67.streamlit.app/Search?cr7c7_projects'

    return render(request, 'auth/search_2.html', {'token': ms_identity_web.id_data._access_token})
#@ms_identity_web.login_required
def get_tables(request):
    #ms_identity_web.acquire_token_silently()
    access_token = request.GET["token"]
    orm = DataverseORM(dynamics_url="https://org47c81eb7.crm.dynamics.com", access_token=access_token)
    #api = NativeApi("https://org47c81eb7.crm.dynamics.com", ms_identity_web.id_data._access_token)
    #dv = Api("https://org47c81eb7.crm.dynamics.com", ms_identity_web.id_data._access_token)
    #resp = api.get_info_version()
    #print(dv.get_entities())
    #table = request.GET["name"]
    table = "cr7c7_projects"
    #account = orm.entity("cr7c7_projects")
    accounts = orm.entity(table)
    accounts = accounts.query()
    
    if table=="cr7c7_projects":
        dim_tables = ["tcs", "bcs", "gdcpms",]
        
        dim_tables = ["cr7c7_" + i for i in dim_tables]
        
        for m in dim_tables:
 
            bc = orm.entity(m)
            #print(m)
            #print(accounts)
            field = '_'+m
            field = field[:-1]
            bc_ent = bc.query()
            #print(tcs_ent)
            bcs = {}
            if m == "cr7c7_tcs":
                for i in bc_ent:
                    bcs[i["cr7c7_techconsultantid"]] = i["cr7c7_tc_name"]
            elif m == "cr7c7_gdcpms":
                for i in bc_ent:
                    bcs[i["cr7c7_gdc_pm_id"]] = i["cr7c7_gdc_pm_name"]
            else:
                for i in bc_ent:
                    bcs[i["cr7c7_bc_id"]] = i["cr7c7_bc_name"]
            
            for i in range(len(accounts)):
                if "@odata.etag" in accounts[i].keys():
                    del accounts[i]["@odata.etag"]
                if m == "cr7c7_tcs":
                    field = "_cr7c7_tc_id"
                    key = [key for key in dict(accounts[i]).keys() if key.startswith(field)]
                else:
                    key = [key for key in dict(accounts[i]).keys() if key.startswith(field)]
                if m == "cr7c7_tcs" and len(key) > 1 and accounts[i][key[0]] is not None and accounts[i][key[1]] is not None:
                    #accounts[i]["_cr7c7_tc_id_value"] = bcs[accounts[i]["_cr7c7_tc_id_value@OData.Community.Display.V1.FormattedValue"]]
            
                    #if accounts[i]["_cr7c7_tc2_id_value"] is not None:
                    #   accounts[i]["_cr7c7_tc2_id_value"] = bcs[accounts[i]["_cr7c7_tc2_id_value@OData.Community.Display.V1.FormattedValue"]]

                    #field = "_cr7c7_tc_id"
                    #key = [key for key in dict(accounts[i]).keys() if key.startswith(field)]
                    accounts[i][key[1]] = bcs[accounts[i][key[0]]]
                    if accounts[i]["_cr7c7_tc2_id_value"] is not None:
                       accounts[i]["_cr7c7_tc2_id_value"] = bcs[accounts[i]["_cr7c7_tc2_id_value@OData.Community.Display.V1.FormattedValue"]]
                else:
                    if len(key) > 1 and accounts[i][key[0]] is not None and accounts[i][key[1]] is not None:
                        accounts[i][key[1]] = bcs[accounts[i][key[0]]]
                '''
                j = dict(accounts[i])
                if "@odata.etag" in accounts[i].keys():
                    del accounts[i]["@odata.etag"]
                #if j['_cr7c7_bc_id_value'] is not None:
                if len(key) > 1 and j[key[0]] is not None and j[key[1]] is not None:
                    
                    #filter_exp = "cr7c7_bc_id eq '" + j["_cr7c7_bc_id_value@OData.Community.Display.V1.FormattedValue"]+"'"
                    #print(key[0], key[1])
                    
                    if key[1] == "_cr7c7_tc_id_value":
                        filter_exp = "cr7c7_techconsultantid" + " eq '" + j[key[0]] + "'"
                        print(filter_exp)
                    #print(filter_exp)
                    #q = bc.query(filter_expression=filter_exp, select_fields=["cr7c7_bc_name"])
                    q = bc.query(filter_expression=filter_exp)
                    #print(q)
                    
                    #accounts[i]["_cr7c7_bc_id_value"] = dict(q[0])["cr7c7_bc_name"]
                    
                    #accounts[i][key[1]] = dict(q[0])["cr7c7_bc_name"]
                    
                    name_cols = [k for k in list(q[0].keys()) if k.endswith("name")]
                    accounts[i][key[1]] = dict(q[0])[name_cols[0]]

                if m == "cr7c7_tcs":
                    field = "_cr7c7_tc2_id"
                    key = [key for key in dict(accounts[i]).keys() if key.startswith(field)]
                    #print(key)
                    if len(key) > 1 and j[key[0]] is not None and j[key[1]] is not None:
                        filter_exp = "cr7c7_techconsultantid" + " eq '" + j[key[0]] + "'"
                        q = bc.query(filter_expression=filter_exp)
                        name_cols = [k for k in list(q[0].keys()) if k.endswith("name")]
                        accounts[i][key[1]] = dict(q[0])[name_cols[0]]
                    field = "_cr7c7_tc_id"
                    key = [key for key in dict(accounts[0]).keys() if key.startswith(field)]
                '''
    query_params = '&'.join([[f'{key}={value}' for key, value in dict(l).items()] for l in accounts][0])
    #response = requests.post('http://localhost:8501/Search', json=accounts)
    #url = f'http://localhost:8501/Search?{query_params}'
    print(len(list(accounts)))
    #return render(request, 'auth/search_2.html', {'context': accounts})
    '''if response.status_code == 200:
        return HttpResponse(status=200)
    else:
        return HttpResponseNotFound("<h1>Page not found</h1>")'''
    return JsonResponse(accounts, safe=False)
    
#@ms_identity_web.login_required
def get_journey(request):
    token = request.GET["token"]
    
    #ms_identity_web.acquire_token_silently()
    orm = DataverseORM(dynamics_url="https://org47c81eb7.crm.dynamics.com", access_token=token)

    table = "cr7c7_journeies"
    #account = orm.entity("cr7c7_projects")
    accounts = orm.entity(table)
    projects=orm.entity("cr7c7_projects")
    data=request.GET["data"]
    result=request.GET["dr_number"]
    filter_exp = "cr7c7_name eq '" + result +"'"
    account_id = projects.query(filter_expression=filter_exp)[0]["cr7c7_projectid"]
    print(account_id)
    filter_exp = "_cr7c7_projectid_value eq '"+account_id+"'"
    accounts = accounts.query(filter_expression=filter_exp)
    print(accounts)
    
    print("Dr:", result, type(result))
    """dim_tables = ["cr7c7_projectstateses", "cr7c7_reasonfordelaies"]
    for m in dim_tables:
        bc = orm.entity(m)
        field = '_'+m
        field = field[:-1]

        bc_ent = bc.query()
        bcs = {}
        
        if m == "cr7c7_projectstateses":
            for i in bc_ent:
                bcs[i["cr7c7_stateid"]] = i["cr7c7_states"]
        else:
            for i in bc_ent:
                bcs[i["cr7c7_reasonid"]] = i["cr7c7_reason"]

        for i in range(len(accounts)):
            #print(accounts[i])
            if "@odata.etag" in accounts[i].keys():
                del accounts[i]["@odata.etag"]
            if m == "cr7c7_projectstateses" and accounts[i]["_cr7c7_stateid_value"] is not None:
                    accounts[i]["_cr7c7_stateid_value"] = bcs[accounts[i]["_cr7c7_stateid_value@OData.Community.Display.V1.FormattedValue"]]
            
            elif m == "cr7c7_reasonfordelaies" and accounts[i]["_cr7c7_reason_for_delay_value"] is not None:
                accounts[i]["_cr7c7_reason_for_delay_value"] = bcs[accounts[i]["_cr7c7_reason_for_delay_value@OData.Community.Display.V1.FormattedValue"]]
        for i in accounts:
            if(str(i["_cr7c7_projectid_value@OData.Community.Display.V1.FormattedValue"])!=result):
                accounts.remove(i)"""
    for i in range(len(accounts)):
            if "@odata.etag" in accounts[i].keys():
                del accounts[i]["@odata.etag"]
    print(data)             
    print(accounts)
    return render(request, 'auth/journey.html', {'context': accounts,'proj_record':data,'fromadd':False, 'token':token})


@ms_identity_web.login_required
def add_record(request):
    ms_identity_web.acquire_token_silently()
    orm = DataverseORM(dynamics_url="https://org47c81eb7.crm.dynamics.com", access_token=ms_identity_web.id_data._access_token)
    print("Request: ", request.GET["payload"])
    
    data = request.GET["payload"]
    #data = json.loads(data)
    token=request.GET["token"]
    account = orm.entity("cr7c7_projects")
    '''
    columns= ['name', 'region', 'quarter', 'project_name', 'stage', 'industry_vertical', 'project_type', 'subscription', 'tier', 'contract_start_date@OData.Community.Display.V1.FormattedValue',
                'contract_end_date@OData.Community.Display.V1.FormattedValue', 'budget_start_date@OData.Community.Display.V1.FormattedValue', 'budget_end_date@OData.Community.Display.V1.FormattedValue', 
                'total_budget', 'budget_year', 'budget_type', 'region_handoff_date@OData.Community.Display.V1.FormattedValue', 'im_handover_date@OData.Community.Display.V1.FormattedValue','actual_customer_interaction_date@OData.Community.Display.V1.FormattedValue',
                'cust_kick_off@OData.Community.Display.V1.FormattedValue', 'go_live', 'fwr', 'hours_actuals', 'term', 'tenure_buckets', 'ownership', 'gdc_status', '_review_id_value',  'comments', '_bc_id_value', 'ae',
                'csm', 'sc', 'onshore_pm', '_gdcpm_value', 'gdc_ta', '_tc_id_value', '_tc2_id_value']
    '''
    #dim_tables = ["bcs", "gdcpms", "pmreviews", "tcs"]  
    dim_tables = ["tcs", "bcs", "gdcpms"] 
    dim_tables = ["cr7c7_" + i for i in dim_tables]
    columns= ['name', 'region', 'quarter', 'project_name', 'stage', 'industry_vertical', 'project_type', 'subscription', 'tier', 'contract_start_date',
                'contract_end_date', 'budget_start_date', 'budget_end_date', 
                'total_budget', 'budget_year', 'budget_type', 'region_handoff_date', 'im_handover_date','actual_customer_interaction_date',
                'go_live', 'fwr', 'hours_actuals', 'term', 'ownership', 'gdc_status', 'pmreview',  'comments', 'BC_id@odata.bind', 'ae',
                'csm', 'sc', 'onshore_pm', 'GDCPM@odata.bind', 'gdc_ta', 'TC_id@odata.bind', 'TC2_id@odata.bind']
    columns = ["cr7c7_" + i for i in columns]
    data = data.replace("'", '"').replace('\\"', '"').replace('""', 'null').replace('None', 'null')
    print(data)
    data = json.loads(data)
    data1=data.copy()
    print(data)
    dates = ['Contract_start_date','Contract_end_date', 'Budget_start_date', 'Budget_end_date', 
                'Region_handoff_date', 'IM_handover_date','Actual_customer_interaction_date',
            ]
    epoch = datetime(1991, 1, 1)
    for m in dim_tables:

        bc = orm.entity(m)
        #print(m)
        #print(accounts)
        field = m[6:]
        if m == "cr7c7_tcs":
            field = "tcid"
        elif m == "cr7c7_bcs":
            field = "bcid"
        elif m == "cr7c7_gdcpms":
            field = "gdcpmid"
        keys = {"bcid":"BC", "gdcpmid":"GDC PM", "tcid":"TC 1"}
        
        if keys[field] in data.keys():
            name = data[keys[field]]
            if name is not None:
                
                if m == "cr7c7_tcs":
                    filter_exp = "cr7c7_tc_name" + " eq '" + name + "'"   
                elif m == "cr7c7_bcs":
                    filter_exp = "cr7c7_bc_name" + " eq '" + name + "'"
                elif m == "cr7c7_gdcpms":
                    filter_exp = "cr7c7_gdc_pm_name" + " eq '" + name + "'"
                q = bc.query(filter_expression = filter_exp)
                print(q[0])
                data[keys[field]] = "/"+m+"("+q[0]["cr7c7_"+field]+")"
                #print("/"+m+"("+q[0]["cr7c7_"+field + "id"]+")")
                if m == "cr7c7_tcs":
                    
                    if "TC 2" in data.keys() and data["TC 2"] is not None:
                        name = data["TC 2"]
                        filter_exp = "cr7c7_tc_name" + " eq '" + name + "'"   
                        q = bc.query(filter_expression = filter_exp)

                        data[keys[field]] = "/"+m+"("+q[0]["cr7c7_"+field]+")"
                
    
    time_object = time(0, 0)
    for date_x in dates:
        if data[date_x] is not None:
            print(date_x, data[date_x])
            edm_decimal = Decimal(data[date_x])

            date_string = str(edm_decimal)
            year = int(date_string[:4])
            month = int(date_string[4:6])
            day = int(date_string[6:8])

            date_object = date(year, month, day)
            datetime_object = date_object.strftime("%m-%d-%Y")
            print(datetime_object)
            data1[date_x] = datetime_object
            data[date_x] = datetime_object
                
    columns = dict(zip(data.keys(), columns))

    
    for k, v in columns.items():
        for old_name in data.copy():
            if old_name == 'TC 2' and data['TC 2'] is None:
                data["cr7c7_TC2_id"] = data.pop(old_name)
            elif k == old_name:
                data[v] = data.pop(old_name)
            
    print(data)
    created_account  = account.create(data)
    data=str(data)
    return render(request, 'auth/journey.html',{'context':[],'proj_record':data1,'fromadd':True,'token':token})

@ms_identity_web.login_required
def get_dropdowns(request):
    #redirect('/')
    #print("Dropdown")
    ms_identity_web.acquire_token_silently()
    #print(request.META.get('Authorization'))
    #orm = DataverseORM(dynamics_url="https://org47c81eb7.crm.dynamics.com", access_token=request.META.get('Authorization'))
    #print(ms_identity_web.id_data._access_token)
    orm = DataverseORM(dynamics_url="https://org47c81eb7.crm.dynamics.com", access_token=ms_identity_web.id_data._access_token)
    dim_tables = ["bcs", "aes", "budgettypes", "csms", "gdcpms", "gdcstatuses", "gdctas", "industryverticals",
                      "onshorepms", "pmreviews", "projectengagements", "scs", "subscriptions", "tcs", "tiers"]
    dim_tables = ["cr7c7_" + i for i in dim_tables]
    global dims
    if len(dims)==0:
        BC = []; AE = []; BudgetType = []; CSM = []; GDCPM = []; GDC_Status = []; GDCTA = []; Vertical = []; OnshorePM = []; 
        PM_review = []; Project_type = []; SC = []; Subscription = []; TC = []; Tier = []
        dims = [BC, AE, BudgetType, CSM, GDCPM, GDC_Status, GDCTA, Vertical, OnshorePM, PM_review, Project_type, SC, Subscription, TC, Tier]
        for m in range(len(dim_tables)):

            bc = orm.entity(dim_tables[m])
            bc = bc.query()
            
            for i in bc:
                if dim_tables[m] == "cr7c7_pmreviews":
                    dims[m].append(i["cr7c7_review"])
                elif dim_tables[m] == "cr7c7_gdcstatuses":
                    dims[m].append(i["cr7c7_gdc_status"])
                elif dim_tables[m] == "cr7c7_projectengagements":
                    dims[m].append(i["cr7c7_project_type"])
                elif dim_tables[m] == "cr7c7_budgettypes":
                    dims[m].append(i["cr7c7_budget_type"])
                elif dim_tables[m] == "cr7c7_subscriptions":
                    dims[m].append(i["cr7c7_subscription_type"])
                else:
                    name_cols = [k for k in list(i.keys()) if k.endswith("name")]
                    
                    if len(name_cols) > 0:
                        dims[m].append(i[name_cols[0]])
    print(dims)
    #return render(request, 'auth/add.html', {'context': dims})
    return render(request, 'auth/add.html', {'context': dims,'token':ms_identity_web.id_data._access_token})

@ms_identity_web.login_required
def get_dropdowns_journey(request):
    #redirect('/')
    #print("Dropdown")
    dr_number = request.GET["dr_number"]
    ms_identity_web.acquire_token_silently()
    orm = DataverseORM(dynamics_url="https://org47c81eb7.crm.dynamics.com", access_token=ms_identity_web.id_data._access_token)
    dim_tables = ["eventses"]
    dim_tables = ["cr7c7_" + i for i in dim_tables]

    delay=[]; state = []; event = []
    dims = [event, delay, state]
    for m in range(len(dim_tables)):

        bc = orm.entity(dim_tables[m])
        bc = bc.query()
        
        for i in bc:
            if dim_tables[m] == "cr7c7_projectstateses":
                dims[m].append(i["cr7c7_states"])
            elif dim_tables[m] == "cr7c7_reasonfordelaies":
                dims[m].append(i["cr7c7_reason"])
            elif dim_tables[m] == "cr7c7_eventses":
                dims[m].append(i["cr7c7_eventname"])
    print(dims)
    #return render(request, 'auth/add.html', {'context': dims})
    return render(request, 'auth/add_journey.html', {'context': dims, 'dr_number':dr_number})

def get_dropdowns_journey_update(request):
    #redirect('/')
    #print("Dropdown")
    #dr_number = request.GET["dr_number"]
    access_token = request.GET["token"]
    orm = DataverseORM(dynamics_url="https://org47c81eb7.crm.dynamics.com", access_token=access_token)
    
    dim_tables = ["eventses"]
    dim_tables = ["cr7c7_" + i for i in dim_tables]

    delay=[]; state = []; event = []
    dims = [event, delay, state]
    for m in range(len(dim_tables)):

        bc = orm.entity(dim_tables[m])
        bc = bc.query()
        
        for i in bc:
            if dim_tables[m] == "cr7c7_eventses":
                dims[m].append(i["cr7c7_eventname"])
    print(dims)
    #return render(request, 'auth/add.html', {'context': dims})
    return JsonResponse(dims, safe=False)

def get_dropdowns_update(request):
    access_token = request.GET["token"]
    orm = DataverseORM(dynamics_url="https://org47c81eb7.crm.dynamics.com", access_token=access_token)
    dim_tables = ["bcs", "aes", "budgettypes", "csms", "gdcpms", "gdcstatuses", "gdctas", "industryverticals",
                      "onshorepms", "pmreviews", "projectengagements", "scs", "subscriptions", "tcs", "tiers"]
    dim_tables = ["cr7c7_" + i for i in dim_tables]
    global dims
    if(len(dims))==0:
        BC = []; AE = []; BudgetType = []; CSM = []; GDCPM = []; GDC_Status = []; GDCTA = []; Vertical = []; OnshorePM = []; 
        PM_review = []; Project_type = []; SC = []; Subscription = []; TC = []; Tier = []
        dims = [BC, AE, BudgetType, CSM, GDCPM, GDC_Status, GDCTA, Vertical, OnshorePM, PM_review, Project_type, SC, Subscription, TC, Tier]
        for m in range(len(dim_tables)):

            bc = orm.entity(dim_tables[m])
            bc = bc.query()
            
            for i in bc:
                if dim_tables[m] == "cr7c7_pmreviews":
                    dims[m].append(i["cr7c7_review"])
                elif dim_tables[m] == "cr7c7_gdcstatuses":
                    dims[m].append(i["cr7c7_gdc_status"])
                elif dim_tables[m] == "cr7c7_projectengagements":
                    dims[m].append(i["cr7c7_project_type"])
                elif dim_tables[m] == "cr7c7_subscriptions":
                    dims[m].append(i["cr7c7_subscription_type"])
                elif dim_tables[m] == "cr7c7_budgettypes":
                    dims[m].append(i["cr7c7_budget_type"])
                else:
                    name_cols = [k for k in list(i.keys()) if k.endswith("name")]
                    
                    if len(name_cols) > 0:
                        dims[m].append(i[name_cols[0]])
    print(dims)
    #return render(request, 'auth/add.html', {'context': dims})
    return JsonResponse(dims, safe=False)

@ms_identity_web.login_required
def get_token(request):
    ms_identity_web.acquire_token_silently()
    
    #orm = DataverseORM(dynamics_url="https://org47c81eb7.crm.dynamics.com", access_token=ms_identity_web.id_data._access_token)
    print(ms_identity_web.id_data._access_token)
    return render(request, "auth/search_2.html", {'token':ms_identity_web.id_data._access_token})

@ms_identity_web.login_required
def update_project(request):
    ms_identity_web.acquire_token_silently()
    orm = DataverseORM(dynamics_url="https://org47c81eb7.crm.dynamics.com", access_token=ms_identity_web.id_data._access_token)
    
    data = request.GET["payload"]
    token = request.GET["token"]
    #data = json.loads(data)
    print(data)
    account = orm.entity("cr7c7_projects")
    dim_tables = ["tcs", "bcs", "gdcpms"] 
    dim_tables = ["cr7c7_" + i for i in dim_tables]
    columns= ['name', 'region', 'quarter', 'project_name', 'stage', 'industry_vertical', 'project_type', 'subscription', 'tier', 'contract_start_date',
                'contract_end_date', 'budget_start_date', 'budget_end_date', 
                'total_budget', 'budget_year', 'budget_type', 'region_handoff_date', 'im_handover_date','actual_customer_interaction_date',
                 'go_live', 'fwr', 'hours_actuals', 'term', 'tenure_buckets', 'ownership', 'gdc_status', 'pmreview',  'comments', 'BC_id@odata.bind', 'ae',
                'csm', 'sc', 'onshore_pm', 'GDCPM@odata.bind', 'gdc_ta', 'TC_id@odata.bind', 'TC2_id@odata.bind']
    columns = ["cr7c7_" + i for i in columns]
    data = data.replace("'", '"').replace('\\"', '"').replace('""', 'null')
    data = json.loads(data)
    data1=data.copy()
    print(data)
    dr_number = data["DR_Number"]
    filter_exp = "cr7c7_name eq '" + data["DR_Number"] +"'"
    account_id = account.query(filter_expression=filter_exp)[0]["cr7c7_projectid"]
    dates = ['Contract_start_date','Contract_end_date', 'Budget_start_date', 'Budget_end_date', 
                'Region_handoff_date', 'IM_handover_date','Actual_customer_interaction_date',
            ]
    epoch = datetime(1991, 1, 1)
    for m in dim_tables:

        bc = orm.entity(m)
        #print(m)
        #print(accounts)
        field = m[6:]
        if m == "cr7c7_tcs":
            field = "tcid"
        elif m == "cr7c7_bcs":
            field = "bcid"
        elif m == "cr7c7_gdcpms":
            field = "gdcpmid"
        keys = {"bcid":"BC", "gdcpmid":"GDC PM", "tcid":"TC 1"}
        
        if keys[field] in data.keys():
            name = data[keys[field]]
            if name is not None:
                
                if m == "cr7c7_tcs":
                    filter_exp = "cr7c7_tc_name" + " eq '" + name + "'"   
                elif m == "cr7c7_bcs":
                    filter_exp = "cr7c7_bc_name" + " eq '" + name + "'"
                elif m == "cr7c7_gdcpms":
                    filter_exp = "cr7c7_gdc_pm_name" + " eq '" + name + "'"
                q = bc.query(filter_expression = filter_exp)
                print(q[0])
                data[keys[field]] = "/"+m+"("+q[0]["cr7c7_"+field]+")"
                #print("/"+m+"("+q[0]["cr7c7_"+field + "id"]+")")
                if m == "cr7c7_tcs":
                    
                    if "TC 2" in data.keys() and data["TC 2"] is not None:
                        name = data["TC 2"]
                        filter_exp = "cr7c7_tc_name" + " eq '" + name + "'"   
                        q = bc.query(filter_expression = filter_exp)
                        print(q)
                        data["TC 2"] = "/"+m+"("+q[0]["cr7c7_"+field]+")"
    
    time_object = time(0, 0)
    for date_x in dates:
        if data[date_x] is not None:
            print(date_x, data[date_x])
            edm_decimal = Decimal(data[date_x])

            date_string = str(edm_decimal)
            year = int(date_string[:4])
            month = int(date_string[4:6])
            day = int(date_string[6:8])

            date_object = date(year, month, day)
            #datetime_object = datetime.combine(date_object, time_object)
            datetime_object = date_object.strftime("%m-%d-%Y")
            print(datetime_object)
            #datetime_offset = epoch + timedelta(milliseconds=datetime_object)
            #formatted_datetime = datetime_offset.strftime("%m-%d-%Y %I:%M %p")
            #data[date_x] = formatted_datetime
            
            data[date_x] = datetime_object
            data1[date_x]=datetime_object
                
    columns = dict(zip(data.keys(), columns))

    
    for k, v in columns.items():
        for old_name in data.copy():
            if k == old_name:
                data[v] = data.pop(old_name)
    columns= ['name', 'region', 'quarter', 'project_name', 'stage', 'industry_vertical', 'project_type', 'subscription', 'tier', 'contract_start_date',

                'contract_end_date', 'budget_start_date', 'budget_end_date',

                'total_budget', 'budget_year', 'budget_type', 'region_handoff_date', 'im_handover_date','actual_customer_interaction_date',

                'cust_kick_off', 'go_live', 'fwr', 'hours_actuals', 'term', 'tenure_buckets', 'ownership', 'gdc_status', 'pmreview',  'comments', 'BC_id@odata.bind', 'ae',

                'csm', 'sc', 'onshore_pm', 'GDCPM@odata.bind', 'gdc_ta', 'TC_id@odata.bind', 'TC2_id@odata.bind']

    columns = ["cr7c7_" + i for i in columns]
    columns1 = ["DR_Number", "Region", "Quarter", "Project_Name", "Stage", "Vertical", "Project type", "Subscription", "Tier", "Contract_start_date", "Contract_end_date", "Budget_start_date", "Budget_end_date",
            "Total_budget", "Budget_year", "Budget_type", "Region_handoff_date", "IM_handover_date", "Actual_customer_interaction_date", "Go_live", "FWR", "Hours_actuals", "Term", "Tenure_buckets",
            "Ownership", "GDC Status", "PM review",  "Comments", "BC", "AE", "CSM", "SC", "Onshore PM", "GDC PM", "GDC TA", "TC 1", "TC 2"]
    print(data)
    created_account  = account.update(entity_id=account_id, entity_data=data)
    project1 = {}
    for key, value in data.items():
        if key in columns:
            index = columns.index(key)
            if index < len(columns1):
                new_key = columns1[index]
                project1[new_key] = value
    print(project1)
    url = f'https://bgdaxjwbynxkobvuwmmt67.streamlit.app/?nav=Search&cr7c7_projects'
    http_request = HttpRequest()
    http_request.method = 'GET'  # Set the request method, e.g., 'GET', 'POST', etc.
    http_request.GET = {'data': str(data1), 'dr_number': dr_number, 'token':ms_identity_web.id_data._access_token}
    return get_journey(http_request)
    return render(request, 'auth/search_2.html', {'url': url})
    

@ms_identity_web.login_required
def get_audit(request):
    ms_identity_web.acquire_token_silently()
    orm = DataverseORM(dynamics_url="https://org47c81eb7.crm.dynamics.com", access_token=ms_identity_web.id_data._access_token)
    
    dr_number = request.GET["payload"]
    account = orm.entity("cr7c7_projects")

    filter_exp = "cr7c7_name eq '" + dr_number +"'"
    account_id = account.query(filter_expression=filter_exp)[0]["cr7c7_projectid"]
    print(account_id)
    #changes = account.audit("cr7c7_projectid", account_id)
    filter_exp = "objecttypecode eq 'cr7c7_project' and _objectid_value eq '"+account_id+"'"
    filter_exp = "_objectid_value eq '"+account_id+"'"
    changes = account.audit(filter_expression=filter_exp)["value"]
    print(changes)
    url = f'https://bgdaxjwbynxkobvuwmmt67.streamlit.app/?nav=Audit&payload='+json.dumps(changes)
    return render(request, 'auth/audit.html', {'context':changes})


@ms_identity_web.login_required
def add_journey(request):
    ms_identity_web.acquire_token_silently()
    orm = DataverseORM(dynamics_url="https://org47c81eb7.crm.dynamics.com", access_token=ms_identity_web.id_data._access_token)
    print("Request: ", request.GET["payload"])
    #data = {"Journey_ID":journey, "Health":health, "Event":event, "Date":date,"TTV":ttv, "Reason_for_dormancy":dormancy,"SHO2":sho2, "Reason_for_delay":delay, "State":state}
    data = request.GET["payload"]
    #data = json.loads(data)
    
    account = orm.entity("cr7c7_journeies")
    '''
    columns= ['name', 'region', 'quarter', 'project_name', 'stage', 'industry_vertical', 'project_type', 'subscription', 'tier', 'contract_start_date@OData.Community.Display.V1.FormattedValue',
                'contract_end_date@OData.Community.Display.V1.FormattedValue', 'budget_start_date@OData.Community.Display.V1.FormattedValue', 'budget_end_date@OData.Community.Display.V1.FormattedValue', 
                'total_budget', 'budget_year', 'budget_type', 'region_handoff_date@OData.Community.Display.V1.FormattedValue', 'im_handover_date@OData.Community.Display.V1.FormattedValue','actual_customer_interaction_date@OData.Community.Display.V1.FormattedValue',
                'cust_kick_off@OData.Community.Display.V1.FormattedValue', 'go_live', 'fwr', 'hours_actuals', 'term', 'tenure_buckets', 'ownership', 'gdc_status', '_review_id_value',  'comments', '_bc_id_value', 'ae',
                'csm', 'sc', 'onshore_pm', '_gdcpm_value', 'gdc_ta', '_tc_id_value', '_tc2_id_value']
    '''
    #dim_tables = ["bcs", "gdcpms", "pmreviews", "tcs"]  
    dim_tables = ["projects"]
    dim_tables = ["cr7c7_" + i for i in dim_tables]
    #columns= ['health', 'event', 'eventdate', 'ttv', 'reason_for_dormancy', 'sho2', 'Reason_for_Delay@odata.bind', 'StateID@odata.bind', 'ProjectID@odata.bind']
    columns= ['event', 'eventdate', 'comments', 'ProjectID@odata.bind']
    columns = ["cr7c7_" + i for i in columns]
    data = data.replace("'", '"').replace('\\"', '"').replace('""', 'null').replace('None', 'null')
    #print(data)
    data = json.loads(data)
    #print(data)
    dr_number = data["ProjectID"]
    dates = ['Date']
    epoch = datetime(1991, 1, 1)
    for m in dim_tables:

        bc = orm.entity(m)
        #print(m)
        #print(accounts)
        field = m[6:]
        if m == "cr7c7_projects":
            field = "projectid"
        
        keys = {"reasonfordelayid":"Reason_for_delay", "projectstatesid":"State", "projectid":"ProjectID"}
        
        if keys[field] in data.keys():
            name = data[keys[field]]
            if name is not None:
                
                if m == "cr7c7_reasonfordelaies":
                    filter_exp = "cr7c7_reason" + " eq '" + name + "'"   
                elif m == "cr7c7_projectstateses":
                    filter_exp = "cr7c7_states" + " eq '" + name + "'"
                elif m == "cr7c7_projects":
                    filter_exp = "cr7c7_name" + " eq '" + name + "'"
                
                q = bc.query(filter_expression = filter_exp)
                print(q[0])
                data[keys[field]] = "/"+m+"("+q[0]["cr7c7_"+field]+")"
                #print("/"+m+"("+q[0]["cr7c7_"+field + "id"]+")")
                
    for date_x in dates:
        if data[date_x] is not None:
            print(date_x, data[date_x])
            edm_decimal = Decimal(data[date_x])

            date_string = str(edm_decimal)
            year = int(date_string[:4])
            month = int(date_string[4:6])
            day = int(date_string[6:8])

            date_object = date(year, month, day)
            datetime_object = date_object.strftime("%m-%d-%Y")
            print(datetime_object)
            data[date_x] = datetime_object
                
    columns = dict(zip(data.keys(), columns))

    
    for k, v in columns.items():
        for old_name in data.copy():
            if k == old_name:
                data[v] = data.pop(old_name)
            

    print(data)
    created_account  = account.create(data)
    acc = orm.entity("cr7c7_projects")
    filter_exp = "cr7c7_name eq '" + dr_number +"'"
       
    project = acc.query(filter_expression = filter_exp)[0]
    del project["@odata.etag"]
    
    columns = ["DR_Number", "Region", "Quarter", "Project_Name", "Stage", "Vertical", "Project type", "Subscription", "Tier", "Contract_start_date", "Contract_end_date", "Budget_start_date", "Budget_end_date",
            "Total_budget", "Budget_year", "Budget_type", "Region_handoff_date", "IM_handover_date", "Actual_customer_interaction_date", "Go_live", "FWR", "Hours_actuals", "Term", "Tenure_buckets",
            "Ownership", "GDC Status", "PM review",  "Comments", "BC", "AE", "CSM", "SC", "Onshore PM", "GDC PM", "GDC TA", "TC 1", "TC 2"]

    columns_to_keep = ['cr7c7_name', 'cr7c7_region', 'cr7c7_quarter', 'cr7c7_project_name', 'cr7c7_stage', 'cr7c7_industry_vertical', 'cr7c7_project_type', 'cr7c7_subscription', 'cr7c7_tier', 'cr7c7_contract_start_date@OData.Community.Display.V1.FormattedValue',
                    'cr7c7_contract_end_date@OData.Community.Display.V1.FormattedValue', 'cr7c7_budget_start_date@OData.Community.Display.V1.FormattedValue', 'cr7c7_budget_end_date@OData.Community.Display.V1.FormattedValue', 
                    'cr7c7_total_budget', 'cr7c7_budget_year', 'cr7c7_budget_type', 'cr7c7_region_handoff_date@OData.Community.Display.V1.FormattedValue', 'cr7c7_im_handover_date@OData.Community.Display.V1.FormattedValue','cr7c7_actual_customer_interaction_date@OData.Community.Display.V1.FormattedValue',
                     'cr7c7_go_live', 'cr7c7_fwr', 'cr7c7_hours_actuals', 'cr7c7_term', 'cr7c7_tenure_buckets', 'cr7c7_ownership', 'cr7c7_gdc_status', 'cr7c7_pmreview', 'cr7c7_comments', '_cr7c7_bc_id_value', 'cr7c7_ae',
                    'cr7c7_csm', 'cr7c7_sc', 'cr7c7_onshore_pm', '_cr7c7_gdcpm_value', 'cr7c7_gdc_ta', '_cr7c7_tc_id_value', '_cr7c7_tc2_id_value']
    
    dim_tables = ["tcs", "bcs", "gdcpms"]
        
    dim_tables = ["cr7c7_" + i for i in dim_tables] 
    for m in dim_tables:

        bc = orm.entity(m)
        #print(m)
        #print(accounts)
        field = '_'+m
        field = field[:-1]
        bc_ent = bc.query()
        #print(tcs_ent)
        bcs = {}
        if m == "cr7c7_tcs":
            for i in bc_ent:
                bcs[i["cr7c7_techconsultantid"]] = i["cr7c7_tc_name"]
        elif m == "cr7c7_gdcpms":
            for i in bc_ent:
                bcs[i["cr7c7_gdc_pm_id"]] = i["cr7c7_gdc_pm_name"]
        else:
            for i in bc_ent:
                bcs[i["cr7c7_bc_id"]] = i["cr7c7_bc_name"]
        
        if m == "cr7c7_tcs":
            field = "_cr7c7_tc_id"
            key = [key for key in project.keys() if key.startswith(field)]
        else:
            key = [key for key in project.keys() if key.startswith(field)]
        if m == "cr7c7_tcs" and len(key) > 1 and project[key[0]] is not None and project[key[1]] is not None:
            
            project[key[1]] = bcs[project[key[0]]]
            if project["_cr7c7_tc2_id_value"] is not None:
                project["_cr7c7_tc2_id_value"] = bcs[project["_cr7c7_tc2_id_value@OData.Community.Display.V1.FormattedValue"]]
        else:
            if len(key) > 1 and project[key[0]] is not None and project[key[1]] is not None:
                project[key[1]] = bcs[project[key[0]]]
    project1 = {}
    for key, value in project.items():
        if key in columns_to_keep:
            index = columns_to_keep.index(key)
            if index < len(columns):
                new_key = columns[index]
                project1[new_key] = value
    print(project1)
    http_request = HttpRequest()
    http_request.method = 'GET'  # Set the request method, e.g., 'GET', 'POST', etc.
    http_request.GET = {'data': str(project1), 'dr_number': dr_number, 'token':ms_identity_web.id_data._access_token}
    return get_journey(http_request)

@ms_identity_web.login_required
def update_journey(request):
    ms_identity_web.acquire_token_silently()
    orm = DataverseORM(dynamics_url="https://org47c81eb7.crm.dynamics.com", access_token=ms_identity_web.id_data._access_token)
    
    data = request.GET["payload"]
    id = request.GET["id"]
    #data = json.loads(data)
    print(data)
    account = orm.entity("cr7c7_journeies")
    dim_tables = ["projects"]
    dim_tables = ["cr7c7_" + i for i in dim_tables]
    #columns= ['health', 'event', 'eventdate', 'ttv', 'reason_for_dormancy', 'sho2', 'Reason_for_Delay@odata.bind', 'StateID@odata.bind', 'ProjectID@odata.bind']
    columns= ['event', 'eventdate', 'comments', 'ProjectID@odata.bind']
    columns = ["cr7c7_" + i for i in columns]
    data = data.replace("'", '"').replace('\\"', '"').replace('""', 'null').replace('None', 'null')
    #print(data)
    data = json.loads(data)
    print(data)
    filter_exp = "cr7c7_name eq '" + id +"'"
    account_id = account.query(filter_expression=filter_exp)[0]["cr7c7_journeyid"]
    dates = ['Date']
    epoch = datetime(1991, 1, 1)
    for m in dim_tables:

        bc = orm.entity(m)
        #print(m)
        #print(accounts)
        field = m[6:]
        if m == "cr7c7_reasonfordelaies":
            field = "reasonfordelayid"
        elif m == "cr7c7_projectstateses":
            field = "projectstatesid"
        elif m == "cr7c7_projects":
            field = "projectid"
        
        keys = {"reasonfordelayid":"Reason_for_delay", "projectstatesid":"State", "projectid":"ProjectID"}
        
        if keys[field] in data.keys():
            name = data[keys[field]]
            if name is not None:
                
                if m == "cr7c7_reasonfordelaies":
                    filter_exp = "cr7c7_reason" + " eq '" + name + "'"   
                elif m == "cr7c7_projectstateses":
                    filter_exp = "cr7c7_states" + " eq '" + name + "'"
                elif m == "cr7c7_projects":
                    dr_number = name
                    filter_exp = "cr7c7_name" + " eq '" + name + "'"
                
                q = bc.query(filter_expression = filter_exp)
                print(q[0])
                data[keys[field]] = "/"+m+"("+q[0]["cr7c7_"+field]+")"
                #print("/"+m+"("+q[0]["cr7c7_"+field + "id"]+")")
    
    for date_x in dates:
        if data[date_x] is not None:
            print(date_x, data[date_x])
            edm_decimal = Decimal(data[date_x])

            date_string = str(edm_decimal)
            year = int(date_string[:4])
            month = int(date_string[4:6])
            day = int(date_string[6:8])

            date_object = date(year, month, day)
            datetime_object = date_object.strftime("%m-%d-%Y")
            print(datetime_object)
            data[date_x] = datetime_object
                
    columns = dict(zip(data.keys(), columns))

    
    for k, v in columns.items():
        for old_name in data.copy():
            if k == old_name:
                data[v] = data.pop(old_name)
    
    print(data)
    created_account  = account.update(entity_id=account_id, entity_data=data)
    acc = orm.entity("cr7c7_projects")
    filter_exp = "cr7c7_name eq '" +dr_number+"'"
       
    project = acc.query(filter_expression = filter_exp)[0]
    
    del project["@odata.etag"]
    
    columns = ["DR_Number", "Region", "Quarter", "Project_Name", "Stage", "Vertical", "Project type", "Subscription", "Tier", "Contract_start_date", "Contract_end_date", "Budget_start_date", "Budget_end_date",
            "Total_budget", "Budget_year", "Budget_type", "Region_handoff_date", "IM_handover_date", "Actual_customer_interaction_date", "Go_live", "FWR", "Hours_actuals", "Term", "Tenure_buckets",
            "Ownership", "GDC Status", "PM review",  "Comments", "BC", "AE", "CSM", "SC", "Onshore PM", "GDC PM", "GDC TA", "TC 1", "TC 2"]

    columns_to_keep = ['cr7c7_name', 'cr7c7_region', 'cr7c7_quarter', 'cr7c7_project_name', 'cr7c7_stage', 'cr7c7_industry_vertical', 'cr7c7_project_type', 'cr7c7_subscription', 'cr7c7_tier', 'cr7c7_contract_start_date@OData.Community.Display.V1.FormattedValue',
                    'cr7c7_contract_end_date@OData.Community.Display.V1.FormattedValue', 'cr7c7_budget_start_date@OData.Community.Display.V1.FormattedValue', 'cr7c7_budget_end_date@OData.Community.Display.V1.FormattedValue', 
                    'cr7c7_total_budget', 'cr7c7_budget_year', 'cr7c7_budget_type', 'cr7c7_region_handoff_date@OData.Community.Display.V1.FormattedValue', 'cr7c7_im_handover_date@OData.Community.Display.V1.FormattedValue','cr7c7_actual_customer_interaction_date@OData.Community.Display.V1.FormattedValue',
                     'cr7c7_go_live', 'cr7c7_fwr', 'cr7c7_hours_actuals', 'cr7c7_term', 'cr7c7_tenure_buckets', 'cr7c7_ownership', 'cr7c7_gdc_status', 'cr7c7_pmreview',  'cr7c7_comments', '_cr7c7_bc_id_value', 'cr7c7_ae',
                    'cr7c7_csm', 'cr7c7_sc', 'cr7c7_onshore_pm', '_cr7c7_gdcpm_value', 'cr7c7_gdc_ta', '_cr7c7_tc_id_value', '_cr7c7_tc2_id_value']
    
    dim_tables = ["tcs", "bcs", "gdcpms",]
        
    dim_tables = ["cr7c7_" + i for i in dim_tables] 
    for m in dim_tables:

        bc = orm.entity(m)
        #print(m)
        #print(accounts)
        field = '_'+m
        field = field[:-1]
        bc_ent = bc.query()
        #print(tcs_ent)
        bcs = {}
        if m == "cr7c7_tcs":
            for i in bc_ent:
                bcs[i["cr7c7_techconsultantid"]] = i["cr7c7_tc_name"]
        elif m == "cr7c7_gdcpms":
            for i in bc_ent:
                bcs[i["cr7c7_gdc_pm_id"]] = i["cr7c7_gdc_pm_name"]
        else:
            for i in bc_ent:
                bcs[i["cr7c7_bc_id"]] = i["cr7c7_bc_name"]
        
        if m == "cr7c7_tcs":
            field = "_cr7c7_tc_id"
            key = [key for key in project.keys() if key.startswith(field)]
        else:
            key = [key for key in project.keys() if key.startswith(field)]
        if m == "cr7c7_tcs" and len(key) > 1 and project[key[0]] is not None and project[key[1]] is not None:
            
            project[key[1]] = bcs[project[key[0]]]
            if project["_cr7c7_tc2_id_value"] is not None:
                project["_cr7c7_tc2_id_value"] = bcs[project["_cr7c7_tc2_id_value@OData.Community.Display.V1.FormattedValue"]]
        else:
            if len(key) > 1 and project[key[0]] is not None and project[key[1]] is not None:
                project[key[1]] = bcs[project[key[0]]]
    project1 = {}
    for key, value in project.items():
        if key in columns_to_keep:
            index = columns_to_keep.index(key)
            if index < len(columns):
                new_key = columns[index]
                project1[new_key] = value
    print(project1)
    http_request = HttpRequest()
    http_request.method = 'GET'  # Set the request method, e.g., 'GET', 'POST', etc.
    http_request.GET = {'data': str(project1), 'dr_number': dr_number, 'token':ms_identity_web.id_data._access_token}
    return get_journey(http_request)

@ms_identity_web.login_required
def get_usecases(request):
    # Your view logic here
    ms_identity_web.acquire_token_silently()
    orm = DataverseORM(dynamics_url="https://org47c81eb7.crm.dynamics.com", access_token=ms_identity_web.id_data._access_token)
    
    data = request.GET["data"]
    # id = request.GET["id"]
    #data = json.loads(data)
    print(data)
    account = orm.entity("cr7c7_customer_usecases")
    # dim_tables = ["projects"]
    # dim_tables = ["cr7c7_" + i for i in dim_tables]
    # #columns= ['health', 'event', 'eventdate', 'ttv', 'reason_for_dormancy', 'sho2', 'Reason_for_Delay@odata.bind', 'StateID@odata.bind', 'ProjectID@odata.bind']
    # columns= ['department', 'implementationdate', 'stakeholderemail','name','summary', 'ProjectID@odata.bind']
    # columns = ["cr7c7_" + i for i in columns]
    # data = data.replace("'", '"').replace('\\"', '"').replace('""', 'null').replace('None', 'null')
    # #print(data)
    # data = json.loads(data)
    # print(data)
    # filter_exp = "cr7c7_name eq '" + id +"'"
    
    
    return render(request, 'auth/usecases.html', {'token':ms_identity_web.id_data._access_token})
