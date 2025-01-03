###
# Written by: rlozano@streamsets.com
# Adds a Role to a User using Rest APIs
# Script for non-production and for demonstration purposes only. 
# There are no guarantees with these scripts. Use at your own risk. 
# Please Read codes for what functionalities they will do.
###

import json
import requests
import warnings
import getpass


def login_to_control_hub(username, password):
    # Logs in to the Control Hub and returns the session token.
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")
    
    login_url = SCH_ENDPOINT + "/security/public-rest/v1/authentication/login"
    login_payload = f'{{"userName":"{username}", "password":"{password}"}}'  # Raw JSON string
    login_headers = {
        "Content-Type": "application/json",
        "X-Requested-By": "SCH"
    }
    
    login_response = requests.post(login_url, data=login_payload, headers=login_headers, verify=False)
    
    if login_response.status_code == 200:
        #print("Login successful.")
        pass
    else:
        raise Exception(f"Login failed. Status code: {login_response.status_code}, Response: {login_response.text}")
    
    cookies = login_response.cookies.get_dict()
    session_token = cookies.get("SS-SSO-LOGIN")
    
    if not session_token:
        raise Exception("Session token not found.")
    
    return session_token

def get_headers(session_token):
    # Constructs the headers for the API call.
    return {
        "Content-Type": "application/json",
        "X-Requested-By": "SCH",
        "X-SS-REST-CALL": "true",
        "X-SS-User-Auth-Token": session_token
    }

def get_available_roles(session_token):
    # Fetches available roles from the Control Hub and prints their IDs.
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")
   
    api_url = SCH_ENDPOINT + "/security/rest/v1/roles"
    api_headers = get_headers(session_token)
    api_response = requests.get(api_url, headers=api_headers, verify=False)
   
    if api_response.status_code == 200:
        # Extract roles and add IDs to a set
        roles = api_response.json()
        roles_set = set()

        for role in roles:
            roles_set.add(role["id"])  # Add each role ID to the set

        return roles_set
    else:
        raise Exception(f"API call failed. Status code: {api_response.status_code}, Response: {api_response.text}")

def get_user_roles(session_token, organization_id, user_id):
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")

    api_url = SCH_ENDPOINT + f"/security/rest/v1/organization/{organization_id}/user/{user_id}"
    api_headers = get_headers(session_token)
    api_response = requests.get(api_url, headers=api_headers, verify=False)
    
    if api_response.status_code == 200:
        # Parse the response
        user_data = api_response.json()
        roles = user_data.get("roles", [])
        return roles
    else:
        raise Exception(f"API call failed. Status code: {api_response.status_code}, Response: {api_response.text}")


def get_user(session_token, organization_id, user_id):
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")

    api_url = SCH_ENDPOINT + f"/security/rest/v1/organization/{organization_id}/user/{user_id}"
    api_headers = get_headers(session_token)
    api_response = requests.get(api_url, headers=api_headers, verify=False)

    if api_response.status_code == 200:
        # Parse the response
        user_data = api_response.json()
        return user_data
    else:
        raise Exception(f"API call failed. Status code: {api_response.status_code}, Response: {api_response.text}")

def edit_user(session_token, organization_id, user_id, user_data):
    # Edits a user in a specific organization vi POST.
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")
    
    api_url = SCH_ENDPOINT + f"/security/rest/v1/organization/{organization_id}/user/{user_id}"
    api_headers = get_headers(session_token)
    
    api_response = requests.post(api_url, headers=api_headers, json=user_data, verify=False)
    
    if api_response.status_code == 200:
        return api_response.json()
    else:
        raise Exception(f"API call failed. Status code: {api_response.status_code}, Response: {api_response.text}")


def add_role(session_token, available_roles, organization_id, user_id, added_role):
    # Add Role to User
    if added_role in available_roles:
        user = get_user(session_token, organization_id=organization_id, user_id=user_id)
        roles = user.get("roles", [])
        if added_role not in roles:
            roles.append(added_role)
            print(f'Adding role: {added_role}...')
        else:
            print(f'Role already exists: {added_role}...')

        user['roles'] = roles
        edit_user(session_token, organization_id=organization_id, user_id=user_id, user_data=user)
    else:
        raise Exception(f"Role: {added_role} is not available for current API User.")


# Main
if __name__ == "__main__":
    try:
        global SCH_ENDPOINT 
        SCH_ENDPOINT = "https://cloud.streamsets.com"

        # Ask for user input
        api_username = input("API Username: ")
        api_password = getpass.getpass("API Password: ")

        session_token = login_to_control_hub(api_username, api_password)
        available_roles  = get_available_roles(session_token)
        available_roles = list(available_roles)
        for num, i in enumerate(available_roles):
            print(num,i) 
        role_num = input("Please role to add  number: ")
        role_num = int(role_num)
        print(available_roles[role_num])
        user_id = input("Please enter user Id, example - username@org_id: ")
        org_id = input("Please enter in org_id, exemple - org_id: ")
        add_role(session_token, available_roles, organization_id=org_id, user_id=user_id, added_role=available_roles[role_num])
    
    except Exception as e:
        print(str(e))





