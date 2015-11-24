 
#######--CONFIG--#######

# Username and password should be stored somewhere other than
# source code, depending on your organization's security policy
username = "API_User"
password = "********"

base_url = "{base_url}/rest/latest/"
project_ids = [123, 234] # Comma separated list of project API IDs
test_run_api_id = 12345 # The API ID of test runs (see admin area)
new_relationship_type = "Dependent on"

#####--END CONFIG--#####

import os.path
import datetime
import requests
import json
import sys

def main():
    new_relationship_type_id = get_relationship_type_id(new_relationship_type)
    for project_id in project_ids:
        get_new_runs( project_id, 
                                test_run_api_id,
                                new_relationship_type_id)

def get_relationship_type_id(type_name):
    remaining_results = -1
    start_index = 0

    while remaining_results != 0:
        start_at = "startAt=" + str(start_index)

        url = base_url + "relationshiptypes?" + start_at
        response = requests.get(url, auth=(username, password))
        json_response = json.loads(response.text)

        if "pageInfo" in json_response["meta"]:
            page_info = json_response["meta"]["pageInfo"]
            total_results = page_info["totalResults"]
            result_count = page_info["resultCount"]
            remaining_results = total_results - (start_index + result_count)
            start_index += 20
        else:
            remaining_results = 0;

        relationship_types = json_response["data"]
        for relationship_type in relationship_types:
            if relationship_type["name"] == type_name:
                return relationship_type["id"]

def get_new_runs(project_id, test_run_id, new_type_id):
    successes = 0
    attempts = 0
    remaining_results = -1
    start_index = 0

    print "New runs evaluated:"

    while remaining_results != 0:
        start_at = "startAt=" + str(start_index)

        url = base_url + "abstractitems?" + start_at + "&project=" + str(project_id) + "&itemType=" + str(test_run_id)

        url += get_date() # Removing this line will cause all runs to be evaluated whenever this script is executed

        response = requests.get(url, auth=(username, password))
        json_response = json.loads(response.text)

        page_info = json_response["meta"]["pageInfo"]
        total_results = page_info["totalResults"]
        result_count = page_info["resultCount"]
        remaining_results = total_results - (start_index + result_count)
        start_index += 20

        runs = json_response["data"]
        for run in runs:
            attempts += 1
            sys.stdout.write("\r{0} / {1}".format(attempts, total_results))
            sys.stdout.flush()
            test_case_id = run["fields"]["testCase"]
            successes += create_relationship(test_case_id, run["id"], new_type_id)

    print "\nSuccesfully created {0}/{1} relationships".format(successes, attempts)

def create_relationship(from_item, to_item, relationship_type):
    payload = {
        "fromItem": from_item,
        "toItem": to_item,
        "relationshipType": relationship_type
    }
    url = base_url + "relationships/"
    response = requests.post(url, json=payload, auth=(username, password))
    if response.status_code == 201:
        return 1
    return 0

def get_date():
    if os.path.isfile("date_file.dat"):
        f = open("date_file.dat", "r")
        date = f.read()
    else:
        date = ""
    f = open("date_file.dat", "w")
    date_string = datetime.date.today().strftime("%Y-%m-%d") + "T17%3A44%3A57.000%2B0000"
    f.write("&createdDate=" + date_string)
    return date

if __name__ == '__main__':
    sys.exit(main())

