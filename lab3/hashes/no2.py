from collections.abc import MutableSet, MutableSequence, Iterable, Iterator
from array import array
from dataclasses import dataclass


class Empty:
    def __int__(self):
        return 0

    @staticmethod
    def from_int(x: int) -> Empty | None:
        return EMPTY if x == 0 else None


EMPTY = Empty()


class Tombstone:
    def __int__(self):
        return 1

    @staticmethod
    def from_int(x: int) -> Tombstone | None:
        return TOMBSTONE if x == 1 else None


TOMBSTONE = Tombstone()


@dataclass(frozen=True, slots=True)
class Value:
    value: int

    def __int__(self):
        return self.value if self.value < 0 else self.value + 2

    @staticmethod
    def from_int(x: int) -> Value | None:
        if x < 0:
            return Value(x)
        elif x > 1:
            return Value(x - 2)
        else:
            return None


TableEntry = Empty | Tombstone | Value


def map_integers(x: int) -> TableEntry:
    CLASSES = [Empty, Tombstone, Value]
    variants = (c.from_int(x) for c in CLASSES)
    return next(x for x in variants if x is not None)


class HashTable(MutableSet[int]):
    __MAX_LOAD_FACTOR: float | None
    __table: MutableSequence[int]

    def __init__(
        self,
        iterable: Iterable[int] = [],
        /,
        *,
        size: int = 128,
        max_load_factor: float | None = 0.75,
    ):
        self.__MAX_LOAD_FACTOR = (
            None if max_load_factor is None else float(max_load_factor)
        )
        self.__table = array("i", (int(EMPTY) for _ in range(size)))

        for item in iterable:
            self.add(item)

    def __contains__(self, x: object) -> bool:
        if not isinstance(x, int):
            return False

        value = Value(x)

        idx = hash(value)

        while self.__entry(idx) is not EMPTY:
            if value == self.__entry(idx):
                return True

            idx += 1

        return False

    def add(self, value: int) -> None:
        val = Value(value)
        idx = hash(val)

        while self.__entry(idx) is not EMPTY and self.__entry(idx) is not TOMBSTONE:
            if self.__entry(idx) == val:
                return

            idx += 1

        self.__set_entry(idx, val)
        self.__balance_load()

    def __iter__(self) -> Iterator[int]:
        entries = map(map_integers, self.__table)
        return (x.value for x in entries if isinstance(x, Value))

    def discard(self, value: int) -> None:
        val = Value(value)
        idx = hash(val)

        while self.__entry(idx) is not EMPTY:
            if self.__entry(idx) == val:
                self.__set_entry(idx, TOMBSTONE)
                return

            idx += 1

    def __len__(self) -> int:
        entries = map(map_integers, self.__table)
        return sum(1 for x in entries if isinstance(x, Value))

    def __repr__(self) -> str:
        return f"{type(self).__name__}({list(self)!r})"

    def __entry(self, idx: int, /) -> TableEntry:
        idx %= len(self.__table)
        return map_integers(self.__table[idx])

    def __set_entry(self, idx: int, value: TableEntry):
        self.__table[idx % len(self.__table)] = int(value)

    def __balance_load(self) -> bool:
        if self.__MAX_LOAD_FACTOR is None:
            return False

        scale_factor = len(self) / len(self.__table)

        if scale_factor > self.__MAX_LOAD_FACTOR:
            self.__resize(2 * len(self.__table))
            return True

        return False

    def __resize(self, n: int, /) -> None:
        cls = type(self)
        copy = cls(self, size=n, max_load_factor=None)
        self.__table = copy.__table
