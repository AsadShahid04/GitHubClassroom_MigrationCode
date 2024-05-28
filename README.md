# GitHub Classroom Migration Script

## Overview

This repository contains a Python script to automate the process of migrating repositories from GitHub Classroom organization/another user to another. The script performs the following tasks:

1. Clones a list of repositories from a specified source.
2. Creates new repositories on GitHub.
3. Pushes the cloned repositories to the newly created repositories on GitHub.

## Prerequisites

- Python 3.x
- Git
- GitHub CLI (`gh`)
- `jq` (a command-line JSON processor)

## Setup

1. **Clone this repository**:

```sh
git clone <repository_url>
cd <repository_directory>
```
2. **Install GitHub CLI**:

Follow the instructions at https://cli.github.com to install gh.

3. **Install jq**:

- On macOS:
```
brew install jq
```
- On Ubuntu:
```
sudo apt-get install jq
```
## Configuration:

1. Authenticate GitHub CLI:

```
gh auth login
```

2. Update the script:

Replace the repo_urls list in  `AsadGithubClassroomMigrationScript.py` to include the URLs of the repositories you want to migrate.
Set the `clone_directory` variable to the desired local directory where the repositories will be cloned.

## Usage:

1. Run the script:
```
python AsadGithubClassroomMigrationScript.py
```

2. Check the log file:
The script will log its actions and any errors to github_migration.log. Check this file to ensure the migration process completed successfully.

## Notes
- Make sure that the GitHub CLI is authenticated with sufficient permissions.
- This script uses git clone --mirror to clone repositories, which clones all refs (branches, tags, etc.). 
- If you only need specific branches or tags, you can modify the clone command accordingly.
- All new repositories are made private through the use of ` --private` flag attatched to the end of line 62:
```
command = f"gh repo create {repo_name} --private"
```

## Troubleshooting
- Errors during cloning:
Check if the repositories exist and the URLs are correct.

- Errors during repository creation:
Ensure you have the necessary permissions to create repositories in the target GitHub account.

- Errors during pushing:Ensure the new repositories are created correctly and the remote URLs are set properly.

## License
This project is licensed under the MIT License.
