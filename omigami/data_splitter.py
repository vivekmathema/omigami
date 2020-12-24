from typing import Union, Dict
from omigami.types import Split, RandomState
from omigami.models import InputData
from sklearn.model_selection import GroupShuffleSplit


class DataSplitter:
    def __init__(
        self,
        n_outer: int,
        n_inner: int,
        input_data: InputData,
        random_state: Union[int, RandomState],
    ):
        self.n_outer = n_outer
        self.n_inner = n_inner
        self.random_state = random_state
        self._splits = self._make_splits(input_data)

    def _make_splits(self, input_data: InputData) -> Dict[tuple, Split]:
        """Create a dictionary of split indexes for i`input_data`,
         according to self.n_outer and self.n_inner and `input_data.groups`.
        The groups are split first in `n_outer` test and train segments. Then each
        train segment is split in `n_inner` smaller test and train sub-segments.
        The splits are keyed `(outer_index_split, n_inner_split)`.
        Outer splits are simply keyed `(outer_index_split, None)`.
        """
        outer_splitter = self._make_random_splitter(self.n_outer)
        inner_splitter = self._make_random_splitter(self.n_inner)

        outer_splits = outer_splitter.split(
            input_data.X, input_data.y, input_data.groups
        )

        splits = {}
        for out_idx, (out_train, out_test) in enumerate(outer_splits):
            splits[(out_idx, None)] = out_train, out_test
            X_train = input_data.X[out_train, :]
            y_train = input_data.y[out_train]
            groups_train = input_data.groups[out_train]
            inner_splits = inner_splitter.split(X_train, y_train, groups_train)
            for in_idx, (in_train, in_test) in enumerate(inner_splits):
                splits[(out_idx, in_idx)] = out_train[in_train], out_train[in_test]
        return splits

    def _make_random_splitter(self, n_splits):
        test_size = 1 / n_splits
        return GroupShuffleSplit(
            n_splits, test_size=test_size, random_state=self.random_state
        )

    def get_outer_split(self, outer_index):
        return self._splits[(outer_index, None)]

    def get_inner_split(self, outer_index, inner_index):
        return self._splits[(outer_index, inner_index)]
