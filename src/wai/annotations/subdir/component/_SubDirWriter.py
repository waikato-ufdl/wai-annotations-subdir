import os

from wai.annotations.core.component.util.output import (
    WritableStoreSink,
    ExpectsDirectory
)
from wai.annotations.core.component.util.output.splitting import (
    SplitSink,
    RequiresNoSplitFinalisation
)
from wai.annotations.core.domain import Data, Instance
from wai.annotations.domain.classification import Classification


class SubDirWriter(
    ExpectsDirectory,
    RequiresNoSplitFinalisation,
    WritableStoreSink[Instance[Data, Classification]],
    SplitSink[Instance[Data, Classification]]
):
    """
    Writes images into a separate sub-directory for each label.
    """
    def consume_element_for_split(
            self,
            element: Instance[Data, Classification]
    ):
        data = element.data
        if data is None:
            return

        path, filename = os.path.split(element.key)

        if element.annotation is None and path != "":
            # TODO: How to handle this case? Last path element will be interpreted as label...
            raise Exception("Encountered unlabelled item with path")

        label = (
            element.annotation.label if element.annotation is not None
            else "."
        )

        split_label = (
            self.split_label if self.is_splitting
            else "."
        )

        self.write(
            data.data,
            os.path.join(split_label, path, label, filename)
        )

    @classmethod
    def get_help_text_for_output_option(cls) -> str:
        return "the directory to store the class directories in"
