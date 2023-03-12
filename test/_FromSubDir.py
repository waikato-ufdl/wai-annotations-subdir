from typing import Callable

from wai.annotations.core.store import DictStore
from wai.annotations.core.stream import Pipeline

from wai.test.decorators import Test

from wai.annotations.test import AbstractConversionTest


class FromSubDir(AbstractConversionTest):
    @Test
    @AbstractConversionTest.SubjectArgs(
        [
            "from-subdir-ac", "-i", "label/test_audio", "-s", "dict-store", "-S=-m", f"-S=label/test_audio>{AbstractConversionTest.TEST_DICT_STORE_AUDIO}",
            "to-data", "-s", "dict-store", "-o", "results"
        ]
    )
    def test_from_subdir(self, subject: Callable[[], Pipeline]):
        pipeline = subject()
        store = pipeline.sink.store
        self.assertIsInstance(store, DictStore)
        self.assertIn(
            store.ensure_key("results/test_audio"),
            store
        )
