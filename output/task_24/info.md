## Task ID

HumanEval/24

## Entry Point

largest_divisor

## Prompt

```python


def largest_divisor(n: int) -> int:
    """ For a given number n, find the largest number that divides n evenly, smaller than n
    >>> largest_divisor(15)
    5
    """

```

## Canonical Solution

```python
    for i in reversed(range(n)):
        if n % i == 0:
            return i

```

## Test

```python
METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate(3) == 1
    assert candidate(7) == 1
    assert candidate(10) == 5
    assert candidate(100) == 50
    assert candidate(49) == 7

```
