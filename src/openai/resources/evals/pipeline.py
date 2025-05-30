from __future__ import annotations

import time
from typing import List, Dict, Any, Union, cast, Protocol
from openai import OpenAI
from enum import Enum
import pandas as pd

from .data_sources import DataSource

# Any grader object only needs a to_dict() method; no need to list them here.
class _GraderProtocol(Protocol):
    def to_dict(self) -> Dict[str, Any]: ...

Grader = Union[
    Dict[str, Any],
    _GraderProtocol,
]

class RunStatus(str, Enum):
            QUEUED = "queued"
            IN_PROGRESS = "in_progress"
            COMPLETED = "completed"
            FAILED = "failed"
            CANCELED = "canceled"

class ReturnFormat(str, Enum):
        RESPONSE = "response"
        JSONL = "jsonl"
        DATAFRAME = "dataframe"       

class EvalPipeline:
    
    def __init__(
        self,
        *,
        data_source: DataSource,
        graders: List[Grader],
        name: str | None = None,
    ) -> None:
        self._data_source = data_source
        self._testing_criteria: List[Dict[str, Any]] = [
            g if isinstance(g, dict) else g.to_dict()  # type: ignore[attr-defined]
            for g in graders
        ]
        self._name = name or "eval-pipeline"
        self._client = OpenAI()


    def run_pipeline(
        self,
        *,
        poll_interval: float = 2.0,
        timeout: float = 600.0,
        return_format: Union["ReturnFormat", None] = ReturnFormat.RESPONSE,
        **kwargs: Any,
    ):
      
        eval_obj = self._client.evals.create(  # type: ignore[arg-type]
            data_source_config=self._data_source.data_source_config,  # type: ignore[arg-type]
            testing_criteria=self._testing_criteria,  # type: ignore[arg-type]
            name=self._name,
            **kwargs,
        )

        
        run_obj = self._client.evals.runs.create(  # type: ignore[arg-type]
            eval_id=eval_obj.id,
            data_source=cast(Any, self._data_source.data_source),  # type: ignore[arg-type]
            name=self._name,
            **kwargs,
        )

        TERMINAL_STATUSES = {
            RunStatus.COMPLETED.value,
            RunStatus.FAILED.value,
            RunStatus.CANCELED.value,
        }

        start = time.time()
        while True:
            run = self._client.evals.runs.retrieve(eval_id=eval_obj.id, run_id=run_obj.id)
            if run.status in TERMINAL_STATUSES:
                # Wait for all output items to be available
                expected = len(self._data_source.data_source["source"]["content"])
                t0 = time.time()
                while True:
                    page = self._client.evals.runs.output_items.list(
                        eval_id=eval_obj.id,
                        run_id=run.id,
                        limit=100,
                    )
                    all_items = page.data
                    if len(all_items) >= expected or (time.time() - t0) > 10:
                        break
                    time.sleep(0.5)

                if return_format is ReturnFormat.RESPONSE:
                    return run

                all_items: List[Any] = []
                after: str | None = None
                while True:
                    page = self._client.evals.runs.output_items.list(  # type: ignore[arg-type]
                        eval_id=eval_obj.id,
                        run_id=run.id,
                        limit=100,
                        after=after,  # type: ignore[arg-type]
                    )
                    all_items.extend(page.data)  # type: ignore[attr-defined]
                    after = getattr(page, "after", None)  # type: ignore[attr-defined]
                    if not after:
                        break

                items_page = page  # last fetched page object
                items_page.data = all_items  # type: ignore[attr-defined]

                print("Fetched items:", len(all_items))
                print("All items:", [item.datasource_item for item in all_items])

                rf = return_format or ReturnFormat.RESPONSE
                if rf is ReturnFormat.RESPONSE:
                    return [item.datasource_item for item in items_page.data]  # type: ignore[attr-defined]
                elif rf is ReturnFormat.JSONL:
                    return [item.datasource_item for item in items_page.data]  # type: ignore[attr-defined]
                elif rf is ReturnFormat.DATAFRAME:
                    return self._to_dataframe_output_items(items_page)
                else:
                    raise ValueError("Unsupported ReturnFormat value")

            if time.time() - start > timeout:
                raise TimeoutError(
                    f"Run did not complete within {timeout} seconds (last status={run.status})."
                )

            time.sleep(poll_interval)


    @staticmethod
    def _to_dataframe_output_items(page: Any):
        """Convert OutputItems page to a pandas DataFrame (logic inlined)."""
        rows: List[Dict[str, Any]] = []
        for item in page.data:  # type: ignore[attr-defined]
            row: Dict[str, Any] = {
                "id": item.id,  # type: ignore[attr-defined]
                "created_at": item.created_at,  # type: ignore[attr-defined]
                "datasource_item": item.datasource_item,  # type: ignore[attr-defined]
                "datasource_item_id": item.datasource_item_id,  # type: ignore[attr-defined]
                "eval_id": item.eval_id,  # type: ignore[attr-defined]
                "object": item.object,  # type: ignore[attr-defined]
                "results": item.results,  # type: ignore[attr-defined]
                "run_id": item.run_id,  # type: ignore[attr-defined]
                "status": item.status,  # type: ignore[attr-defined]
            }
            for k, v in item.datasource_item.items():  # type: ignore[attr-defined]
                row[f"datasource_item.{k}"] = str(v)
            if item.results and len(item.results) == 1:  # type: ignore[attr-defined]
                for k, v in item.results[0].items():  # type: ignore[index]
                    row[f"result.{k}"] = str(v)
            rows.append(row)
        return pd.DataFrame(rows)

   