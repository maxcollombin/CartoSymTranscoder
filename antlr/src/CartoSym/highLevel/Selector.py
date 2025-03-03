from dataclasses import dataclass
from typing import List, Optional
from ..expressions.Expression import Expression

@dataclass
class Selector(Expression):
    ctx: object
    _identifier: Optional[str] = None
    _expression: Optional[str] = None
    @property
    def identifier(self) -> Optional[str]:
        if self.ctx.IDENTIFIER() is not None:
            return self.ctx.IDENTIFIER().getText()
        return self._identifier
    @identifier.setter
    def identifier(self, value: Optional[str]) -> None:
        self._identifier = value
    @property
    def expression(self) -> Optional[str]:
        if self.ctx.expression() is not None:
            return self.ctx.expression().getText()
        return self._expression
    @expression.setter
    def expression(self, value: Optional[str]) -> None:
        self._expression = value
