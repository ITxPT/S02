import os
import xml.etree.ElementTree as ET
import git 
import shutil
import io
import pytest
from lib.power_bi import push_results_to_power_bi
import os
from dotenv import load_dotenv
import glob
from lxml import etree

load_dotenv()

BI_DATASET_ID = os.getenv("BI_DATASET_ID")

def insert_test_result(test_name: str, actual_result, expected_result, BI_DATASET_ID: str):
    # Check if the actual result matches the expected result
    verdict = 1 if actual_result == expected_result else 0

    # Push test result to Power BI
    push_results_to_power_bi(test_name, verdict, BI_DATASET_ID)

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

def validate_xml_examples():
    # List to store error messages
    errors = []

    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(current_dir)

    # Iterate over each sibling directory
    for sibling_dir in os.listdir(parent_dir):
        # Skip the current directory
        if sibling_dir == os.path.basename(current_dir):
            continue

        # Define the directories where your XSDs and XMLs are stored
        xsd_dir = os.path.join(parent_dir, sibling_dir, "xsd")
        xml_dir = os.path.join(parent_dir, sibling_dir, "examples")

        # Skip this sibling directory if it doesn't contain XSDs and XMLs
        if not os.path.exists(xsd_dir) or not os.path.exists(xml_dir):
            continue

        # Get all XSD and XML files
        xsd_files = glob.glob(f"{xsd_dir}/*.xsd")
        xml_files = glob.glob(f"{xml_dir}/*.xml")

        # Check if there are any XSD files without a corresponding XML
        for xsd_file in xsd_files:
            xml_file = os.path.join(xml_dir, os.path.basename(xsd_file).replace('.xsd', '.xml'))
            if not os.path.exists(xml_file):
                errors.append(f"XSD file {xsd_file} does not have a corresponding XML")

        # Check if there are any XML files without a corresponding XSD
        for xml_file in xml_files:
            xsd_file = os.path.join(xsd_dir, os.path.basename(xml_file).replace('.xml', '.xsd'))
            if not os.path.exists(xsd_file):
                errors.append(f"XML file {xml_file} does not have a corresponding XSD")

        # Iterate over each XML file
        for xml_file in glob.glob(f"{xml_dir}/*.xml"):
            # Derive the name of the corresponding XSD
            xsd_file = os.path.join(xsd_dir, os.path.basename(xml_file).replace('.xml', '.xsd'))

            # Skip this XML file if its XSD doesn't exist
            if not os.path.exists(xsd_file):
                continue

            # Parse the XSD
            xmlschema_doc = etree.parse(xsd_file)
            xmlschema = etree.XMLSchema(xmlschema_doc)

            # Parse the XML
            doc = etree.parse(xml_file)

            # Validate the XML against the XSD
            #assert xmlschema.validate(doc), f"{xml_file} does not conform to its XSD"
            if not xmlschema.validate(doc):
                errors.append(f"{xml_file} does not conform to its XSD")
                
    return errors

def test_xsd_versions():
    # Execute the system under test (SUT)
    result = []
    result += xsd_check()
    result += validate_xml_examples()

    # Define expected result
    expected_result = []

    # Insert test result into the database
    insert_test_result("S02", result, expected_result, BI_DATASET_ID)

    # Assert result
    assert result == expected_result, "\n".join(result)
