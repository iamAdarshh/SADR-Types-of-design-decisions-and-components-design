import pandas as pd
import requests
from Urls import JIRA_API_BASE
from Constants import Issues_File_Path, Issue_Details_File_Path

if __name__ == '__main__':
    issues_df = pd.read_csv(Issues_File_Path, delimiter=';')

    # Load the list of issue IDs
    issue_ids = issues_df['key'].tolist()

    # Create an empty list to store issue details
    issue_data = []

    # Fetch details for each issue
    for issue_id in issue_ids:
        try:
            # Make a GET request to fetch issue details
            response = requests.get(f"{JIRA_API_BASE}{issue_id}")
            response.raise_for_status()  # Raise an error for unsuccessful requests

            issue = response.json()
            # Extract relevant fields
            issue_details = {
                'ID': issue['key'],
                'Summary': issue['fields'].get('summary', ''),
                'Status': issue['fields']['status']['name'],
                'Assignee': issue['fields'].get('assignee', {}).get('displayName', 'Unassigned'),
                'Reporter': issue['fields'].get('reporter', {}).get('displayName', ''),
                'Created': issue['fields'].get('created', ''),
                'Updated': issue['fields'].get('updated', ''),
                'Description': issue['fields'].get('description', '')
            }
            issue_data.append(issue_details)
        except Exception as e:
            print(f"Error fetching details for {issue_id}: {e}")

    # Convert the issue data to a DataFrame
    issue_df = pd.DataFrame(issue_data)

    # Save to Excel
    issue_df.to_excel(Issue_Details_File_Path, index=False)

    print(f"Issue details have been saved to {Issue_Details_File_Path}")
