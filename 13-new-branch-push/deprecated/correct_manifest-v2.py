# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import subprocess

# Function to get all projects starting with a specific prefix
def get_gerrit_projects_with_prefix(prefix):
    command = "ssh -p 29418 wangnanwang@192.168.117.71 gerrit ls-projects"
    all_projects = subprocess.check_output(command.split()).splitlines()

    # Find projects that start with the given prefix
    return [project for project in all_projects if project.startswith(prefix)]

# Function to parse manifest file and update project names
def parse_manifest(manifest_file, prefix):

    tree = ET.parse(manifest_file)
    root = tree.getroot()

    # Get all Gerrit projects starting with the given prefix
    projects = get_gerrit_projects_with_prefix(prefix)

    # Remove the prefix for easier matching
    stripped_projects = {project[len(prefix) + 1:]: project for project in projects}

    # Iterate over each project element
    for project in root.findall('project'):
        name = project.get('name')

        # Check if the project name without the prefix exists in the stripped projects
        if name in stripped_projects:
            new_name = stripped_projects[name]

            # Set the project name to the matching Gerrit project with prefix
            project.set('name', new_name)
        else:
            print("Project {} does not have a matching Gerrit project with prefix {}.".format(name, prefix))

    # Save the corrected manifest file
    tree.write('correct_manifest_v3.xml', encoding='utf-8', xml_declaration=True)

# Call the function with the manifest and prefix
parse_manifest('UPQ00915_Q1100.xml', 'UPQ0090010')