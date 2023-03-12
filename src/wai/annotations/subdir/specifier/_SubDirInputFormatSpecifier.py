from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import Data, Instance
from wai.annotations.core.domain.specifier import DomainSpecifier
from wai.annotations.core.stage.bounds import InstanceTypeBoundUnion
from wai.annotations.core.stage.specifier import SourceStageSpecifier
from wai.annotations.domain.classification import Classification


class SubDirInputFormatSpecifier(SourceStageSpecifier[DomainSpecifier[Instance[Data, Classification]]]):
    """
    Specifier of the components for reading classification instances where
    each file is stored in a sub-directory named after the class label.
    """
    @classmethod
    def name(cls) -> str:
        return "Sub-dir Reader"

    @classmethod
    def description(cls) -> str:
        return f"Reads files from sub-directories named after their class labels."

    @classmethod
    def bound(cls) -> InstanceTypeBoundUnion:
        return InstanceTypeBoundUnion((Data, Classification))

    @classmethod
    def components(cls, domain: Type[DomainSpecifier[Instance[Data, Classification]]]) -> Tuple[Type[Component], ...]:
        from wai.annotations.core.component.util.input import ReadableStoreSource
        from ..component import reader_class
        return ReadableStoreSource, reader_class(domain.instance_type())
