from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string",
)
def read_document(
    doc_id: str = Field(description="The ID of the document to read"),
):
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found")

    return docs[doc_id]

@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the document's content with a new string",
)
def edit_document(
    doc_id: str = Field(description="The ID of the document to edit"),
    old_string: str = Field(description="The text to replace. Must match exactly, including whitespace"),
    new_string: str = Field(description="The new text to replace the old string with"),
):
    if doc_id not in docs:
        raise ValueError(f"Document with ID {doc_id} not found")

    docs[doc_id] = docs[doc_id].replace(old_string, new_string)

@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs() -> list[str]:
    return list(docs.keys())

@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with ID {doc_id} not found")
    return docs[doc_id]

# TODO: Write a prompt to rewrite a doc in markdown format
@mcp.prompt(
    name="format",
    description="Rewrites the contents of the document in Markdown format"
)
def format_doc(
    doc_id: str=Field(description="The ID of the document to format")
    ) -> list[base.Message]:
    prompt = f"""
    Your goal is to reformat a document to be written with markdown syntax.

    The id of the document you need to reformat is:
    <document_id>
    {doc_id}
    </document_id>

    Add in headers, bullet points, tables, etc as necessary. Feel free to add in extra text, but don't change the meaning of the report.
    Use the 'edit_document' tool to edit the document. After the document has been edited, respond with the final version of the doc. Don't explain your changes.
    """

    return [
        base.UserMessage(prompt)
    ]


# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
