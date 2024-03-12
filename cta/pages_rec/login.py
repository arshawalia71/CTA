
import streamlit as st
import requests

#this is the login page. The function gets executed by default when the apllication is started.
def load_view():
    col1,col2=st.columns([2,1])
    #below markdown adds the image on the login page
    #markdown can be used to run and execute html code
    col1.markdown("""
    <div class="centered" style="position: fixed; top: 0px; left: 0px;">
        <img src="https://media.istockphoto.com/id/1281150061/vector/register-account-submit-access-login-password-username-internet-online-website-concept.jpg?s=612x612&w=0&k=20&c=9HWSuA9IaU4o-CK6fALBS5eaO1ubnsM08EOYwgbwGBo=" alt="Logo" width="600" height="600">
    </div>
    """, unsafe_allow_html=True)
    #below are just to position the button in the right place as css might not work always
    col2.write("\n")
    col2.write("\n")
    col2.write("\n")
    col2.write("\n")
    col2.write("\n")
    col2.write("\n")
    col2.write("\n")
    col2.write("\n")
    col2.write("\n")
    # Add the sign-in button to the container
    #replace the below path with your path as mentioned in installation guide
    with open('C:\\Users\\arshaw\\Downloads\\call-graph\\cta\\pages_rec\\button.css') as f:
        col2.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        col1,col2,col3,col4,col5=col2.columns(5)
        x = col1.button("Sign in with Adobe")
        #Once the button is clicked the users are redirected to the sign_in.html page from where they are authenticated
        if x:
            nav_script = """
                <meta http-equiv="refresh" content="0; url='%s'">
                """ % ('https://bgdaxjwbynxkobvuwmmt67.streamlit.app/auth/sign_in')
            col2.write(nav_script, unsafe_allow_html=True)

    