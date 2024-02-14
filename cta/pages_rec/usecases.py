import streamlit as st
import ast
import utils as utl

# This is the function that gets called when the "Add Customer Use Cases" button is clicked
def load_view():
    utl.sidebar_component() #displays navbar component
    data = st.experimental_get_query_params()
    dataframe = data["payload"][0] #gets the record details of the selected record to be updated
    drNumber = data["dr_number"][0]

    print(drNumber)
    #st.empty()
    dataframe = ast.literal_eval(dataframe)
    # Create two columns to organize the input fields, three fields in each column
    col1, col2 = st.columns(2)

    with st.form("addForm", clear_on_submit=True):
        # Fields in the first column
        with col1:
            name = st.text_input(":triangular_flag_on_post: Name")
            summary = st.text_area(":triangular_flag_on_post: Summary")
            implementation_date = st.date_input(":triangular_flag_on_post: Implementation Date")

        # Fields in the second column
        with col2:
            customer = st.text_input("Customer details")
            # go_live_date = st.date_input(":triangular_flag_on_post: Go-Live Date")
            department = st.text_input(":triangular_flag_on_post: Department - String")
            stakeholder_email = st.text_input(":triangular_flag_on_post: Stakeholder Email")

        form_filled = True
        if not (name and summary and implementation_date and department and stakeholder_email):
            form_filled = False
            st.error("Please fill all the mandatory fields before clicking on the add button")

        submit_button = st.form_submit_button("Add")

        if submit_button and form_filled:
            data = {
                "Name": name,
                "Summary": summary,
                "Implementation Date": implementation_date.strftime("%Y%m%d"),
                # "Go-Live Date": go_live_date.strftime("%Y%m%d"),
                "Department": department,
                "Stakeholder Email": stakeholder_email,
                "ProjectID": dr_number  # Make sure 'dr_number' is defined
            }

            st.write(data)
            nav_script = """
                <meta http-equiv="refresh" content="0; url='%s'">
            """ % ('http://localhost:8000/auth/add_customer_use_cases?payload=' + str(data))
            st.write(nav_script, unsafe_allow_html=True)