import os, sys

PROJECT_DIR = '/var/www/html/website'

activate_this = os.path.join(PROJECT_DIR, 'venv', 'bin', 'activate_this.py')
execfile(activate_this, dict(__file__=activate_this))
sys.path.insert(0, PROJECT_DIR)

from website import app as application