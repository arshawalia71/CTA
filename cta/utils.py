import streamlit as st
import base64
from streamlit.components.v1 import html

css_styles = """
<style>
    /* Dropdown container */
    .dropdown {
        position: relative;
        display: inline-block;
    }

    /* Dropdown content (hidden by default) */
    .dropdown-content {
        display: none;
        position: absolute;
        margin-top:50px;

        background-color: #f9f9f9;
        min-width: 170px;
        border-radius: 15px;
        box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
        z-index: 1;
    }

    /* Links inside the dropdown */
    .dropdown-content a {
        color: black;
        padding: 12px 16px;
        text-decoration: none;
        display: block;
    }

    /* Change color of dropdown links on hover */
    .dropdown-content a:hover {
        background-color: #f1f1f1;
    }

    /* Show the dropdown menu when hovering over the parent div */
    .dropdown:hover .dropdown-content {
        display: block;
    }
</style>
"""
st.markdown(css_styles, unsafe_allow_html=True)

from PATHS import NAVBAR_PATHS, SETTINGS
#file used to add the navbar
#the below code can be used to add css from a file later
"""def inject_custom_css():
    with open('assets/styles.css') as f:
        custom_css = f.read()
        st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)"""
#returns the route "?nav=" based on the url query
def get_current_route():
    try:
        return st.experimental_get_query_params()['nav'][0]
    except:
        return None
