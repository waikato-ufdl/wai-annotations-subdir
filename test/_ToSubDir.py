import itertools
from typing import Callable

from wai.annotations.domain.classification import Classification
from wai.annotations.test import AbstractConversionTest
from wai.annotations.core.store import DictStore
from wai.annotations.core.stream import Pipeline
from wai.annotations.core.util.path import PathKey
from wai.annotations.domain.image.classification import ImageClassificationInstance

from wai.test.decorators import Test

class ToSubDir(AbstractConversionTest):
    @Test
    @AbstractConversionTest.SubjectArgs(
        ["to-subdir-ic", "-s", "dict-store", "-o", "results", "--split-names", "A", "B", "--split-ratios", "1", "1"],
        source=map(
            lambda key, image, label: ImageClassificationInstance.from_parts(key, image, Classification(label)),
            itertools.repeat(PathKey("test/test_image.png"), 100),
            itertools.repeat(AbstractConversionTest.get_test_image()),
            itertools.cycle(("l1", "l2", "l3"))
        )
    )
    def test_to_subdir(self, subject: Callable[[], Pipeline]):
        pipeline = subject()
        store = pipeline.sink.store
        self.assertIsInstance(store, DictStore)
        self.assertIn(store.ensure_key(PathKey("results/A/test/l1/test_image.png")), store)
        self.assertIn(store.ensure_key(PathKey("results/B/test/l1/test_image.png")), store)
        self.assertIn(store.ensure_key(PathKey("results/A/test/l2/test_image.png")), store)
        self.assertIn(store.ensure_key(PathKey("results/B/test/l2/test_image.png")), store)
        self.assertIn(store.ensure_key(PathKey("results/A/test/l3/test_image.png")), store)
        self.assertIn(store.ensure_key(PathKey("results/B/test/l3/test_image.png")), store)
