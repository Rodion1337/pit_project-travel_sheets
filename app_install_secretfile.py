import json
from os.path import exists

from django.core.management.utils import get_random_secret_key

# creating a file with a secret key and bebug status
if not exists("TraveSheets/security_files.env"):
    print("\nsecurity_files.env file not found.\nLet's start creating it.\n")
    with open("TraveSheets/security_files.env", "w") as security_files:
        # get_random_secret_key
        text = {"SECRET_KEY": str(get_random_secret_key()), "DEBUG": "False"}
        security_files.write(json.dumps(text))
    print("security_files.env file created.\n")
else:
    print("\nThe file security_files.env already exists.\n")