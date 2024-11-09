# Import necessary mappings from the dungeon module
from .dungeon import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# Import required modules
import os
import server
from aiohttp import web

# Define the web root directory
WEBROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), "web")

# Define a route for the main entry point of the Wyrmbrush application
@server.PromptServer.instance.routes.get("/wyrmbrush")
def deungeon_entrance(request):
    # Serve the index.html file when accessing the /wyrmbrush route
    return web.FileResponse(os.path.join(WEBROOT, "index.html"))

# Set up static routes for serving CSS and JavaScript files
server.PromptServer.instance.routes.static("/dungeon/css/", path=os.path.join(WEBROOT, "css"))
server.PromptServer.instance.routes.static("/dungeon/js/", path=os.path.join(WEBROOT, "js"))

# Define what should be imported when using "from module import *"
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
