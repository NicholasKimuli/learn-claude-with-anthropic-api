from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pathlib import Path
from pydantic import Field


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(description="Path to the PDF or DOCX file to convert")
) -> str:
    """Convert a PDF or DOCX file to markdown-formatted text.

    Takes a file path to a PDF or DOCX document, reads the file, and converts
    its contents to markdown format using the MarkItDown library.

    When to use:
    - When you need to convert document files to markdown format
    - When you have a file path rather than binary data
    - For processing PDF and DOCX documents

    Args:
        file_path: Path to the PDF or DOCX file to convert

    Returns:
        String containing the markdown-formatted content of the document

    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the file type is not supported (not PDF or DOCX)
        Exception: For other file reading or conversion errors

    Examples:
    >>> document_path_to_markdown("document.pdf")
    "# Document Title\n\nDocument content here..."
    >>> document_path_to_markdown("report.docx")
    "## Report\n\n- Item 1\n- Item 2"
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    
    extension = path.suffix.lower()
    if extension not in ['.pdf', '.docx']:
        raise ValueError(f"Unsupported file type: {extension}. Only PDF and DOCX files are supported.")
    
    try:
        with open(path, 'rb') as file:
            binary_data = file.read()
        
        return binary_document_to_markdown(binary_data, extension)
    except Exception as e:
        raise Exception(f"Error converting document: {str(e)}")
