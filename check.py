import streamlit as st
import requests
import csv
from PIL import Image

# Load the password and API key from Streamlit secrets
APP_PASSWORD = st.secrets["app_password"]
API_KEY = st.secrets["hunter_api_key"]

# Branding colors
PRIMARY_COLOR = "#0078D4"  # Example primary color from the logo palette
SECONDARY_COLOR = "#2B579A"  # Example secondary color from the logo palette

def search_marketing_officer(company_name):
    queries = [
        f'"{company_name}" "Chief Marketing Officer" OR "CMO" OR "Marketing Director" OR "Marketing Manager" OR "Marketing Assistant" OR "Marketing" OR "Sales" OR "current" OR "present" site:linkedin.com',
        f'"{company_name}" "Chief Marketing Officer" OR "CMO" OR "Marketing Director" OR "Marketing Manager" OR "Marketing Assistant" OR "Marketing" OR "Sales" OR "current" OR "present" site:crunchbase.com',
        f'"{company_name}" "Chief Marketing Officer" OR "CMO" OR "Marketing Director" OR "Marketing Manager" OR "Marketing Assistant" OR "Marketing" OR "Sales" OR "current" OR "present" site:zoominfo.com',
        f'"{company_name}" "Chief Marketing Officer" OR "CMO" OR "Marketing Director" OR "Marketing Manager" OR "Marketing Assistant" OR "Marketing" OR "Sales" OR "current" OR "present" site:rocketreach.co',
    ]
    
    for query in queries:
        google_search_url = f"https://www.google.com/search?q={query}"
        st.markdown(f'<a href="{google_search_url}" target="_blank">Click here to search for "{company_name}" on Google</a>', unsafe_allow_html=True)


def find_email(company_domain, first_name, last_name):
    url = f"https://api.hunter.io/v2/email-finder?domain={company_domain}&first_name={first_name}&last_name={last_name}&api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if 'data' in data and 'email' in data['data']:
        return data['data']['email']
    else:
        return None

def verify_email(email):
    url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if 'data' in data and 'result' in data['data']:
        return data['data']['result'], data['data']['score']
    else:
        return None, None

def save_to_csv(company_name, first_name, last_name, email):
    with open('marketing_officers.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([company_name, first_name, last_name, email])

def main():
    st.set_page_config(page_title="Brandience Email Finding Tool", page_icon=":mailbox_with_mail:", layout="wide")
    
    # First sheet with logo and branding colors
    st.markdown("<div style='text-align: center;'><img src='https://th.bing.com/th?id=OLC.qOUpO2/FdZUwkg480x360&rs=1&pid=ImgDetMain' width='300'></div>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='color: {PRIMARY_COLOR}; text-align: center;'>Brandience Email Finding Tool</h1>", unsafe_allow_html=True)
    
    password = st.text_input("Enter the password to access the tool:", type="password")
    
    if password == APP_PASSWORD:
        st.success("Access granted! Redirecting to the main tool...")
        
        # Main sheet content
        st.markdown(f"<h1 style='color: {PRIMARY_COLOR};'>Search for Marketing Officers</h1>", unsafe_allow_html=True)
        
        company_name = st.text_input("Enter the company name:")
        company_domain = st.text_input("Enter the company's domain (e.g., example.com):")
        
        if st.button("Search Marketing Officer"):
            with st.spinner("Searching..."):
                search_marketing_officer(company_name)
        
        st.markdown(f"<h1 style='color: {PRIMARY_COLOR};'>Find and Verify Email</h1>", unsafe_allow_html=True)
        
        first_name = st.text_input("Enter the first name of the prospect:")
        last_name = st.text_input("Enter the last name of the prospect:")
        
        if st.button("Find Email"):
            with st.spinner("Finding email..."):
                email = find_email(company_domain, first_name, last_name)
                if email:
                    st.success(f"Email found: {email}")
                    result, score = verify_email(email)
                    if result:
                        st.info(f"Verification result: {result}")
                        st.info(f"Email accuracy score: {score}")
                    else:
                        st.warning("Verification failed.")
                    save_to_csv(company_name, first_name, last_name, email)
                    st.success("Details saved to marketing_officers.csv")
                else:
                    st.error("No email found for the given details")
        
        # Add a section for viewing search history
        st.markdown(f"<h1 style='color: {PRIMARY_COLOR};'>Search History</h1>", unsafe_allow_html=True)
        if st.button("View Search History"):
            try:
                with open('marketing_officers.csv', mode='r') as file:
                    reader = csv.reader(file)
                    history_data = list(reader)
                    if history_data:
                        for row in history_data:
                            st.write(f"Company: {row[0]}, First Name: {row[1]}, Last Name: {row[2]}, Email: {row[3]}")
                    else:
                        st.write("No search history found.")
            except FileNotFoundError:
                st.write("No search history found.")
        
        # Add a feedback form
        st.markdown(f"<h1 style='color: {PRIMARY_COLOR};'>Feedback</h1>", unsafe_allow_html=True)
        feedback_text = st.text_area("Please provide your feedback:")
        if st.button("Submit Feedback"):
            with open('feedback.txt', mode='a') as file:
                file.write(feedback_text + "\n")
            st.success("Thank you for your feedback!")
        
    else:
        if password:
            st.error("Incorrect password. Access denied.")

if __name__ == "__main__":
    main()
