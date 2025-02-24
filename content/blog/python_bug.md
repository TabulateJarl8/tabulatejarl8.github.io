---
title: "Python Bug"
date: 2025-02-24T01:03:22-05:00
draft: false
tags: ["python"]
---

I was recently working on my [Vapor](/software/vapor/) project, which is a TUI program written in Python using [Textual](https://github.com/Textualize/textual). I was updating the project's typing to utilize newer features which were introduced in Python 3.10, such as using the bitwise OR operator instead of `Union`. This involved rewriting things like `x: Union[str, int]` as `x: str | int`. In this process, I came across the following piece of code:

```py
yield Container(
    ...,
    DataTable[Union[str, Text]](zebra_stripes=True)
)
```

The `DataTable` in Textual accepts a generic type parameter, which in my case is a string or a `Text` object. This seems like it'd be pretty easy to update, so I rewrote it as this:

```py
yield Container(
    ...,
    DataTable[str | Text](zebra_stripes=True)
)
```

After this, I realized that in order to backport this behavior into Python versions before 3.10, you need to add `from __future__ import annotations` to the top of each file which uses these newer types of typing. From my understanding, this sets an interpreter flag which converts type hints into strings at runtime, allowing static type checkers to still read the types, while the string literals are ignored by the interpreter while the program is running. After adding this and running my unit tests in Python 3.9, I realized that the `DataTable` generic type was raising a `TypeError`. I looked around for a while, eventually coming to the conclusion that this might be a bug in Python itself. I was then able to produce the following minimal reproducible example:

```py
from __future__ import annotations
from typing import Generic, TypeVar

T = TypeVar('T')

class Node(Generic[T]):
    x = None

    def __init__(self, label: T = None) -> None:
        pass

    def __str__(self) -> None:
        return str(self.x)

print(Node[str | int](''))
```

This example will raise a `TypeError` in Python 3.9. I thought about fixing this bug, however with Python 3.9 being EOL in October, they're only accepting security fixes. While talking about this with some others, the only other possible conclusion that we could come to is that this behavior is intentional. Technically, this `Node[str | int]` syntax could be valid in 3.9 if you had a metaclass which defined `__getitem__` and then indexed into a class's attributes with an object that defined `__or__`. Such an example could be something like this:

```py
class Subscriptable(type):
    def __getitem__(self, item):
        return self.__dict__[item]

class Subscript(metaclass=Subscriptable):
    testing = '1'

class BitwiseORString:
    def __init__(self, data):
        self.data = data

    def __or__(self, other):
        if isinstance(other, BitwiseORString):
            return self.data + other.data
        return ''

s1 = BitwiseORString('test')
s2 = BitwiseORString('ing')
print(Subscript[s1 | s2])
```

In my personal opinion (if I were designing the language), this seems like something that would be too inconsistent to leave out, especially since this generic syntax works for singular types in Python 3.9, just not when they're OR'd together. This means that the parser has the ability to differentiate between the two, it just seems that they've forgotten about this edge case. You could maybe make the argument to say that they intentionally left this out to not break code that was using something like this, however if you're using `from __future__ import annotations`, I would guess that you're using this for backwards compatibility with older versions of Python, therefore you'd want your entire codebase to behave the same way instead of having weird discontinuities like this. Thankfully, the fix is pretty simple and you can just quote the types yourself like so:

```py
yield Container(
    ...,
    DataTable["str | Text"](zebra_stripes=True)
)
```

If nothing else, maybe this will help someone who also comes across the same issue, as I couldn't really find much talk about this online. The associated PR can be found [here](https://github.com/TabulateJarl8/vapor/pull/22/).
