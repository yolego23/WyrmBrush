# Import necessary mappings from the dungeon module
from .dungeon import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# Import required modules
import os
import server
import json
import shutil
from aiohttp import web

# Define the web root directory
WEBROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), "web")

# Define default config paths and values
CONFIG_DIR = os.path.join(WEBROOT, "config")
DEFAULT_CONFIG_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "default_config")

# Define default config files and their template values
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "web", "js")

TEMPLATE_FILES = {
    "settings.json": {
        "default_workflow": "basic_workflow",
        "theme": "light"
    },
    "basic_workflow.json": os.path.join(TEMPLATE_DIR, "template_workflow.json"),
    "model_config.json": {
        "basic_default": {
            "sampler_name": "dpmpp_2m",
            "CFG": 6.5,
            "scheduler": "exponential"
      }
    }
}

def init_config():
    """
    Initialize the config directory and populate it with default files
    if they do not exist.
    """
    try:
        # Ensure the config directory exists
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)
            print(f"[Wyrmbrush]Created config directory: {CONFIG_DIR}")

        # Iterate through TEMPLATE_FILES and initialize each file
        for filename, source in TEMPLATE_FILES.items():
            config_path = os.path.join(CONFIG_DIR, filename)

            # Skip files that already exist
            if os.path.exists(config_path):
                print(f"[Wyrmbrush]File already exists, skipping: {config_path}")
                continue

            # Handle copying template files
            if isinstance(source, str) and os.path.isfile(source):
                shutil.copy2(source, config_path)
                print(f"[Wyrmbrush] Copied template: {source} -> {config_path}")

            # Handle creating JSON files from dictionaries
            elif isinstance(source, dict):
                with open(config_path, 'w') as f:
                    json.dump(source, f, indent=2)
                print(f"[Wyrmbrush]Created config file: {config_path} with default values")

            else:
                print(f"[Wyrmbrush]Warning: Unable to handle source for {filename}")

    except Exception as e:
        print(f"[Wyrmbrush]Error initializing config: {e}")

# Initialize config when module is loaded
init_config()

# Define a route for the main entry point of the Wyrmbrush application
@server.PromptServer.instance.routes.get("/wyrmbrush")
def deungeon_entrance(request):
    # Serve the index.html file when accessing the /wyrmbrush route
    return web.FileResponse(os.path.join(WEBROOT, "index.html"))

# Set up static routes for serving CSS and JavaScript files
server.PromptServer.instance.routes.static("/dungeon/css/", path=os.path.join(WEBROOT, "css"))
server.PromptServer.instance.routes.static("/dungeon/js/", path=os.path.join(WEBROOT, "js"))
# Set up static route for serving config files
server.PromptServer.instance.routes.static("/dungeon/config/", path=os.path.join(WEBROOT, "config"))


# Define what should be imported when using "from module import *"
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

