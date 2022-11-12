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
                callable(subclass.delete) and
                hasattr(subclass, 'render') and
                callable(subclass.render) or
                NotImplemented)

    @abc.abstractmethod
    def create(self, path: str, file_name: str, rendered_template: DocxTemplate) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, full_file_path: str):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, full_file_path: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def render(self, path: str, full_file_path: str, data: dict) -> DocxTemplate:
        raise NotImplementedError


class FileManagerLocal(FileManagerInterface):
    def create(self, path: str, file_name: str, rendered_template: DocxTemplate) -> str:
        path_to_storage = Path(path) / file_name
        rendered_template.save(path_to_storage)
        return str(path_to_storage)

    def get(self, full_file_path: str) -> bytes:
        with open(Path(full_file_path), "rb") as in_file:
            yield from in_file

    def delete(self, full_file_path: str) -> str:
        Path(full_file_path).unlink()
        return f"Successfully deleted file {full_file_path}"

    def render(self, path: str, file_name: str, data: dict) -> DocxTemplate:
        full_file_path = Path(path) / file_name
        template = DocxTemplate(full_file_path)
        template.render(data)
        return template


file_manager = FileManagerLocal()
