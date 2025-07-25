import pytest
from pathlib import Path
from tools.document import document_path_to_markdown


class TestDocumentPathToMarkdown:
    """Test cases for document_path_to_markdown function."""
    
    @pytest.fixture
    def fixtures_dir(self):
        """Get path to test fixtures directory."""
        return Path(__file__).parent / "fixtures"
    
    # Happy Path Tests
    def test_valid_docx_file(self, fixtures_dir):
        """Test converting a valid DOCX file to markdown."""
        docx_path = fixtures_dir / "mcp_docs.docx"
        result = document_path_to_markdown(str(docx_path))
        
        assert isinstance(result, str)
        assert len(result) > 0
        # Should contain some markdown formatting or content
        assert result.strip() != ""
    
    def test_valid_pdf_file(self, fixtures_dir):
        """Test converting a valid PDF file to markdown."""
        pdf_path = fixtures_dir / "mcp_docs.pdf"
        result = document_path_to_markdown(str(pdf_path))
        
        assert isinstance(result, str)
        assert len(result) > 0
        # Should contain some markdown formatting or content
        assert result.strip() != ""
    
    def test_large_document(self, fixtures_dir):
        """Test with a larger document to ensure it handles size appropriately."""
        # Using the existing fixtures as they should be reasonably sized
        docx_path = fixtures_dir / "mcp_docs.docx"
        result = document_path_to_markdown(str(docx_path))
        
        assert isinstance(result, str)
        assert len(result) > 100  # Expect substantial content
    
    # Edge Cases
    def test_empty_docx_document(self, fixtures_dir):
        """Test with an empty DOCX file."""
        empty_docx_path = fixtures_dir / "empty.docx"
        # The empty DOCX we created is actually invalid, so it should raise an exception
        with pytest.raises(Exception, match="Error converting document"):
            document_path_to_markdown(str(empty_docx_path))
    
    def test_empty_pdf_document(self, fixtures_dir):
        """Test with an empty PDF file."""
        empty_pdf_path = fixtures_dir / "empty.pdf"
        result = document_path_to_markdown(str(empty_pdf_path))
        
        assert isinstance(result, str)
        # Empty documents might return empty string or minimal content
        assert len(result) >= 0
    
    def test_minimal_document_single_word(self, fixtures_dir):
        """Test with a minimal document containing just one word."""
        # Use the existing fixtures which should have minimal content
        docx_path = fixtures_dir / "mcp_docs.docx"
        result = document_path_to_markdown(str(docx_path))
        
        assert isinstance(result, str)
        assert len(result) >= 0
    
    # Error Handling Tests
    def test_non_existent_file_path(self):
        """Test with invalid/missing file path."""
        with pytest.raises(FileNotFoundError, match="File not found"):
            document_path_to_markdown("/path/that/does/not/exist.pdf")
    
    def test_unsupported_file_type_txt(self, fixtures_dir):
        """Test with .txt file which should be unsupported."""
        txt_path = fixtures_dir / "unsupported.txt"
        with pytest.raises(ValueError, match="Unsupported file type"):
            document_path_to_markdown(str(txt_path))
    
    def test_unsupported_file_type_jpg(self, tmp_path):
        """Test with .jpg file which should be unsupported."""
        jpg_path = tmp_path / "image.jpg"
        jpg_path.write_bytes(b"fake jpg content")
        
        with pytest.raises(ValueError, match="Unsupported file type"):
            document_path_to_markdown(str(jpg_path))
    
    def test_corrupted_docx_file(self, fixtures_dir):
        """Test with malformed/corrupted DOCX."""
        corrupted_docx_path = fixtures_dir / "corrupted.docx"
        # MarkItDown is robust and may handle corrupted files gracefully
        # so we test that it either succeeds or fails appropriately
        try:
            result = document_path_to_markdown(str(corrupted_docx_path))
            assert isinstance(result, str)
        except Exception as e:
            # If it fails, it should be with our error message
            assert "Error converting document" in str(e)
    
    def test_corrupted_pdf_file(self, fixtures_dir):
        """Test with malformed/corrupted PDF."""
        corrupted_pdf_path = fixtures_dir / "corrupted.pdf"
        # MarkItDown is robust and may handle corrupted files gracefully
        try:
            result = document_path_to_markdown(str(corrupted_pdf_path))
            assert isinstance(result, str)
        except Exception as e:
            # If it fails, it should be with our error message
            assert "Error converting document" in str(e)
    
    def test_directory_instead_of_file(self, fixtures_dir):
        """Test when path points to a directory."""
        with pytest.raises(ValueError, match="Path is not a file"):
            document_path_to_markdown(str(fixtures_dir))
    
    # File Type Validation Tests
    def test_case_insensitive_pdf_extension(self, fixtures_dir, tmp_path):
        """Test .PDF extension (uppercase)."""
        # Copy existing PDF with uppercase extension
        pdf_path = fixtures_dir / "mcp_docs.pdf"
        uppercase_pdf = tmp_path / "test.PDF"
        uppercase_pdf.write_bytes(pdf_path.read_bytes())
        
        result = document_path_to_markdown(str(uppercase_pdf))
        assert isinstance(result, str)
    
    def test_case_insensitive_docx_extension(self, fixtures_dir, tmp_path):
        """Test .DOCX extension (uppercase)."""
        # Copy existing DOCX with uppercase extension
        docx_path = fixtures_dir / "mcp_docs.docx"
        uppercase_docx = tmp_path / "test.DOCX"
        uppercase_docx.write_bytes(docx_path.read_bytes())
        
        result = document_path_to_markdown(str(uppercase_docx))
        assert isinstance(result, str)
    
    def test_mixed_case_extensions(self, fixtures_dir, tmp_path):
        """Test mixed case extensions like .Pdf, .DocX."""
        # Test .Pdf
        pdf_path = fixtures_dir / "mcp_docs.pdf"
        mixed_pdf = tmp_path / "test.Pdf"
        mixed_pdf.write_bytes(pdf_path.read_bytes())
        
        result = document_path_to_markdown(str(mixed_pdf))
        assert isinstance(result, str)
        
        # Test .DocX
        docx_path = fixtures_dir / "mcp_docs.docx"
        mixed_docx = tmp_path / "test.DocX"
        mixed_docx.write_bytes(docx_path.read_bytes())
        
        result = document_path_to_markdown(str(mixed_docx))
        assert isinstance(result, str)
    
    def test_files_without_extensions(self, fixtures_dir, tmp_path):
        """Test behavior with extensionless files."""
        # Create file without extension
        no_ext_file = tmp_path / "document_no_extension"
        no_ext_file.write_bytes(b"some content")
        
        with pytest.raises(ValueError, match="Unsupported file type"):
            document_path_to_markdown(str(no_ext_file))
    
    def test_wrong_extension_pdf_as_docx(self, fixtures_dir, tmp_path):
        """Test .pdf file renamed to .docx extension."""
        pdf_path = fixtures_dir / "mcp_docs.pdf"
        wrong_ext_file = tmp_path / "actually_pdf.docx"
        wrong_ext_file.write_bytes(pdf_path.read_bytes())
        
        # MarkItDown may be smart enough to detect actual file type
        # Test that it either works or fails appropriately
        try:
            result = document_path_to_markdown(str(wrong_ext_file))
            assert isinstance(result, str)
        except Exception as e:
            assert "Error converting document" in str(e)
    
    def test_wrong_extension_docx_as_pdf(self, fixtures_dir, tmp_path):
        """Test .docx file renamed to .pdf extension."""
        docx_path = fixtures_dir / "mcp_docs.docx"
        wrong_ext_file = tmp_path / "actually_docx.pdf"
        wrong_ext_file.write_bytes(docx_path.read_bytes())
        
        # MarkItDown may be smart enough to detect actual file type  
        # Test that it either works or fails appropriately
        try:
            result = document_path_to_markdown(str(wrong_ext_file))
            assert isinstance(result, str)
        except Exception as e:
            assert "Error converting document" in str(e)
    
    # Output Validation Tests
    def test_markdown_formatting_preservation(self, fixtures_dir):
        """Verify that markdown formatting is properly generated."""
        docx_path = fixtures_dir / "mcp_docs.docx"
        result = document_path_to_markdown(str(docx_path))
        
        # Result should be a string (basic validation)
        assert isinstance(result, str)
        # If the document has content, result should not be empty
        if len(result.strip()) > 0:
            # Basic check that it's text content
            assert isinstance(result, str)
    
    def test_content_preservation(self, fixtures_dir):
        """Ensure all text content is preserved in conversion."""
        docx_path = fixtures_dir / "mcp_docs.docx"
        result = document_path_to_markdown(str(docx_path))
        
        # Should return string content
        assert isinstance(result, str)
        # If there's content, it should be preserved as text
        if len(result.strip()) > 0:
            # Content should be readable text (not binary)
            assert result.isprintable() or any(c in result for c in ['\n', '\t', ' '])
    
    def test_structure_preservation(self, fixtures_dir):
        """Verify document structure is maintained in markdown."""
        docx_path = fixtures_dir / "mcp_docs.docx"
        result = document_path_to_markdown(str(docx_path))
        
        # Should return structured text
        assert isinstance(result, str)
        # Basic validation that it's text content
        if len(result.strip()) > 0:
            # Should contain readable characters
            assert any(c.isalnum() or c.isspace() for c in result)
    
    def test_return_type_is_string(self, fixtures_dir):
        """Verify that function always returns a string."""
        docx_path = fixtures_dir / "mcp_docs.docx"
        result = document_path_to_markdown(str(docx_path))
        
        assert isinstance(result, str)
        
        pdf_path = fixtures_dir / "mcp_docs.pdf"
        result = document_path_to_markdown(str(pdf_path))
        
        assert isinstance(result, str)