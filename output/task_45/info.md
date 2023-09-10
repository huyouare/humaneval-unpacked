## Task ID

HumanEval/45

## Entry Point

triangle_area

## Prompt

```python


def triangle_area(a, h):
    """Given length of a side and high return area for a triangle.
    >>> triangle_area(5, 3)
    7.5
    """

```

## Canonical Solution

```python
    return a * h / 2.0

```

## Test

```python
METADATA = {}


def check(candidate):
    assert candidate(5, 3) == 7.5
    assert candidate(2, 2) == 2.0
    assert candidate(10, 8) == 40.0


```
