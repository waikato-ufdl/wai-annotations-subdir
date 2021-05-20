import os

from wai.annotations.core.component.util import AnnotationFileProcessor
from wai.annotations.core.stream import ThenFunction
from wai.annotations.domain.classification import Classification
from wai.annotations.domain.image import Image
from wai.annotations.domain.image.classification import ImageClassificationInstance


class SubDirReader(AnnotationFileProcessor[ImageClassificationInstance]):
    """
    Reader of image-classification datasets which store images in
    folders named after the classification label.
    """
    def read_annotation_file(self, filename: str, then: ThenFunction[ImageClassificationInstance]):
        # The label is the last directory folder of the filename
        label = os.path.basename(os.path.dirname(filename))

        then(
            ImageClassificationInstance(
                Image.from_file(filename),
                Classification(label)
            )
        )

    def read_negative_file(self, filename: str, then: ThenFunction[ImageClassificationInstance]):
        then(
            ImageClassificationInstance(
                Image.from_file(filename),
                None
            )
        )
