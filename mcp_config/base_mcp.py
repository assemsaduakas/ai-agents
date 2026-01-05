from abc import ABC, abstractmethod

class BaseMCPTool(ABC):
    def __init__(self, schema: dict):
        self.schema = schema

    @abstractmethod
    def execute(self, params: dict) -> dict:
        pass
