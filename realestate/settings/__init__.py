
from decouple import config

# Load the project variable from the .env file
project = config('PROJECT', default='dev')

# Determine which settings to import based on the project variable
if project == 'local':
    from .local import *
else:
    from .dev import *