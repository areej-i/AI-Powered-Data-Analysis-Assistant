from enum import Enum

from pydantic import BaseModel

class Operation(str, Enum):
    mean = "mean"
    sum = "sum"
    max = "max"
    min = "min"
    median = "median"
    count = "count"
    missing_values = "missing_values"
    unique_values = "unique_values"

class AnalysisRequest(BaseModel):
    intent: str
    operation: Operation | None = None
    group_by: str | None = None
    value_column: str | None = None

class DatasetAnalysis(BaseModel):
    dataset_type: str
    summary: str
    important_columns: list[str]
    analysis_questions: list[str]