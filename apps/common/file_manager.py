import abc

from docxtpl import DocxTemplate
from pathlib import Path


class FileManagerInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'create') and 
                callable(subclass.create) and 
                hasattr(subclass, 'get') and 
                callable(subclass.get) and 
                hasattr(subclass, 'delete') and 
                callable(subclass.delete) or 
                NotImplemented)

    @abc.abstractmethod
    def create(self, path: str, file_name: str, rendered_template: DocxTemplate) -> str:
        """Create new file"""
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, full_file_path: str):
        """Get file"""
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, full_file_path: str) -> str:
        """Delete file"""
        raise NotImplementedError

    @abc.abstractmethod
    def render(self,path: str, full_file_path: str, data: dict) -> DocxTemplate:
        """Render template file"""
        raise NotImplementedError


class FileManagerLocal(FileManagerInterface):
    """Extract text from a PDF."""
    def create(self, path: str, file_name: str, rendered_template: DocxTemplate) -> str:
        """Overrides FormalParserInterface.load_data_source()"""
        path_to_storage = path / file_name
        rendered_template.save(path_to_storage)
        return path_to_storage

    def get(self, full_file_path: str) -> bytes:
        """Overrides FormalParserInterface.extract_text()"""
        with open(full_file_path, "rb") as in_file:
            data = in_file.read()
        return data

    def delete(self, full_file_path: str) -> str:
        """Overrides FormalParserInterface.extract_text()"""
        Path(full_file_path).unlink()
        return f"Successfully deleted file {full_file_path}"

    def render(self, path: str, file_name: str, data: dict) -> DocxTemplate:
        full_file_path = path / file_name
        template = DocxTemplate(full_file_path)
        template.render(data)
        return template
