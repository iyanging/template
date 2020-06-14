import re
import sys

MODULE_REGEX = r'^[_a-zA-Z0-9]+$'

project_name = '{{cookiecutter.project_name}}'

if not re.match(MODULE_REGEX, project_name):
    print(f'ERROR: {project_name} is an invalid project name!')

    # exits with status 1 to indicate failure
    sys.exit(1)
