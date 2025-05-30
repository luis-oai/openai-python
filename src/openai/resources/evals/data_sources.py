from __future__ import annotations

import pandas as pd
from typing import Any, Dict, Tuple, cast
from enum import Enum


class DataSource:
    
    class RunType(str, Enum):
        JSONL = "jsonl"
        COMPLETIONS = "completions"
        STORED_COMPLETIONS = "stored_completions"
        RESPONSES = "responses"

    class JSONLSource(str, Enum):
        FILE_CONTENT = "file_content"
        FILE_ID = "file_id"

    def __init__(self, *, _config: Dict[str, Any], _source: Dict[str, Any]):
        """Use the class-methods below instead of instantiating directly."""
        self.data_source_config: Dict[str, Any] = _config
        self.data_source: Dict[str, Any] = _source


    @classmethod
    def from_dataframe(cls, df: "pd.DataFrame") -> "DataSource":
        config = cls._schema_from_dataframe(df)
        source = {
            "type": cls.RunType.JSONL.value,
            "source": {
                "type": cls.JSONLSource.FILE_CONTENT.value,
                "content": cls.df_to_jsonl(df),
            },
        }
        return cls(_config=config, _source=source)

    @classmethod
    def from_jsonl_file_content(
        cls,
        rows: "list[dict[str, Any]]",
        *,
        config: "dict[str, Any] | None" = None,
    ) -> "DataSource":
        if config is None:
            config = cls._schema_from_jsonl(rows)

        source = {
            "type": cls.RunType.JSONL.value,
            "source": {"type": cls.JSONLSource.FILE_CONTENT.value, "content": rows},
        }
        return cls(_config=config, _source=source)

    @classmethod
    def from_jsonl_file_id(
        cls,
        file_id: str,
        *,
        config: Dict[str, Any],
    ) -> "DataSource":
        source = {
            "type": cls.RunType.JSONL.value,
            "source": {"type": cls.JSONLSource.FILE_ID.value, "id": file_id},
        }
        return cls(_config=config, _source=source)


    @classmethod
    def from_completions_file_content(
        cls,
        rows: "list[dict[str, Any]]",
        *,
        model: str,
        input_messages: Dict[str, Any] | None = None,
        sampling_params: Dict[str, Any] | None = None,
        config: Dict[str, Any] | None = None,
    ) -> "DataSource":
        if config is None:
            config = cls._schema_from_jsonl(rows)

        source = {
            "type": cls.RunType.COMPLETIONS.value,
            "source": {"type": cls.JSONLSource.FILE_CONTENT.value, "content": rows},
            "model": model,
        }
        if input_messages is not None:
            source["input_messages"] = input_messages  # type: ignore[index]
        if sampling_params is not None:
            source["sampling_params"] = sampling_params  # type: ignore[index]

        return cls(_config=config, _source=source)  # type: ignore[arg-type]

    @classmethod
    def from_stored_completions(
        cls,
        *,
        created_after: int | None = None,
        created_before: int | None = None,
        limit: int | None = None,
        metadata: Dict[str, Any] | None = None,
        model: str | None = None,
        config: Dict[str, Any],
    ) -> "DataSource":
        source: Dict[str, Any] = {
            "type": cls.RunType.STORED_COMPLETIONS.value,
        }
        if created_after is not None:
            source["created_after"] = created_after
        if created_before is not None:
            source["created_before"] = created_before
        if limit is not None:
            source["limit"] = limit
        if metadata is not None:
            source["metadata"] = metadata
        if model is not None:
            source["model"] = model

        return cls(_config=config, _source=source)

    @classmethod
    def from_completions_file_id(
        cls,
        *,
        file_id: str,
        model: str,
        input_messages: Dict[str, Any] | None = None,
        sampling_params: Dict[str, Any] | None = None,
        config: Dict[str, Any],
    ) -> "DataSource":
        source: Dict[str, Any] = {
            "type": cls.RunType.COMPLETIONS.value,
            "source": {"type": cls.JSONLSource.FILE_ID.value, "id": file_id},
            "model": model,
        }
        if input_messages is not None:
            source["input_messages"] = input_messages  # type: ignore[index]
        if sampling_params is not None:
            source["sampling_params"] = sampling_params  # type: ignore[index]

        return cls(_config=config, _source=source)

    @classmethod
    def from_responses_file_content(
        cls,
        rows: "list[dict[str, Any]]",
        *,
        input_messages: Dict[str, Any] | None = None,
        model: str | None = None,
        sampling_params: Dict[str, Any] | None = None,
        config: Dict[str, Any] | None = None,
    ) -> "DataSource":
        if config is None:
            config = cls._schema_from_jsonl(rows)

        source: Dict[str, Any] = {
            "type": cls.RunType.RESPONSES.value,
            "source": {"type": cls.JSONLSource.FILE_CONTENT.value, "content": rows},
        }
        if input_messages is not None:
            source["input_messages"] = input_messages  # type: ignore[index]
        if model is not None:
            source["model"] = model  # type: ignore[index]
        if sampling_params is not None:
            source["sampling_params"] = sampling_params  # type: ignore[index]

        return cls(_config=config, _source=source)

    @classmethod
    def from_responses_file_id(
        cls,
        *,
        file_id: str,
        input_messages: Dict[str, Any] | None = None,
        model: str | None = None,
        sampling_params: Dict[str, Any] | None = None,
        config: Dict[str, Any],
    ) -> "DataSource":
        source: Dict[str, Any] = {
            "type": cls.RunType.RESPONSES.value,
            "source": {"type": cls.JSONLSource.FILE_ID.value, "id": file_id},
        }
        if input_messages is not None:
            source["input_messages"] = input_messages  # type: ignore[index]
        if model is not None:
            source["model"] = model  # type: ignore[index]
        if sampling_params is not None:
            source["sampling_params"] = sampling_params  # type: ignore[index]

        return cls(_config=config, _source=source)

    @classmethod
    def from_responses_query(
        cls,
        *,
        filters: Dict[str, Any],
        input_messages: Dict[str, Any] | None = None,
        model: str | None = None,
        sampling_params: Dict[str, Any] | None = None,
        config: Dict[str, Any],
    ) -> "DataSource":
        source: Dict[str, Any] = {"type": cls.RunType.RESPONSES.value, "source": filters}
        if input_messages is not None:
            source["input_messages"] = input_messages  # type: ignore[index]
        if model is not None:
            source["model"] = model  # type: ignore[index]
        if sampling_params is not None:
            source["sampling_params"] = sampling_params  # type: ignore[index]

        return cls(_config=config, _source=source)

    @staticmethod
    def _schema_from_dataframe(df: "pd.DataFrame") -> Dict[str, Any]:
        # Infer schema from DataFrame columns and dtypes
        properties = {}
        type_map = {
            "object": "string",
            "int64": "integer",
            "float64": "number",
            "bool": "boolean",
        }
        for col, dtype in df.dtypes.items():  # type: ignore[attr-defined]
            dtype_str: str = str(dtype) # type: ignore[arg-type]
            json_type = type_map.get(dtype_str, "string")
            properties[col] = {"type": json_type}
        return {
            "type": "custom",
            "item_schema": {
                "type": "object",
                "properties": properties,
                "required": list(df.columns),
            },
        }

    @staticmethod
    def _schema_from_jsonl(content: "list[dict[str, Any]]") -> Dict[str, Any]:
        """Derive a minimal *custom* schema from JSONL rows."""
        if not content:
            raise ValueError("Cannot infer schema from empty JSONL content.")

        first_item: Dict[str, Any] = cast(Dict[str, Any], content[0].get("item", {}))
        if not first_item:
            raise ValueError("First JSONL row is missing 'item' dict.")

        properties = {str(key): {"type": "string"} for key in first_item.keys()}
        return {
            "type": "custom",
            "item_schema": {
                "type": "object",
                "properties": properties,
                "required": list(first_item.keys()),
            },
        }


    @staticmethod
    def df_to_jsonl(df: "pd.DataFrame") -> "list[dict[str, Any]]":
        """Convert a DataFrame to the JSONL row format required by the API."""
        return [{"item": row} for row in df.to_dict(orient="records")]  # type: ignore

    @staticmethod
    def convert_dataframe_data_source(obj: "dict[str, Any] | pd.DataFrame") -> "dict[str, Any]":
        """Public helper used by Runs.create to normalise its `data_source` arg."""
        if isinstance(obj, pd.DataFrame):
            return {
                "type": DataSource.RunType.JSONL.value,
                "source": {"type": DataSource.JSONLSource.FILE_CONTENT.value, "content": DataSource.df_to_jsonl(obj)},
            }

        if getattr(obj, "get", None) is not None and obj.get("type") == "dataframe":  # type: ignore[arg-type]
            obj["type"] = DataSource.RunType.JSONL.value
            obj["source"]["type"] = DataSource.JSONLSource.FILE_CONTENT.value
            obj["source"]["content"] = DataSource.df_to_jsonl(obj["source"]["data"])
            del obj["source"]["data"]
            return obj

        return obj


    def as_tuple(self) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Return (data_source_config, data_source) tuple."""
        return self.data_source_config, self.data_source


    @staticmethod
    def logs_config(metadata: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Return a *logs* type data_source_config dict."""
        cfg: Dict[str, Any] = {"type": "logs"}
        if metadata is not None:
            cfg["metadata"] = metadata
        return cfg

    @staticmethod
    def custom_config(item_schema: Dict[str, Any], *, include_sample_schema: bool = False) -> Dict[str, Any]:
        """Helper to build *custom* data_source_config with optional sample schema."""
        cfg: Dict[str, Any] = {
            "type": "custom",
            "item_schema": item_schema,
        }
        if include_sample_schema:
            cfg["include_sample_schema"] = True
        return cfg
