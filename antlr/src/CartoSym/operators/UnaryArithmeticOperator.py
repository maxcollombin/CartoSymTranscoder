from dataclasses import dataclass

@dataclass
class UnaryArithmeticOperator:
    _plus: str = None
    _minus: str = None
    @property
    def plus(self) -> str:
        if self._plus is not None:
            return self._plus
        return self.ctx.PLUS().getText()
    @plus.setter
    def plus(self, value: str) -> None:
        self._plus = value
    @property
    def minus(self) -> str:
        if self._minus is not None:
            return self._minus
        return self.ctx.MINUS().getText()
    @minus.setter
    def minus(self, value: str) -> None:
        self._minus = value