#builds the navbar component
#
def navbar_component():
    """with open("assets/images/3lines.png", "rb") as image_file:
        image_as_base64 = base64.b64encode(image_file.read())""" #image added to the right top corner

    navbar_items = ''
    #add css only inline as it can cause confusions with agGrid's css if a file is used!!!
    for key, value in NAVBAR_PATHS.items():

        if value == "Report":
            navbar_items += (
                f'<a title:"report" style="font-family: Sans Serif; float: left; display: block; color: #0w2450 !important; text-align: center; padding: 10px 0px; text-decoration: none !important; border-bottom: 2px solid transparent; font-size: 24px;" href="http://localhost:8000/get_token" target="_self">{key}</a>'
            )

        #styling for add icon 
        elif value == "Add":
            # navbar_items += (
            #     f'<a title:"home" style="font-family: \'Trebuchet MS\', sans-serif; float: left; display: block; color: #f2f2f2 !important; text-align: center; padding: 0px 0px; text-decoration: none !important; border-bottom: 2px solid transparent; font-size: 34px;" href="http://localhost:8000/get_dropdowns" target="_self">{key}</a>'
            # )
            navbar_items += ( 
                f'<div class="dropdown" style="position: relative; display: inline-block;">'
                f'    <a style="font-family: Sans Serif; float: left; display: block; color: #f2f2f2 !important; text-align: center; padding: 10px 40px; text-decoration: none !important; border-bottom: 2px solid transparent; font-size: 24px; cursor: pointer;" target="_self">{key}</a>'
                f'    <div class="dropdown-content" >'
                f'        <a href="http://localhost:8000/get_dropdowns" ">Customer Project</a>'
                f'        <a href="http://localhost:8000/get_usecases" >Customer Usecase</a>'
                    
                f'    </div>'
                f'</div>'
            )
        elif value == "Search":
            navbar_items += (
                f'<a style="font-family: Sans Serif; float: left; display: block; color: #0w2450 !important; text-align: center; padding: 10px 40px; text-decoration: none !important; border-bottom: 2px solid transparent; font-size: 24px;" href="http://localhost:8000/get_token" target="_self">{key}</a>'
            )

        
    # Add the "Update" and "View" buttons (invisible)
        elif value=="update":
            navbar_items+=(
            f'<a style="display: none;" href="http://localhost:8000/update" target="_self">Update</a>'
            )
        elif value=='View':
            navbar_items += (
                f'<a style="display: none;" href="http://localhost:8000/view" target="_self">View</a>')
        elif value=='Audit':
            navbar_items += (
                f'<a style="display: none;" href="http://localhost:8000/Audit" target="_self">Audit</a>')
        else:

            navbar_items += (

                f'<a style="font-family: \'Trebuchet MS\', sans-serif; float: left; display: block; color: #000000 !important; text-align: center; text-decoration: none !important; border-bottom: 2px solid transparent; padding-left:40px; font-size: 34px;" href="http://localhost:8000/" target="_self">{key}</a>'

            )
    #adds a dropdown icon to the right corner of page but currently not being used
    settings_items = ''
    for key, value in SETTINGS.items():
        settings_items += (
            f'<a style="color: white; position: absolute; right: 1rem; bottom: 1.75rem; opacity: 0.5; z-index: 9999; border: 2px solid #333; border-radius: 25px; padding-right: 0.5rem; padding-left: 0.5rem; background: #333;" href="/?nav={value}" class="custom-settingsNav">{key}</a>'
        )
    #additional_text = username
    #add the nav component and execute the html code using markdown
    component = rf'''
            <nav class="container" style="font-family: 'Trebuchet MS',sans-serif; color:#000000 !important;  position: fixed; width: 70%; z-index: 99999999999999999999; left: 0rem; top: 1rem; height: 70px;">
                <ul class="custom-navlist" style="color:#000000">
                {navbar_items} 
                </ul>
                
            </nav>
            <nav class="container" style="font-family: 'Trebuchet MS', sans-serif; position: fixed; width: 10%; color: #000000; z-index: 9999; right: 0rem; top: 2.5rem; height: 80px;">
                <a style="font-family: \'Trebuchet MS\', sans-serif; float: left; display: block; color: #00000 !important;   text-align: center; background-color: rgb(255,255,255); padding: 5px 10px; text-decoration: none; font-size: 14px;" href="http://localhost:8000/auth/sign_out" target="_self">Log Out</a>
            </nav>
            '''
    st.markdown(component, unsafe_allow_html=True)
    #the below isn't used currently but it can be used to give the dropdown functionality on right top corner
    js = '''
    <script>
    // Navbar elements
    var navigationTabs_custom = window.parent.document.getElementsByClassName("custom-navitem");
    var cleanNavbar_custom = function (navigation_element) {
        navigation_element.removeAttribute('target');
    }

    for (var i = 0; i < navigationTabs_custom.length; i++) {
        cleanNavbar_custom(navigationTabs_custom[i]);
    }

    // Dropdown hide / show
    var dropdown_custom = window.parent.document.getElementById("custom-settingsDropDown");
    dropdown_custom.onclick = function () {
        var dropWindow_custom = window.parent.document.getElementById("myDropdown");
        if (dropWindow_custom.style.visibility == "hidden") {
            dropWindow_custom.style.visibility = "visible";
        } else {
            dropWindow_custom.style.visibility = "hidden";
        }
    };

    var settingsNavs_custom = window.parent.document.getElementsByClassName("custom-settingsNav");
    var cleanSettings_custom = function (navigation_element) {
        navigation_element.removeAttribute('target');
    }

    for (var i = 0; i < settingsNavs_custom.length; i++) {
        cleanSettings_custom(settingsNavs_custom[i]);
    }
    </script>
    '''
    #html(js)



    # ...............................................................................

# SideBar Code

import streamlit as st

