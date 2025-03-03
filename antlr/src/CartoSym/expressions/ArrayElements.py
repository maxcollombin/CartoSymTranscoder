from dataclasses import dataclass
from .Expression import Expression

@dataclass
class ArrayElements:
    ctx: object
    _arrayElements: object = None
    _expression: object = None
    @property
    def arrayElements(self) -> object:
        if self.ctx.arrayElements() is not None:
            return self.ctx.arrayElements()
        return self._arrayElements
    @arrayElements.setter
    def arrayElements(self, value: object) -> None:
        self._arrayElements = value
    @property
    def expression(self) -> object:
        if self._expression is not None:
            return self._expression
        return Expression(self.ctx.expression())
    @expression.setter
    def expression(self, value: object) -> None:
        self._expression = value
