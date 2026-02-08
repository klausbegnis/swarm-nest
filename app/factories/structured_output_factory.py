"""
File: structured_output_factory.py
Project: swarm-nest
Created: Sunday, 8th February 2026 6:20:21 pm
Author: Klaus Begnis

Copyright (c) 2026 Swarm Nest. See LICENSE for details.
"""

from typing import Any

from pydantic import BaseModel, create_model

# Mapeamento de tipo string para tipo Python/Pydantic
TYPE_MAP: dict[str, type] = {
    "int": int,
    "str": str,
    "float": float,
    "bool": bool,
    "list": list,
    "dict": dict,
    "any": Any,
}


class StructuredOutputFactory:
    """
    Factory for creating structured output models.
    """

    def create_structured_output_model(
        self,
        fields: list[dict[str, str]],
        model_name: str = "DynamicModel",
    ) -> type[BaseModel]:
        """
        Create a Pydantic model class from a schema of fields.

        Args:
            fields: List in the format
                [{"type": "int", "field_name": "total"}, ...].
            model_name: Name of the generated model.

        Returns:
            Pydantic model class (not an instance).
        """
        self._validate_fields_input(fields)
        model = self._create_model_from_fields(fields, model_name=model_name)
        return model

    def _validate_fields_input(self, fields: list[dict[str, str]]) -> None:
        """
        Validate the fields input.

        Args:
            fields: List in the format
                [{"type": "int", "field_name": "total"}, ...].
        """
        for item in fields:
            field_name = item.get("field_name")
            field_type = item.get("type")
            if not field_name:
                raise ValueError("Each item must have 'field_name'")
            if not field_type:
                raise ValueError("Each item must have 'type'")
            try:
                field_type = str(field_type).lower().strip()
                field_name = str(field_name).strip()
            except TypeError as err:
                raise ValueError(
                    f"Invalid field configuration: {item}"
                ) from err
            if field_type not in TYPE_MAP:
                raise ValueError(f"Invalid type: {field_type}")

    def _create_model_from_fields(
        self,
        fields: list[dict[str, str]],
        model_name: str = "DynamicModel",
    ) -> type[BaseModel]:
        """
        Create a Pydantic dynamic model from a list of field definitions.

        Args:
            fields: List in the format
                [{"type": "int", "field_name": "total"}, ...].
            model_name: Name of the generated model.

        Returns:
            Pydantic model class.
        """
        field_defs: dict[str, tuple[type, ...]] = {}
        for item in fields:
            field_name = item.get("field_name")
            if not field_name:
                raise ValueError("Each item must have 'field_name'")
            type_str = (item.get("type") or "str").strip().lower()
            py_type = TYPE_MAP.get(type_str, str)
            field_defs[field_name] = (py_type, ...)  # ... = required

        return create_model(model_name, **field_defs)
