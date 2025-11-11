import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime, date
from typing import Literal


API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Patient Management System",
    layout="wide",
    initial_sidebar_state="expanded" 
)

st.markdown("""
<style>
.stApp {
    background-color: #1a1a2e; /* Deep Dark Blue */
    color: #e6e6fa; /* Light Text */
}
.stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size: 18px; /* Bigger Tab Font */
}
.stButton>button {
    background-color: #0f4c75; /* Blue Button */
    color: white;
    border-radius: 8px;
    border: 1px solid #1a1a2e;
}
.stButton>button:hover {
    background-color: #3282b8;
}
</style>
""", unsafe_allow_html=True)


def create_patient_record(name, dob, gender, phone, email, status):
    data = {
        "name": name,
        "dob": dob.isoformat(),
        "gender": gender,
        "phone": phone,
        "email": email if email else None,
        "status": status
    }
    response = requests.post(f"{API_BASE_URL}/patients/", json=data)
    return response.json()

def get_all_patients(status=None, gender=None, name=None):
    params = {}
    if status:
        params["status"] = status
    if gender:
        params["gender"] = gender
    if name:
        params["name"] = name
        
    response = requests.get(f"{API_BASE_URL}/patients/", params=params)
    return response.json()

def update_patient_record(patient_id, data: dict):
    if 'dob' in data and isinstance(data['dob'], date):
        data['dob'] = data['dob'].isoformat()
        
    response = requests.put(f"{API_BASE_URL}/patients/{patient_id}", json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        return response.json()

def delete_patient_record(patient_id):
    response = requests.delete(f"{API_BASE_URL}/patients/{patient_id}")
    return response.status_code == 200


st.title("Patient Management System")
st.markdown("---")

with st.sidebar:
    st.header("Patient Management System")
    st.markdown("---")
    st.caption("Created by Hamza Shabbir")
    st.markdown("---")

    st.markdown("[GitHub](https://github.com/hamza-shabbir-ansari)")


tab1, tab2 = st.tabs(["New Patient Registration", "Manage Records and Analytics"])


with tab1:
    st.header("New Patient Entry Form")
    
    with st.form("new_patient_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Patient Name", max_chars=100)
            phone = st.text_input("Phone Number", help="e.g., 923xxxxxxxxx")
            dob = st.date_input("Date of Birth", value=date(2000, 1, 1), max_value=date.today())
            
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            email = st.text_input("Email Address (Optional)")
            status = st.selectbox("Initial Status", ["Active", "Discharged"])
            
        submitted = st.form_submit_button("Register Patient")

        if submitted:
            if not name or not phone:
                st.error("Name and Phone Number are required fields.")
            else:
                try:

                    result = create_patient_record(name, dob, gender, phone, email, status)
                    
                    if "id" in result:
                        
                        st.success(f"Patient Record Created Successfully! ID: {result['id']}") 
                    elif "detail" in result:
                        st.error(f"Error: {result['detail']}")
                    else:
                        st.error("An unknown error occurred while submitting the form.")
                except requests.exceptions.ConnectionError:
                    st.error("Backend API is not running. Please run `uvicorn app:app --reload` in the backend directory.")


with tab2:
    st.header("Search, Filter, and Manage Patient Records")
    

    col_search, col_filter1, col_filter2 = st.columns([2, 1, 1])
    
    with col_search:
        search_name = st.text_input("Search by Name", placeholder="Enter patient name...")
    with col_filter1:
        status_filter = st.selectbox("Filter by Status", ["ALL", "Active", "Discharged"])
    with col_filter2:
        gender_filter = st.selectbox("Filter by Gender", ["ALL", "Male", "Female", "Other"])
        
    st.markdown("---")
    

    if st.button("Refresh Patient List", key="refresh_list"):
        st.session_state.run_refresh = True
    
    if 'run_refresh' in st.session_state and st.session_state.run_refresh:
        
        status_param = status_filter if status_filter != "ALL" else None
        gender_param = gender_filter if gender_filter != "ALL" else None

        try:
            with st.spinner('Fetching records...'):
                all_patients = get_all_patients(status=status_param, gender=gender_param, name=search_name)
            
            df = pd.DataFrame(all_patients)
            
            if not df.empty:
                df['dob'] = pd.to_datetime(df['dob']).dt.strftime('%Y-%m-%d')
                df['age'] = df['dob'].apply(lambda x: datetime.now().year - pd.to_datetime(x).year)
                
                display_cols = ['id', 'name', 'age', 'gender', 'phone', 'email', 'status', 'dob']
                df = df[display_cols].rename(columns={'id': 'ID', 'name': 'Name', 'dob': 'DOB', 'age': 'Age'})
                
                st.subheader(f"Total Records: {len(df)}")
                st.dataframe(df, use_container_width=True)

                st.session_state.patient_df = df
                
            else:
                st.info("No records found matching the criteria.")
            
        except requests.exceptions.ConnectionError:
            st.error("Backend API is not running. Please run `uvicorn app:app --reload` in the backend directory.")
        
        st.session_state.run_refresh = False
        
    st.markdown("---")


    st.subheader("Manage Records (Update/Delete)")
    
    col_upd, col_del = st.columns(2)
    

    with col_upd:
        with st.form("update_patient_form"):
            st.markdown("##### Update Record")
            update_id = st.number_input("Record ID to Update", min_value=1, step=1, key="update_id_input")
            
            upd_name = st.text_input("Name (Keep blank to skip)", key="upd_name")
            upd_phone = st.text_input("Phone (Keep blank to skip)", key="upd_phone")
            upd_email = st.text_input("Email (Keep blank to skip)", key="upd_email")
            upd_status = st.selectbox("New Status", ["", "Active", "Discharged"], key="upd_status")
            
            upd_submitted = st.form_submit_button("Update Record")
            
            if upd_submitted:
                if update_id:
                    update_data = {}
                    if upd_name: update_data['name'] = upd_name
                    if upd_phone: update_data['phone'] = upd_phone
                    if upd_email: update_data['email'] = upd_email
                    if upd_status: update_data['status'] = upd_status
                    
                    if not update_data:
                        st.warning("Please enter at least one field to update.")
                    else:
                        result = update_patient_record(update_id, update_data)
                        if "id" in result:
                            st.success(f"Patient ID {update_id} updated.")
                        elif "detail" in result:
                            st.error(f"Error: {result['detail']}")
                        else:
                            st.error("Update failed or record not found.")
                else:
                    st.error("Please enter a valid Record ID.")


    with col_del:
        with st.form("delete_patient_form"):
            st.markdown("##### Delete Record")
            del_id = st.number_input("Record ID to Delete", min_value=1, step=1, key="delete_id")
            st.markdown("##")
            
            del_submitted = st.form_submit_button("Delete Record")
            
            if del_submitted:
                if del_id:
                    if delete_patient_record(del_id):
                        st.success(f"Record ID **{del_id}** deleted successfully.")
                    else:
                        st.error(f"Could not delete ID **{del_id}**. Maybe it doesn't exist.")
                else:
                    st.error("Please enter a valid Record ID.")