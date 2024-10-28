"""
Hardcoding secret keys in your code is a security risk because:
    it exposes sensitive information to everyone, 
    including collaborators, 
    version control history.
    etc.
"""

"""Do this"""
# 1. Install the python-dotenv package
# pip install python-dotenv

# 2. Import the necessary libraries
import os
from dotenv import load_dotenv

# 3. Load the .env file
load_dotenv()

# 4. Access your secret key safely
secret_key = os.getenv("SECRET_KEY")

# 5. Print the secret key (for demonstration purposes)
print(f"Your secret key is: {secret_key}")



