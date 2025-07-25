# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python package implementing document-related tools for converting and processing document formats. The tools are exposed through an MCP (Model Context Protocol) server interface using FastMCP for seamless integration with AI assistants.

## Development Commands

### Setup
```bash
# Create virtual environment and activate it
uv venv
source .venv/bin/activate

# Install package in development mode
uv pip install -e .
```

### Running
```bash
# Start the MCP server
uv run main.py
```

### Testing
```bash
# Run all tests
uv run pytest

# Run a specific test file
uv run pytest tests/test_document.py

# Run a specific test class or method
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_docx
```

## Architecture

### MCP Server Structure
The application uses FastMCP to create an MCP server that exposes tools as callable functions:

- **main.py**: Entry point that creates the FastMCP server instance and registers tools
- **tools/**: Directory containing all tool implementations
- **tests/**: Test suite with fixtures for document conversion testing

### Tool Registration Pattern
Tools are registered with the MCP server using the decorator pattern:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("server_name")
mcp.tool()(function_name)
```

### Tool Definition Guidelines
All tools should follow these patterns from the README:

#### Function Signature
Use Pydantic `Field` for parameter descriptions:
```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does")
) -> ReturnType:
    """Comprehensive docstring here"""
    # Implementation
```

#### Documentation Structure
Tool docstrings should include:
- Begin with a one-line summary
- Provide detailed explanation of functionality  
- Explain when to use (and not use) the tool
- Include usage examples with expected input/output

Example from tools/math.py:
```python
def add(
    a: float = Field(description="First number to add"),
    b: float = Field(description="Second number to add"),
) -> float:
    """Add two numbers together.

    Takes two numerical inputs and returns their sum. This tool handles
    integers and floating point numbers.

    When to use:
    - When you need to perform simple addition
    - When you need precise numerical calculation

    Examples:
    >>> add(2, 3)
    5.0
    >>> add(2.5, 3.5)
    6.0
    """
    return a + b
```

### Current Tools
- **math.py**: Basic mathematical operations (currently only addition)
- **document.py**: Document conversion utilities using MarkItDown library for converting binary documents to markdown

### Testing Structure
- Tests use pytest framework
- Fixture files located in `tests/fixtures/` (DOCX and PDF samples)
- Test classes follow naming pattern `Test[FunctionName]`
- Binary document tests verify conversion output contains markdown formatting

### Dependencies
Key dependencies managed via uv:
- `markitdown[docx,pdf]`: Document conversion library
- `mcp[cli]`: Model Context Protocol server implementation
- `pydantic`: Data validation and type hints
- `pytest`: Testing framework

## Claude Code Best Practices

### Code Quality Guidelines
- Always apply appropriate types to function args