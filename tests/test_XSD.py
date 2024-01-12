import os
import xml.etree.ElementTree as ET
import git 
import shutil
import io
import pytest
from lib.power_bi import push_results_to_power_bi
import os
from dotenv import load_dotenv

load_dotenv()

BI_DATASET_ID = os.getenv("BI_XSD_DATASET_ID")

def insert_test_result(actual_result, expected_result):
    verdict = "PASS" if actual_result == expected_result else "FAIL"
    # Push test result to Power BI
    if verdict == "PASS":
        push_results_to_power_bi(1, BI_DATASET_ID)
    else:
        push_results_to_power_bi(0, BI_DATASET_ID)
    


def get_schema_versions_from_string(file_content):
    # Parse the XML content using an in-memory file
    tree = ET.parse(io.StringIO(file_content))
    root = tree.getroot()
    version = root.attrib.get("version")
    return version


def clone_repo(repo_url, local_dir):
    """Clone the repository to access the previous commit."""
    return git.Repo.clone_from(repo_url, local_dir)

def get_file_commits(repo, file_path, max_count):
    """Get the commits for a file."""
    return list(repo.iter_commits(paths=file_path, max_count=max_count))

def get_file_version(repo, commit, file_path):
    """Get the version of a file from a commit."""
    return get_schema_versions_from_string(repo.git.show(f"{commit.hexsha}:{file_path}"))

def xsd_check():
    """Check the versions of .xsd files in a Git repository."""

    # Clone the repository to access the previous commit
    repo = clone_repo("https://github.com/ITxPT/S02.git", "temp_repo")

    # List to store error messages
    errors = []

    # Loop through all the files and folders for the directory
    for root, dirs, files in os.walk("temp_repo"):
        for file in files:
            if file.endswith(".xsd"):
                file_path = os.path.join(root, file)[len("temp_repo/"):]

                commits = get_file_commits(repo, file_path, 2)
                latest_commit = commits[0]
                latest_version = get_file_version(repo, latest_commit, file_path)

                if latest_version is None:  # If the latest version is None, then the file does not have a version
                    errors.append(f"{file_path}: File [{file}] does not have a version")
                    continue

                if len(commits) > 1:
                    second_latest_commit = commits[1]
                    previous_version = get_file_version(repo, second_latest_commit, file_path)
                    if latest_version == previous_version:  # If the latest version is the same as the previous version, then the version has not changed
                        errors.append(f"{file_path}: Schema version for file [{file}] has not changed!")

    # Clean up: Delete the temporary repository
    shutil.rmtree("temp_repo")

    return errors

def test_xsd_versions():
    # Execute the system under test (SUT)
    result = xsd_check()

    # Define expected result
    expected_result = []

    # Insert test result into the database
    insert_test_result(result, expected_result)

    # Assert result
    assert result == expected_result, "\n".join(result)
