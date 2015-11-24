
#Jama Software
Jama Software is the definitive system of record and action for product development. The company’s modern requirements and test management solution helps enterprises accelerate development time, mitigate risk, slash complexity and verify regulatory compliance. More than 600 product-centric organizations, including NASA, Boeing and Caterpillar use Jama to modernize their process for bringing complex products to market. The venture-backed company is headquartered in Portland, Oregon. For more information, visit [jamasoftware.com](http://jamasoftware.com).

Please visit [dev.jamasoftware.com](http://dev.jamasoftware.com) for additional resources and join the discussion in our community [community.jamasoftware.com](http://community.jamasoftware.com).

## Relate test cases to test runs
```relate_cases_runs.py``` is a script which creates relationships from Jama Test Cases to Test Runs using the Jama REST API.
Please note that this script is distrubuted as-is as an example and will likely require modification to work for your specific use-case.  This example omits error checking. Jama Support will not assist with the use or modification of the script.

### Before you begin
- Install Python 2.7 or higher and the requests library.  [Python](https://www.python.org/) and [Requests](http://docs.python-requests.org/en/latest/)

### Setup
1. As always, set up a test environment and project to test the script.

2. Fill out the CONFIG section of the script.  The necessary fields are:
  - ```username```
  - ```password```
  - ```base_url```  -- This should end with "/rest/latest/"
  - ```project_ids``` -- A comma-separated list of project API IDs.  These are available from the Admin area in Jama, under 'Manage All Projects'
  - ```test_run_api_id``` -- The API ID of test runs.  This is available in the Admin area under 'Item Types'
  - ```new_relationship_type``` -- The exact name of a relationship type.  For example, "Related to" or "Dependent on".

### Testing

1. Run the script.  It will create relationships from all Test Runs in the listed projects to their Test Cases.

2. A new file called 'date_file.dat' is created in the same directory as the script.  This file contains the last date the script was run.  This cuts down on the number of test runs the script has to evaluate.  Note that the time is always set to a minute after Midnight so runs created on the same day will be reevaluated.

3. To reevaluate all the runs in the listed projects, just delete 'date_file.dat'
