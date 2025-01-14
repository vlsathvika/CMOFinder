import streamlit as st
import webbrowser
import requests
import csv

# Load the password and API key from Streamlit secrets
APP_PASSWORD = st.secrets["app_password"]
API_KEY = st.secrets["hunter_api_key"]

def search_marketing_officer(company_name):
    queries = [
        f'"{company_name}" "Chief Marketing Officer" OR "CMO" OR "Marketing Director" OR "Marketing Manager" OR "Marketing Assistant" OR "Marketing" OR "Sales" OR "current" OR "present" site:linkedin.com',
        f'"{company_name}" "Chief Marketing Officer" OR "CMO" OR "Marketing Director" OR "Marketing Manager" OR "Marketing Assistant" OR "Marketing" OR "Sales" OR "current" OR "present" site:crunchbase.com',
        f'"{company_name}" "Chief Marketing Officer" OR "CMO" OR "Marketing Director" OR "Marketing Manager" OR "Marketing Assistant" OR "Marketing" OR "Sales" OR "current" OR "present" site:zoominfo.com',
        f'"{company_name}" "Chief Marketing Officer" OR "CMO" OR "Marketing Director" OR "Marketing Manager" OR "Marketing Assistant" OR "Marketing" OR "Sales" OR "current" OR "present" site:rocketreach.co',
    ]
    
    for query in queries:
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)

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
    st.title("Brandience Email Finding Tool")
    
    # Password protection
    password = st.text_input("Enter the password:", type="password")
    if password == APP_PASSWORD:
        st.success("Access granted!")
        
        company_name = st.text_input("Enter the company name:")
        company_domain = st.text_input("Enter the company's domain (e.g., example.com):")
        
        if st.button("Search Marketing Officer"):
            search_marketing_officer(company_name)
        
        first_name = st.text_input("Enter the first name of the prospect:")
        last_name = st.text_input("Enter the last name of the prospect:")
        
        if st.button("Find Email"):
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
    else:
        st.error("Incorrect password. Access denied.")

if __name__ == "__main__":
    main()
