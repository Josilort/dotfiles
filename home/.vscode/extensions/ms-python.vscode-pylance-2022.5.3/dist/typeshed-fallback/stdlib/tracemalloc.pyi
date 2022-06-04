import sys
from _tracemalloc import *
from collections.abc import Sequence
from typing import Any, Union, overload
from typing_extensions import SupportsIndex, TypeAlias

def get_object_traceback(obj: object) -> Traceback | None: ...
def take_snapshot() -> Snapshot: ...

class BaseFilter:
    inclusive: bool
    def __init__(self, inclusive: bool) -> None: ...

class DomainFilter(BaseFilter):
    @property
    def domain(self) -> int: ...
    def __init__(self, inclusive: bool, domain: int) -> None: ...

class Filter(BaseFilter):
    domain: int | None
    lineno: int | None
    @property
    def filename_pattern(self) -> str: ...
    all_frames: bool
    def __init__(
        self, inclusive: bool, filename_pattern: str, lineno: int | None = ..., all_frames: bool = ..., domain: int | None = ...
    ) -> None: ...

class Statistic:
    count: int
    size: int
    traceback: Traceback
    def __init__(self, traceback: Traceback, size: int, count: int) -> None: ...
    def __eq__(self, other: object) -> bool: ...

class StatisticDiff:
    count: int
    count_diff: int
    size: int
    size_diff: int
    traceback: Traceback
    def __init__(self, traceback: Traceback, size: int, size_diff: int, count: int, count_diff: int) -> None: ...
    def __eq__(self, other: object) -> bool: ...

_FrameTupleT: TypeAlias = tuple[str, int]

class Frame:
    @property
    def filename(self) -> str: ...
    @property
    def lineno(self) -> int: ...
    def __init__(self, frame: _FrameTupleT) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __lt__(self, other: Frame) -> bool: ...
    if sys.version_info >= (3, 11):
        def __gt__(self, other: Frame) -> bool: ...
        def __ge__(self, other: Frame) -> bool: ...
        def __le__(self, other: Frame) -> bool: ...
    else:
        def __gt__(self, other: Frame, NotImplemented: Any = ...) -> bool: ...
        def __ge__(self, other: Frame, NotImplemented: Any = ...) -> bool: ...
        def __le__(self, other: Frame, NotImplemented: Any = ...) -> bool: ...

if sys.version_info >= (3, 9):
    _TraceTupleT: TypeAlias = Union[tuple[int, int, Sequence[_FrameTupleT], int | None], tuple[int, int, Sequence[_FrameTupleT]]]
else:
    _TraceTupleT: TypeAlias = tuple[int, int, Sequence[_FrameTupleT]]

class Trace:
    @property
    def domain(self) -> int: ...
    @property
    def size(self) -> int: ...
    @property
    def traceback(self) -> Traceback: ...
    def __init__(self, trace: _TraceTupleT) -> None: ...
    def __eq__(self, other: object) -> bool: ...

class Traceback(Sequence[Frame]):
    if sys.version_info >= (3, 9):
        @property
        def total_nframe(self) -> int | None: ...
        def __init__(self, frames: Sequence[_FrameTupleT], total_nframe: int | None = ...) -> None: ...
    else:
        def __init__(self, frames: Sequence[_FrameTupleT]) -> None: ...
    if sys.version_info >= (3, 7):
        def format(self, limit: int | None = ..., most_recent_first: bool = ...) -> list[str]: ...
    else:
        def format(self, limit: int | None = ...) -> list[str]: ...

    @overload
    def __getitem__(self, index: SupportsIndex) -> Frame: ...
    @overload
    def __getitem__(self, index: slice) -> Sequence[Frame]: ...
    def __contains__(self, frame: Frame) -> bool: ...  # type: ignore[override]
    def __len__(self) -> int: ...
    def __eq__(self, other: object) -> bool: ...
    def __lt__(self, other: Traceback) -> bool: ...
    if sys.version_info >= (3, 11):
        def __gt__(self, other: Traceback) -> bool: ...
        def __ge__(self, other: Traceback) -> bool: ...
        def __le__(self, other: Traceback) -> bool: ...
    else:
        def __gt__(self, other: Traceback, NotImplemented: Any = ...) -> bool: ...
        def __ge__(self, other: Traceback, NotImplemented: Any = ...) -> bool: ...
        def __le__(self, other: Traceback, NotImplemented: Any = ...) -> bool: ...

class Snapshot:
    def __init__(self, traces: Sequence[_TraceTupleT], traceback_limit: int) -> None: ...
    def compare_to(self, old_snapshot: Snapshot, key_type: str, cumulative: bool = ...) -> list[StatisticDiff]: ...
    def dump(self, filename: str) -> None: ...
    def filter_traces(self, filters: Sequence[DomainFilter | Filter]) -> Snapshot: ...
    @staticmethod
    def load(filename: str) -> Snapshot: ...
    def statistics(self, key_type: str, cumulative: bool = ...) -> list[Statistic]: ...
    traceback_limit: int
    traces: Sequence[Trace]
