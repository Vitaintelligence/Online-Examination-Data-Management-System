"""Small, explicit DSA implementations used by ExamSphere application routes."""
from __future__ import annotations
from typing import Any, Callable


class Queue:
    """First-in, first-out queue used when processing submitted answers."""
    def __init__(self):
        self._items = []
        self._front = 0

    def enqueue(self, item: Any) -> None:
        self._items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        item = self._items[self._front]
        self._front += 1
        if self._front > 32 and self._front * 2 >= len(self._items):
            self._items = self._items[self._front:]
            self._front = 0
        return item

    def is_empty(self) -> bool:
        return self._front >= len(self._items)

    def __len__(self) -> int:
        return len(self._items) - self._front


def linear_search(records: list[dict], query: str, field: str) -> list[dict]:
    """Return records containing query text (case-insensitive)."""
    needle = query.casefold()
    matches = []
    for record in records:
        if needle in str(record.get(field, "")).casefold():
            matches.append(record)
    return matches


def merge_sort(items: list[dict], key: Callable[[dict], Any], reverse: bool = False) -> list[dict]:
    """Stable merge sort; returns a new list ordered by key."""
    if len(items) <= 1:
        return list(items)
    mid = len(items) // 2
    left = merge_sort(items[:mid], key, reverse)
    right = merge_sort(items[mid:], key, reverse)
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        left_first = key(left[i]) >= key(right[j]) if reverse else key(left[i]) <= key(right[j])
        if left_first:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:]); merged.extend(right[j:])
    return merged
