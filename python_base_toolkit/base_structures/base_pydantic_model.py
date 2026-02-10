from typing import Any, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound="PydanticMixin")


class BasePydanticModel(BaseModel):
    """Mixin to add Enum-like utility methods to Pydantic BaseModels."""

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.model_dump()})"

    def to_dict(self, **kwargs) -> dict[str, Any]:
        """Wrapper for model_dump."""
        return self.model_dump(**kwargs)

    def to_json(self, **kwargs) -> str:
        """Wrapper for model_dump_json."""
        return self.model_dump_json(**kwargs)

    def values(self) -> list[Any]:
        """Returns a list of the current instance's field values."""
        return list(self.model_dump().values())

    @classmethod
    def field_names(cls) -> list[str]:
        """Returns a list of all field names defined in the model."""
        return list(cls.model_fields.keys())

    @classmethod
    def has_field(cls, name: str) -> bool:
        """Checks if a field name exists in the model definition."""
        return name in cls.model_fields

    @classmethod
    def to_schema_dict(cls) -> dict[str, Any]:
        """Returns the JSON schema of the model as a dictionary."""
        return cls.model_json_schema()
