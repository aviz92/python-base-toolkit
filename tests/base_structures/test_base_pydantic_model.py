import json

from python_base_toolkit.base_structures.base_pydantic_model import BasePydanticModel


class User(BasePydanticModel):
    name: str
    age: int


class TestBasePydanticModel:
    def test_str_includes_class_name_and_fields(self) -> None:
        user = User(name="avi", age=30)
        assert str(user) == "User({'name': 'avi', 'age': 30})", f"Got {str(user)!r}"

    def test_to_dict_returns_model_dump(self) -> None:
        user = User(name="avi", age=30)
        assert user.to_dict() == {"name": "avi", "age": 30}, f"Got {user.to_dict()}"

    def test_to_dict_forwards_kwargs(self) -> None:
        user = User(name="avi", age=30)
        assert user.to_dict(exclude={"age"}) == {"name": "avi"}, "kwargs should reach model_dump"

    def test_to_json_returns_valid_json(self) -> None:
        user = User(name="avi", age=30)
        assert json.loads(user.to_json()) == {"name": "avi", "age": 30}, f"Got {user.to_json()}"

    def test_values_returns_field_values(self) -> None:
        assert User(name="avi", age=30).values() == ["avi", 30], "Values order should follow field order"

    def test_field_names_returns_declared_fields(self) -> None:
        assert User.field_names() == ["name", "age"], f"Got {User.field_names()}"

    def test_has_field_returns_true_for_declared_field(self) -> None:
        assert User.has_field("name"), "name should be a field"

    def test_has_field_returns_false_for_unknown_field(self) -> None:
        assert not User.has_field("email"), "email should not be a field"

    def test_to_schema_dict_contains_properties(self) -> None:
        schema = User.to_schema_dict()
        assert set(schema["properties"]) == {"name", "age"}, f"Got {schema}"
