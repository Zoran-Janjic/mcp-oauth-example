
from fastmcp import FastMCP
import re
import os

from mcp.server.fastmcp import FastMCP
from mcp.server.auth.settings import AuthSettings
from pydantic import AnyHttpUrl
from dotenv import load_dotenv
from utils.auth import create_auth0_verifier


mcp = FastMCP("My MCP Server")


# Load environment variables from .env file
load_dotenv()

# Get Auth0 configuration from environment
auth0_domain = os.getenv("AUTH0_DOMAIN")
resource_server_url = os.getenv("RESOURCE_SERVER_URL")

if not auth0_domain:
    raise ValueError("AUTH0_DOMAIN environment variable is required")
if not resource_server_url:
    raise ValueError("RESOURCE_SERVER_URL environment variable is required")


# Initialize Auth0 token verifier
token_verifier = create_auth0_verifier()



# Create an MCP server with OAuth authentication
mcp = FastMCP(
    "oauth-test-server",
    host="0.0.0.0",
    port=3002,
    # OAuth Configuration
    token_verifier=token_verifier,
    auth=AuthSettings(
        issuer_url=AnyHttpUrl(f"https://{auth0_domain}/"),
        resource_server_url=AnyHttpUrl(resource_server_url),
        required_scopes=["openid", "profile", "email", "address", "phone"],
    ),
)


@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}, Hello from mcp-oauth-example!"

if __name__ == "__main__":
    mcp.run(transport='streamable-http')