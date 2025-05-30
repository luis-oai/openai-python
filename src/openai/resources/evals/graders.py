from enum import Enum
from typing import Optional, Dict, Union, Any


class DirectCheckOp(Enum):
    EQUALS = "eq"
    NOT_EQUALS = "neq"
    LIKE = "like"
    ILIKE = "ilike"


class SimilarityCheckOp(Enum):
    """Enumeration of supported text similarity evaluation metrics."""

    FUZZY_MATCH = "fuzzy_match"
    BLEU = "bleu"
    GLEU = "gleu"
    METEOR = "meteor"
    ROUGE_1 = "rouge_1"
    ROUGE_2 = "rouge_2"
    ROUGE_3 = "rouge_3"
    ROUGE_4 = "rouge_4"
    ROUGE_5 = "rouge_5"
    ROUGE_L = "rouge_l"    
    

class PointWiseStringCheckGrader:
    TYPE = "string_check"
    def __init__(self, input: str,
                 reference: str,
                 operation: DirectCheckOp,
                 name: str = "PointWiseStringCheckGrader"):
        self.input = input
        self.reference = reference
        self.operation = operation
        self.name = name
        self.type = self.TYPE

    def to_dict(self) -> 'Dict[str, str]':
        return {
            "type": self.type,
            "name": self.name,
            "input": self.input,
            "reference": self.reference,
            "operation": self.operation.value,
        }
    

class PairWiseStringCheckGrader:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Placeholder for pair-wise string check grader."""
        raise NotImplementedError("PairWiseStringCheckGrader is not implemented yet.")


class PointWiseTextSimilarityGrader:
    TYPE = "text_similarity"
    def __init__(
        self,
        evaluation_metric: SimilarityCheckOp,
        input: str,
        reference: str,
        pass_threshold: float,
        name: str = "PointWiseTextSimilarityGrader",
    ) -> None:
        self.evaluation_metric = evaluation_metric
        self.input = input
        self.reference = reference
        self.pass_threshold = pass_threshold
        self.name = name
        self.type = self.TYPE

    def to_dict(self) -> "Dict[str, Union[str, float]]":
        return {
            "type": self.type,
            "name": self.name,
            "evaluation_metric": self.evaluation_metric.value,
            "input": self.input,
            "reference": self.reference,
            "pass_threshold": self.pass_threshold,
        }

class PairWiseTextSimilarityGrader:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Placeholder for pair-wise text similarity grader."""
        raise NotImplementedError("PairWiseTextSimilarityGrader is not implemented yet.")

class PointWisePythonGrader:
    TYPE = "python"
    def __init__(
        self,
        source: str,
        image_tag: Optional[str] = None,
        pass_threshold: Optional[float] = None,
        name: str = "PointWisePythonGrader",
    ) -> None:
        self.name = name
        self.source = source
        self.image_tag = image_tag
        self.pass_threshold = pass_threshold
        self.type = self.TYPE

    def to_dict(self) -> "Dict[str, Union[str, float]]":
        config: Dict[str, Union[str, float]] = {
            "type": self.type,
            "name": self.name,
            "source": self.source,
        }
        if self.image_tag is not None:
            config["image_tag"] = self.image_tag
        if self.pass_threshold is not None:
            config["pass_threshold"] = self.pass_threshold
        return config

class PairWisePythonGrader:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Placeholder for pair-wise python grader."""
        raise NotImplementedError("PairWisePythonGrader is not implemented yet.")

class PointWiseScoreModelGrader:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Placeholder for score model grader."""
        raise NotImplementedError("PointWiseScoreModelGrader is not implemented yet.")

class PairWiseScoreModelGrader:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Placeholder for pair-wise score model grader."""
        raise NotImplementedError("PairWiseScoreModelGrader is not implemented yet.")