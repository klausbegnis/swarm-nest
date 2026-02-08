"""
File: test_structured_output_factory.py
Project: swarm-nest
Created: Sunday, 8th February 2026
Author: Klaus Begnis

Copyright (c) 2026 Swarm Nest. See LICENSE for details.
"""

from pydantic import ValidationError
import pytest

from app.factories.structured_output_factory import (
    TYPE_MAP,
    StructuredOutputFactory,
)


@pytest.fixture
def factory() -> StructuredOutputFactory:
    """Factory instance for tests."""
    return StructuredOutputFactory()


@pytest.mark.unit
def test_create_structured_output_model_returns_model_class(
    factory: StructuredOutputFactory,
) -> None:
    """create_structured_output_model retorna uma classe de modelo Pydantic."""
    fields = [
        {"type": "int", "field_name": "total"},
        {"type": "str", "field_name": "name"},
    ]
    model = factory.create_structured_output_model(fields)
    assert model is not None
    assert hasattr(model, "model_validate")
    # Avoid deprecated model_fields: verify structure via model_construct
    instance = model.model_construct(total=0, name="")
    assert hasattr(instance, "total")
    assert hasattr(instance, "name")


@pytest.mark.unit
def test_create_structured_output_model_instantiates_with_valid_data(
    factory: StructuredOutputFactory,
) -> None:
    """Modelo criado aceita dados válidos e retorna instância."""
    fields = [
        {"type": "int", "field_name": "total"},
        {"type": "str", "field_name": "name"},
    ]
    model = factory.create_structured_output_model(fields)
    obj = model(total=42, name="foo")
    assert obj.total == 42
    assert obj.name == "foo"


@pytest.mark.unit
def test_create_structured_output_model_validates_types(
    factory: StructuredOutputFactory,
) -> None:
    """Modelo rejeita dados com tipo incorreto."""
    fields = [{"type": "int", "field_name": "total"}]
    model = factory.create_structured_output_model(fields)
    with pytest.raises(ValidationError):
        model(total="not_an_int")


@pytest.mark.unit
def test_create_structured_output_model_custom_name(
    factory: StructuredOutputFactory,
) -> None:
    """model_name é aplicado ao modelo gerado."""
    fields = [{"type": "str", "field_name": "x"}]
    model = factory.create_structured_output_model(
        fields, model_name="CustomModel"
    )
    assert model.__name__ == "CustomModel"


@pytest.mark.unit
def test_validate_fields_missing_field_name(
    factory: StructuredOutputFactory,
) -> None:
    """Lista com item sem field_name levanta ValueError."""
    fields = [{"type": "int"}]
    with pytest.raises(ValueError, match="field_name"):
        factory._validate_fields_input(fields)


@pytest.mark.unit
def test_validate_fields_missing_type(
    factory: StructuredOutputFactory,
) -> None:
    """Lista com item sem type levanta ValueError."""
    fields = [{"field_name": "total"}]
    with pytest.raises(ValueError, match="type"):
        factory._validate_fields_input(fields)


@pytest.mark.unit
def test_validate_fields_invalid_type(
    factory: StructuredOutputFactory,
) -> None:
    """Tipo não mapeado levanta ValueError."""
    fields = [{"type": "unknown", "field_name": "x"}]
    with pytest.raises(ValueError, match="Invalid type"):
        factory._validate_fields_input(fields)


@pytest.mark.unit
def test_create_structured_output_model_all_types(
    factory: StructuredOutputFactory,
) -> None:
    """Todos os tipos do TYPE_MAP são aceitos e validam corretamente."""
    fields = [
        {"type": "int", "field_name": "n"},
        {"type": "str", "field_name": "s"},
        {"type": "float", "field_name": "f"},
        {"type": "bool", "field_name": "b"},
        {"type": "list", "field_name": "lst"},
        {"type": "dict", "field_name": "d"},
        {"type": "any", "field_name": "a"},
    ]
    model = factory.create_structured_output_model(fields)
    obj = model(
        n=1,
        s="x",
        f=1.5,
        b=True,
        lst=[1, 2],
        d={"k": "v"},
        a=None,
    )
    assert obj.n == 1
    assert obj.s == "x"
    assert obj.f == 1.5
    assert obj.b is True
    assert obj.lst == [1, 2]
    assert obj.d == {"k": "v"}
    assert obj.a is None


@pytest.mark.unit
def test_type_map_contains_expected_types() -> None:
    """TYPE_MAP contém os tipos esperados."""
    expected = {"int", "str", "float", "bool", "list", "dict", "any"}
    assert set(TYPE_MAP.keys()) == expected


@pytest.mark.unit
def test_create_model_from_fields_empty_field_name_raises(
    factory: StructuredOutputFactory,
) -> None:
    """_create_model_from_fields com field_name vazio levanta ValueError."""
    fields = [{"type": "str", "field_name": ""}]
    with pytest.raises(ValueError, match="field_name"):
        factory._create_model_from_fields(fields)


@pytest.mark.unit
def test_create_structured_output_model_type_case_insensitive(
    factory: StructuredOutputFactory,
) -> None:
    """Tipo em maiúsculas ou misto é aceito (normalizado para minúsculo)."""
    fields = [{"type": "INT", "field_name": "total"}]
    model = factory.create_structured_output_model(fields)
    obj = model(total=10)
    assert obj.total == 10