def sidebar_component():
# Create a sidebar with navigation links
    st.sidebar.title("Navigation")

    navbar_items = ''
    #add css only inline as it can cause confusions with agGrid's css if a file is used!!!
    for key, value in NAVBAR_PATHS.items():

        # if value == "Report":
        #     navbar_items += (
        #         f'<a title:"report" style="font-family: Sans Serif; float: left; display: block; color: #0w2450 !important; text-align: center; padding: 10px 0px; text-decoration: none !important; border-bottom: 2px solid transparent; font-size: 24px;" href="http://localhost:8000/get_token" target="_self">{key}</a>'
        #     )

        #styling for add icon 
        if value == "Add":
            # navbar_items += (
            #     f'<a title:"home" style="font-family: \'Trebuchet MS\', sans-serif; float: left; display: block; color: #f2f2f2 !important; text-align: center; padding: 0px 0px; text-decoration: none !important; border-bottom: 2px solid transparent; font-size: 34px;" href="http://localhost:8000/get_dropdowns" target="_self">{key}</a>'
            # )
            navbar_items += ( 
                f'<div class="dropdown" style="position: relative; display: inline-block;">'
                f'    <a style="font-family: Sans Serif; float: left; display: block; color: #f2f2f2 !important; text-align: center; padding: 10px 40px; text-decoration: none !important; border-bottom: 2px solid transparent; font-size: 24px; cursor: pointer;" target="_self">{key}</a>'
                f'    <div class="dropdown-content" >'
                f'        <a href="http://localhost:8000/get_dropdowns" ">Customer Project</a>'
                f'        <a href="http://localhost:8000/get_usecases" >Customer Usecase</a>'
                    
                f'    </div>'
                f'</div>'
            )
        elif value == "Search":
            navbar_items += (
                f'<a style="font-family: Sans Serif; float: left; display: block; color: #0w2450 !important; text-align: center; padding: 10px 40px; text-decoration: none !important; border-bottom: 2px solid transparent; font-size: 24px;" href="http://localhost:8000/get_token" target="_self">{key}</a>'
            )

        
    # Add the "Update" and "View" buttons (invisible)
        elif value=="update":
            navbar_items+=(
            f'<a style="display: none;" href="http://localhost:8000/update" target="_self">Update</a>'
            )
        elif value=='View':
            navbar_items += (
                f'<a style="display: none;" href="http://localhost:8000/view" target="_self">View</a>')
        elif value=='Audit':
            navbar_items += (
                f'<a style="display: none;" href="http://localhost:8000/Audit" target="_self">Audit</a>')
        else:

            navbar_items += (

                f'<a style="font-family: \'Trebuchet MS\', sans-serif; float: left; display: block; color: #000000 !important; text-align: center; text-decoration: none !important; border-bottom: 2px solid transparent; padding-left:40px; font-size: 34px;" href="http://localhost:8000/" target="_self">{key}</a>'

            )
    # Create a dictionary to map component labels to URLs
    components = {
        "Home": "http://localhost:8000/",
        "Add Customer Project": "http://localhost:8000/get_dropdowns",
        "Search Project": "http://localhost:8000/get_token",
        # "Add Customer Usecases": "http://localhost:8000/get_usecases",
        "Search CSAT": ""
    }

    component = rf'''
            <nav class="container" style="font-family: 'Trebuchet MS',sans-serif; color:#000000 !important;  position: fixed; width: 70%; z-index: 99999999999999999999; left: 0rem; top: 1rem; height: 70px;">
                <ul class="custom-navlist" style="color:#000000">
                {navbar_items} 
                </ul>
                
            </nav>
            <nav class="container" style="font-family: 'Trebuchet MS', sans-serif; position: fixed; width: 10%; color: #000000; z-index: 9999; right: 0rem; top: 2.5rem; height: 80px;">
                <a style="font-family: \'Trebuchet MS\', sans-serif; float: left; display: block; color: #00000 !important;   text-align: center; background-color: rgb(255,255,255); padding: 5px 10px; text-decoration: none; font-size: 14px;" href="http://localhost:8000/auth/sign_out" target="_self">Log Out</a>
            </nav>
            '''
    st.markdown(component, unsafe_allow_html=True)
    # Add navigation links to the sidebar
    for label, url in components.items():
        st.sidebar.markdown(
            f'<a href="{url}" style="text-decoration: none; color: #333; font-size: 16px;">{label}</a>',
            unsafe_allow_html=True,
        )

    # Add a horizontal line for separation
    st.sidebar.markdown("<hr style='border: 1px solid #333;'>", unsafe_allow_html=True)

    # Add a "Log Out" button at the bottom
    if st.sidebar.button("Log Out"):
        st.write("You clicked Log Out")

# Call the sidebar_component to create the sidebar
# sidebar_component()