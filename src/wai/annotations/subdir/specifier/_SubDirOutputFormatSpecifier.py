from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import Data, Instance
from wai.annotations.core.domain.specifier import DomainSpecifier
from wai.annotations.core.stage.bounds import InstanceTypeBoundUnion
from wai.annotations.core.stage.specifier import SinkStageSpecifier
from wai.annotations.domain.classification import Classification


class SubDirOutputFormatSpecifier(SinkStageSpecifier[DomainSpecifier[Instance[Data, Classification]]]):
    """
    Specifier of the components for writing classification instances where
    each file is stored in a sub-directory named after the class label.
    """
    @classmethod
    def name(cls) -> str:
        return "Sub-dir Writer"

    @classmethod
    def description(cls) -> str:
        return f"Writes files to sub-directories named after their class labels."

    @classmethod
    def bound(cls) -> InstanceTypeBoundUnion:
        return InstanceTypeBoundUnion((Data, Classification))

    @classmethod
    def components(cls, domain: Type[DomainSpecifier[Instance[Data, Classification]]]) -> Tuple[Type[Component], ...]:
        from ..component import SubDirWriter
        return SubDirWriter,
