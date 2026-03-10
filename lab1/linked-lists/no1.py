from typing import Generic, Optional, TypeVar


T = TypeVar("T")


class LinkedList(Generic[T]):
    def __init__(self, value: T, next: Optional["LinkedList[T]"] = None):
        self.value = value
        self.next = next

    def prepend(self, value: T) -> "LinkedList[T]":
        return LinkedList(value, self)

    def append(self, value: T) -> "LinkedList[T]":
        next = self.next

        self.next = LinkedList(value, next)

        return self.next

    def __len__(self) -> int:
        if self.next is None:
            return 1
        
        return 1 + len(self.next)

    def advance(self, count = 1) -> "LinkedList[T]":
        if count == 0:
            return self

        if count < 0:
            return self.advance(len(self) + count)

        if self.next is None:
            raise IndexError

        return self.next.advance(count - 1)
