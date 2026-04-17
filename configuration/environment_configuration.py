import os

from dotenv import load_dotenv

load_dotenv()

routes_configuration_file_path = os.getenv("ROUTES_CONFIGURATION_FILE_PATH", "/config/routes.yaml")
output_directory = os.getenv("OUTPUT_DIRECTORY", "/etc/nginx/conf.d")
