from typing import Dict, Any

class JsonSerializable:
    def to_json(self) -> Dict[str, Any]:
        pass

    @staticmethod
    def deserialize(json: Dict[str, Any]) -> 'JsonSerializable':
        pass

    @staticmethod
    def serialize(self) -> str:
        pass