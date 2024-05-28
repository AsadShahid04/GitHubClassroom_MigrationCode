import os
import subprocess
import logging

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a file handler for logging to a file
file_handler = logging.FileHandler('github_migration.log')
file_handler.setLevel(logging.INFO)

# Create a console handler for logging to the terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a logging format and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def run_command(command, cwd=None):
    """ Run a shell command and log the output. """
    logger.info(f"Running command: {command}")
    result = subprocess.run(command, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        logger.error(f"Error running command: {command}\n{result.stderr.decode()}")
    else:
        logger.info(f"Command output: {result.stdout.decode()}")
    return result.returncode == 0

def clone_repos(repo_urls, clone_dir):
    """ Clone each repository in the list to the specified directory. """
    if not os.path.exists(clone_dir):
        os.makedirs(clone_dir)

    for repo_url in repo_urls:
        logger.info(f"Cloning repository {repo_url}")
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        clone_path = os.path.join(clone_dir, repo_name)
        if run_command(f"git clone {repo_url} {clone_path}"):
            logger.info(f"Successfully cloned {repo_url} to {clone_path}")
        else:
            logger.error(f"Failed to clone {repo_url}")

def repo_exists(repo_name, github_username):
    """ Check if a repository already exists on GitHub. """
    command = f"gh repo view {github_username}/{repo_name}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def create_new_repo(repo_name, github_username):
    """ Create a new repository on GitHub using GitHub CLI. """
    if repo_exists(repo_name, github_username):
        logger.info(f"Repository {repo_name} already exists on GitHub. Skipping creation.")
        return f"https://github.com/{github_username}/{repo_name}.git"
    
    command = f"gh repo create {repo_name} --private"
    if run_command(command):
        logger.info(f"Successfully created new GitHub repository {repo_name}")
        return f"https://github.com/{github_username}/{repo_name}.git"
    else:
        logger.error(f"Failed to create new GitHub repository {repo_name}")
        return None

def push_to_new_repo(repo_path, new_repo_url):
    """ Push the local repository to the new remote repository. """
    # Set the remote URL to the new repository
    if run_command(f"git remote set-url origin {new_repo_url}", repo_path):
        logger.info(f"Remote URL set to {new_repo_url}")
    else:
        logger.error(f"Failed to set remote URL to {new_repo_url}")
        return

    # Push branches and tags
    if run_command(f"git push --all", repo_path) and run_command(f"git push --tags", repo_path):
        logger.info(f"Successfully pushed {repo_path} to {new_repo_url}")
    else:
        logger.error(f"Failed to push {repo_path} to {new_repo_url}")

if __name__ == "__main__":
   #TODO
    repo_urls = [
        "https://github.com/drdr-teaching/ASSIGNMENT_NAME",
        # Add more repositories as needed
    ]

    #TODO 
    clone_directory = "/INSERT_DIRECTORY_PATH"

    logger.info("Starting the cloning and pushing process")

    # Retrieve GitHub username using GitHub CLI
    result = subprocess.run("gh api user | jq -r .login", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        github_username = result.stdout.decode().strip()
        logger.info(f"GitHub username: {github_username}")
    else:
        logger.error("Failed to retrieve GitHub username")
        exit(1)

    # Step 1: Clone the repositories
    clone_repos(repo_urls, clone_directory)

    # Step 2: Create a new repository using GitHub CLI and push each cloned repo
    for repo_url in repo_urls:
        old_repo_name = repo_url.split('/')[-1].replace('.git', '')
        new_repo_name = old_repo_name
        new_repo_url = create_new_repo(new_repo_name, github_username)
        
        if new_repo_url:
            repo_path = os.path.join(clone_directory, old_repo_name)
            push_to_new_repo(repo_path, new_repo_url)

    logger.info("Process completed")
