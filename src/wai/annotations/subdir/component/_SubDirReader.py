import os
from typing import Type, TypeVar

from wai.annotations.core.component.util.input import FileDataProcessor, ReadableStoreItem
from wai.annotations.core.domain import Data, Instance
from wai.annotations.core.store import ReadableStore
from wai.annotations.core.store.key import StoreKey
from wai.annotations.core.stream import ThenFunction
from wai.annotations.core.util.path import PathKey
from wai.annotations.domain.classification import Classification

InstanceType = TypeVar('InstanceType', bound=Instance[Data, Classification])

FileDataProcessorType = FileDataProcessor[
    ReadableStoreItem,  # FIXME: Bug: Python doesn't recognise that this generic parameter
                        #             is already specified in FileDataProcessor.
    InstanceType
]


def reader_class(instance_type: Type[InstanceType]) -> Type[FileDataProcessorType]:
    class SubDirReader(FileDataProcessorType):
        """
        Reader of classification datasets which store files in
        folders named after the classification label.
        """
        def parse_annotation_file(
                self,
                key: StoreKey,
                data: bytes,
                store: ReadableStore,
                common_prefix: str,
                then: ThenFunction[InstanceType]
        ):
            # The label is the last directory folder of the filename
            path, filename = os.path.split(key)
            if path == common_prefix:
                common_prefix = os.path.dirname(common_prefix)
            path, label = os.path.split(path)
            if common_prefix != "":
                path = os.path.relpath(path, common_prefix)

            classification = (
                Classification(label) if label != ""
                else None
            )

            data_type: Type[Data] = instance_type.data_type()

            then(
                instance_type.from_parts(
                    PathKey(os.path.join(path, filename)),
                    data_type.from_data(data),
                    classification
                )
            )

        def parse_negative_file(
                self,
                key: StoreKey,
                data: bytes,
                store: ReadableStore,
                common_prefix: str,
                then: ThenFunction[InstanceType]
        ):
            data_type: Type[Data] = instance_type.data_type()

            then(
                instance_type.from_parts(
                    self.store_key_to_instance_key(key, common_prefix),
                    data_type.from_data(data),
                    None
                )
            )

    return SubDirReader
