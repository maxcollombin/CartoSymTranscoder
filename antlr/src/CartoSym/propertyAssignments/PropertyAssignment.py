from dataclasses import dataclass
from typing import Optional
from ..expressions.Expression import Expression

@dataclass
class PropertyAssignment:
    ctx: object
    _lhValue: Optional[str] = None
    _expression: Optional[str] = None

    @property
    def lhValue(self) -> Optional[str]:
        if self.ctx.lhValue() is not None:
            return self.ctx.lhValue().getText()
        return self._lhValue

    @lhValue.setter
    def lhValue(self, value: str) -> None:
        self._lhValue = value

    @property
    def expression(self) -> Optional[str]:
        if self.ctx.expression() is not None:
            return self.ctx.expression().getText()
        return self._expression

    @expression.setter
    def expression(self, value: str) -> None:
        self._expression = value
