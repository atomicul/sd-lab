from collections.abc import Hashable, MutableMapping, Mapping, Iterable, Iterator
import itertools
import functools


class HashTable[K: Hashable, V](MutableMapping[K, V]):
    __MAX_LOAD_FACTOR: float | None
    __table: list[list[tuple[K, V]]]

    def __init__(
        self,
        obj: Iterable[tuple[K, V]] | Mapping[K, V] = [],
        /,
        *,
        size: int = 128,
        max_load_factor: float | None = 0.75,
    ):
        self.__MAX_LOAD_FACTOR = (
            None if max_load_factor is None else float(max_load_factor)
        )

        if isinstance(obj, Mapping):
            obj = iter(obj.items())  # type: ignore

        self.__table = [[] for _ in range(size)]

        for k, v in obj:  # type: ignore
            self[k] = v

    def __getitem__(self, key: K, /) -> V:
        bucket = self.__get_bucket(key)
        try:
            value = next(v for k, v in bucket if k == key)
            return value
        except StopIteration:
            raise KeyError(key)

    def __setitem__(self, key: K, value: V, /) -> None:
        try:
            del self[key]
        except KeyError:
            pass

        bucket = self.__get_bucket(key)
        bucket.append((key, value))

        self.__balance_load()

    def __iter__(self) -> Iterator[K]:
        keys = functools.partial(map, lambda x: x[0])  # type: ignore
        buckets_with_keys = map(keys, self.__table)
        return iter(itertools.chain(*buckets_with_keys))

    def __len__(self) -> int:
        return sum(map(len, self.__table))

    def __delitem__(self, key: K, /) -> None:
        try:
            bucket = self.__get_bucket(key)
            pos = next(idx for idx, (k, _) in enumerate(bucket) if k == key)
            bucket.pop(pos)
        except StopIteration:
            raise KeyError(key)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({list(itertools.chain(*self.__table))!r})"

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

    def __get_bucket(self, key: K, /) -> list[tuple[K, V]]:
        bucket_idx = hash(key) % len(self.__table)
        return self.__table[bucket_idx]
