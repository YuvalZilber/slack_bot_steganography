from typing import TypeVar, Generic, Iterable, Sized, Self

T = TypeVar("T")

ListLike = TypeVar("ListLike", Iterable, Sized)


class LimitedBuffer(Generic[T]):
    def __init__(self, limit=15):
        self._limit = limit
        self._buffer = []
        self._pos = 0

    def write(self, *to_write: Iterable[T]) -> None:
        to_write = to_write[-self._limit:]
        to_remove = max(0, len(self._buffer) + len(to_write) - self._limit)
        self._buffer = self._buffer[to_remove:]
        self._buffer.extend(to_write)

    def pop(self, n=None) -> list[T]:
        n = n or len(self._buffer)
        result = self._buffer[:n]
        self._buffer = self._buffer[n:]
        return result

    def read(self) -> list[T]:
        return self._buffer

    def __len__(self):
        return len(self._buffer)

    def is_full(self) -> bool:
        return len(self) == self._limit

    def __iter__(self):
        yield from self.read()

    def equals(self, other: list[T] | tuple[T] | Self):
        if len(self) != len(other):
            return False
        return all(a == b for a, b in zip(self._buffer, other))
