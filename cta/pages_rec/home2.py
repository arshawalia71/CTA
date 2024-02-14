import streamlit as st
import utils as utl

#this is the function that is executed once the user is authenticated
def load_view():
    query_params=st.experimental_get_query_params() 
    if len(query_params) > 0:
        if 'username' in query_params:
            query_params = query_params['username'][0] #gets the username from the mscall graph after authentication
            st.session_state['username']=query_params
    utl.sidebar_component()
    st.header("Welcome to Customer Tracking Application, " + st.session_state.username)
    st.markdown("<br style='line-height:100px;'>", unsafe_allow_html=True)
    st.header("DCPS")
    st.write("Adobe's Document Cloud Professional Services refers to a range of consulting and implementation services offered by Adobe to assist organizations in deploying and optimizing their use of Adobe Document Cloud. These services are designed to help organizations maximize the value and effectiveness of Adobe Document Cloud within their specific business environment.The Professional Services team at Adobe works closely with customers to understand their unique requirements, challenges, and goals. They provide expertise, guidance, and support throughout the implementation process to ensure a successful deployment of Adobe Document Cloud.")
#currently not being used can be used later to send username to different pages
"""def get_name():
    return st.session_state.username"""


