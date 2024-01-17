#!/usr/bin/env python3
"""
Script: list_instances_by_computes.py

Description:
    This script retrieves information about OpenStack instances organized by project
    from specified hosts. It uses the openstacksdk library for OpenStack API interaction.

Usage:
    python list_instances_by_computes.py <host1> [<host2> ...]

Environment Variables (required for authentication):
    - OS_AUTH_URL
    - OS_PROJECT_NAME
    - OS_USERNAME
    - OS_PASSWORD
    - OS_USER_DOMAIN_NAME
    - OS_PROJECT_DOMAIN_NAME

Dependencies:
    - openstacksdk (install using 'pip install openstacksdk')

Note:
    Make sure to set the necessary environment variables for OpenStack authentication
    before running the script.

Example:
    python list_instances_by_computes.py openstack-host1 openstack-host2
"""
import os
import sys
from openstack import connection

def get_instances_by_project(conn, hosts):
    instances_by_project = {}

    for host in hosts:
        servers = conn.compute.servers(host=host, all_projects=True)
        for server in servers:
            instance_name = server.name
            project_id = server.project_id 
            project = conn.identity.get_project(project_id)
            project_name = project.name if project else None

            if project_name:
                if project_name not in instances_by_project:
                    instances_by_project[project_name] = []
                instances_by_project[project_name].append(instance_name)

    return instances_by_project

def main():
    # Use OpenStack environment variables for authentication
    auth_args = {
        'auth_url': os.environ.get('OS_AUTH_URL'),
        'project_name': os.environ.get('OS_PROJECT_NAME'),
        'username': os.environ.get('OS_USERNAME'),
        'password': os.environ.get('OS_PASSWORD'),
        'user_domain_name': os.environ.get('OS_USER_DOMAIN_NAME'),
        'project_domain_name': os.environ.get('OS_PROJECT_DOMAIN_NAME'),
    }

    # Check if at least one argument (host) is provided
    if len(sys.argv) < 2:
        print("Usage: {} <host1> [<host2> ...]".format(sys.argv[0]))
        sys.exit(1)

    # List of OpenStack hosts to query
    hosts = sys.argv[1:]

    conn = connection.Connection(**auth_args)

    instances_by_project = get_instances_by_project(conn, hosts)

    # Display instance names per project
    for project_name, instances in instances_by_project.items():
        print(f"Instances for project {project_name}:")
        for instance in instances:
            print(f"  - {instance}")
        print()

if __name__ == "__main__":
    main()

