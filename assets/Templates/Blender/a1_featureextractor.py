from typing import Callable, Union

from thinc.api import Model
from thinc.types import Ints2d

from ..tokens import Doc


def FeatureExtractor(
    columns: Union[list[str], list[int], list[Union[int, str]]]
) -> Model[list[Doc], list[Ints2d]]:
    return Model("extract_features", forward, attrs={"columns": columns})


def forward(
    model: Model[list[Doc], list[Ints2d]], docs, is_train: bool
) -> tuple[list[Ints2d], Callable]:
    columns = model.attrs["columns"]
    features: list[Ints2d] = []
    for doc in docs:
        if hasattr(doc, "to_array"):
            attrs = doc.to_array(columns)
        else:
            attrs = doc.doc.to_array(columns)[doc.start : doc.end]
        if attrs.ndim == 1:
            attrs = attrs.reshape((attrs.shape[0], 1))
        features.append(model.ops.asarray2i(attrs, dtype="uint64"))

    backprop: Callable[[list[Ints2d]], list] = lambda d_features: []
    return features, backprop