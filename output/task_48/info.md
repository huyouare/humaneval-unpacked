## Task ID

HumanEval/48

## Entry Point

is_palindrome

## Prompt

```python


def is_palindrome(text: str):
    """
    Checks if given string is a palindrome
    >>> is_palindrome('')
    True
    >>> is_palindrome('aba')
    True
    >>> is_palindrome('aaaaa')
    True
    >>> is_palindrome('zbcd')
    False
    """

```

## Canonical Solution

```python
    for i in range(len(text)):
        if text[i] != text[len(text) - 1 - i]:
            return False
    return True

```

## Test

```python
METADATA = {}


def check(candidate):
    assert candidate('') == True
    assert candidate('aba') == True
    assert candidate('aaaaa') == True
    assert candidate('zbcd') == False
    assert candidate('xywyx') == True
    assert candidate('xywyz') == False
    assert candidate('xywzx') == False


```
