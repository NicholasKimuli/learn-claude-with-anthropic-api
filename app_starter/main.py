from mcp.server.fastmcp import FastMCP
from tools.math import add
from tools.document import binary_document_to_markdown, document_path_to_markdown

mcp = FastMCP("docs")

mcp.tool()(add)
mcp.tool()(binary_document_to_markdown)
mcp.tool()(document_path_to_markdown)

if __name__ == "__main__":
    mcp.run()
