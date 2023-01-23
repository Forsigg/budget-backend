import os
from pathlib import Path


project_path = Path('.')
template_env_file = os.path.join(project_path, 'scripts', 'template.env')
env_file_path = os.path.join(project_path, '.env')


with open(template_env_file, 'r') as file:
    env = file.read()

with open('.env', 'w') as file:
    file.write(env)
