import streamlit as st
st.set_page_config(layout="wide") #makes sure the page occupies the entire space 
import utils as utl
from pages_rec import login,Search,Add,update,View,home2,Audit,Add_journey,Update_journey, usecases

#removes an error message when using plots
st.set_option('deprecation.showPyplotGlobalUse', False)

#NOTES: The port for the backend and related files is always 8000
# the port for frontend and ir's related files is always 8501.
# Make sure to use only these in the codes or you'll have to explicitly change them in all the files and the codebase givrn until now

#function that gets executed first when the application is started, called by default below
def navigation():
    #the utils.py file has the current route function that gives the route "?nav=route"
    route = utl.get_current_route()
    #conditional statements that take care of which function to be executed based on the route to display that particular page
    if route == "Home":
        home2.load_view()
    elif route == "Search":
        Search.search()
    elif route == "Add":
        Add.load_view()
    # elif route == "Report":
    #     Report.load_view()
    elif route=="update":
        update.update()
    elif route == "Usecases":
        usecases.load_view()
    elif route=="View":
        View.viewAndUpdateJourney()
    elif route=="Audit":
        Audit.load_view()
    elif route=="Add_journey":
        Add_journey.load_view()
    elif route=="Update_journey":
        Update_journey.update()
    elif route == None:
        login.load_view()     
navigation()
