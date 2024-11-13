from pydriller import Repository
import pandas as pd
from Constants import Issues_File_Path, Commit_Deatails_File_Path

issues_df = pd.read_csv(Issues_File_Path, delimiter=';')

issue_keys = issues_df['key'].tolist()

# Specify the repository URL or local path
repo_url = 'https://github.com/apache/axis-axis2-java-core'  # Replace with your repository URL or path

# Create a list to store commit details
commit_data = []

# Traverse each commit in the repository
for commit in Repository(repo_url).traverse_commits():
    for issue_key in issue_keys:
        if issue_key in commit.msg:

            print(f"Found commit for issue {issue_key}")

            commit_details = {
                'Key': issue_key,
                'Hash': commit.hash,
                'Parents': commit.parents,
                'Author': commit.author.name,
                'Email': commit.author.email,
                'Date': commit.author_date.__str__(),
                'Message': commit.msg,
                'Number of Files Modified': len(commit.modified_files),
                'Lines Added': commit.insertions,
                'Lines Deleted': commit.deletions,
                'Complexity': commit.dmm_unit_complexity,
                'Interfacing': commit.dmm_unit_interfacing,
                'Size': commit.dmm_unit_size,
                'Files': commit.files,
            }
            commit_data.append(commit_details)

# Convert the commit data to a DataFrame
commit_df = pd.DataFrame(commit_data)

# Save to an Excel file
output_file = Commit_Deatails_File_Path
commit_df.to_excel(output_file, index=False)

print(f"Commit details have been saved to {output_file}")
