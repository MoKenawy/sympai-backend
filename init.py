import os
import sys
import dotenv

dotenv.load_dotenv()
# Get the current directory of the script
current_dir = os.getenv('INIT_PATHS_DIR') + "\\src"

# Add the project root directory to sys.path
sys.path.append(current_dir)

# Iterate through all subdirectories and add them to sys.path
for root, dirs, _ in os.walk(current_dir):
    for d in dirs:
        if not ('__pycache__' in d or 'venv' in d):
            subdirectory_path = os.path.join(root, d)
            sys.path.append(subdirectory_path)


print("Paths Initialized.")
