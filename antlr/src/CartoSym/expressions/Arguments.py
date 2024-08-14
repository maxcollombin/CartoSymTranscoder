from dataclasses import dataclass
from .Expression import Expression

@dataclass
class Arguments:
    ctx: object
    _arguments: object = None
    _expression: object = None
    @property
    def arguments(self) -> object:
        if self.ctx.arguments() is not None:
            return self.ctx.arguments()
        return self._arguments
    @arguments.setter
    def arguments(self, value: object) -> None:
        self._arguments = value
    @property
    def expression(self) -> object:
        if self._expression is not None:
            return self._expression
        return Expression(self.ctx.expression())
    @expression.setter
    def expression(self, value: object) -> None:
        self._expression = value
