import os
import xml.etree.ElementTree as ET
import git 
import shutil
import io
import pytest
from datetime import datetime
from lib.testResultsDB import TestResultDB
import inspect

@pytest.fixture
def db():
    db = TestResultDB()
    db.createConnection()
    yield db
    db.close()

def insert_test_result(db, table_name, test_info, sut_info, actual_result, expected_result):
    # Insert test result into the database
    verdict = "PASS" if actual_result == expected_result else "FAIL"
    db.insert_test_result(table_name, datetime.now(), test_info["name"], test_info["version"],
                          sut_info["name"], sut_info["version"], verdict)
    


def get_schema_versions_from_string(file_content):
    # Parse the XML content using an in-memory file
    tree = ET.parse(io.StringIO(file_content))
    root = tree.getroot()
    version = root.attrib.get("version")
    return version


def xsd_check():
    # Clone the repository to access the previous commit
    repo = git.Repo.clone_from("https://github.com/ITxPT/S02.git", "temp_repo")

    # List to store error messages
    errors = []

    # loop through all the files and folders for the directory
    for root, dirs, files in os.walk("temp_repo"):
        for file in files:
            if file.endswith(".xsd"):
                file_path = os.path.join(root, file)[len("temp_repo/"):]
                
                commits = list(repo.iter_commits(paths=file_path, max_count=2))
                latest_commit = commits[0]
                latest_version = get_schema_versions_from_string(repo.git.show(f"{latest_commit.hexsha}:{file_path}")) # Get the latest version

                if latest_version is None: # If the latest version is None, then the file does not have a version
                    errors.append(f"{file_path}: File [{file}] does not have a version")
                    continue

                if len(commits) > 1:
                    second_latest_commit = commits[1]
                    previous_version = get_schema_versions_from_string(repo.git.show(f"{second_latest_commit.hexsha}:{file_path}")) # Get the previous version
                    if latest_version == previous_version: # If the latest version is the same as the previous version, then the version has not changed
                        errors.append(f"{file_path}: Schema version for file [{file}] has not changed!")

    # Clean up: Delete the temporary repository
    shutil.rmtree("temp_repo")

    return errors

def test_xsd_versions(db):
    # Database table name
    table_name = "XSD_check"
    db.create_table(table_name)

    # Test case information
    test_info = {
        "name": inspect.currentframe().f_code.co_name,
        "version": "1.0.0"
    }

    # System under test (SUT) information
    sut_info = {
        "name": "S02 XSD",
        "version": "NA"
    }

    # Execute the system under test (SUT)
    result = xsd_check()

    # Define expected result
    expected_result = "Hello World!"

    # Insert test result into the database
    insert_test_result(db, table_name, test_info, sut_info, result, expected_result)

    # Assert result
    raise AssertionError("\n".join(result))
