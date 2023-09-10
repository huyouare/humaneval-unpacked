## Task ID

HumanEval/35

## Entry Point

max_element

## Prompt

```python


def max_element(l: list):
    """Return maximum element in the list.
    >>> max_element([1, 2, 3])
    3
    >>> max_element([5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10])
    123
    """

```

## Canonical Solution

```python
    m = l[0]
    for e in l:
        if e > m:
            m = e
    return m

```

## Test

```python
METADATA = {}


def check(candidate):
    assert candidate([1, 2, 3]) == 3
    assert candidate([5, 3, -5, 2, -3, 3, 9, 0, 124, 1, -10]) == 124

```
