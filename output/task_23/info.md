## Task ID

HumanEval/23

## Entry Point

strlen

## Prompt

```python


def strlen(string: str) -> int:
    """ Return length of given string
    >>> strlen('')
    0
    >>> strlen('abc')
    3
    """

```

## Canonical Solution

```python
    return len(string)

```

## Test

```python
METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate('') == 0
    assert candidate('x') == 1
    assert candidate('asdasnakj') == 9

```
