# copied and adapted from https://github.com/ideoforms/isobar/blob/master/isobar/pattern/lsystem.py

# Copyright (c) 2011-2020 Daniel John Jones

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from isobar import Pattern
import random


class LSystem:
    def __init__(self, rule="N[-N++N]-N", seed="N", limit=5000):
        self.rule = rule
        self.seed = seed
        self.string = seed
        self.generation = 0
        self.limit = limit

        self.reset()

    def reset(self):
        self.pos = 0
        self.stack = []
        self.state = 0

    def iterate(self, count=1):
        if self.rule.count("[") != self.rule.count("]"):
            raise ValueError("Imbalanced brackets in rule string: %s" % self.rule)

        for n in range(count):
            string_new = ""
            for char in self.string:
                string_new = (
                    string_new + self.rule if char == "N" else string_new + char
                )

            self.string = string_new

    def __next__(self):
        while self.pos < len(self.string) and self.generation <= self.limit:
            token = self.string[self.pos]
            self.pos = self.pos + 1
            self.generation += 1

            if token == "N":
                return self.state
            elif token == "_":
                return None
            elif token == "-":
                self.state -= 1
            elif token == "+":
                self.state += 1
            elif token == "?":
                self.state += random.choice([-1, 1])
            elif token == "[":
                self.stack.append(self.state)
            elif token == "]":
                self.state = self.stack.pop()

        raise StopIteration

    def __iter__(self):
        return self


class PLSystem(Pattern):
    """PLSystem: integer sequence derived from Lindenmayer systems"""

    def __init__(self, rule, depth=4, loop=True):
        self.rule = rule
        self.depth = depth
        self.loop = loop
        self.lsys = None
        self.reset()

    def __str__(self):
        return "lsystem (%s)" % self.rule

    def reset(self):
        self.lsys = LSystem(self.rule, "N")
        self.lsys.iterate(self.depth)

    def __next__(self):
        n = next(self.lsys)
        if self.loop and n is None:
            self.lsys.reset()
            n = next(self.lsys)

        return None if n is None else n
