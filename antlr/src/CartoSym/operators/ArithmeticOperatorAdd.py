from dataclasses import dataclass

@dataclass
class ArithmeticOperatorAdd:
    ctx: object
    _minus: str = None
    _plus: str = None
    #minus
    @property
    def minus(self) -> str:
        if self.ctx.MINUS() is not None:
            return self.ctx.MINUS().getText()
        return self._minus
    @minus.setter
    def minus(self, value: str) -> None:
        self._minus = value
    #plus
    @property
    def plus(self) -> str:
        if self.ctx.PLUS() is not None:
            return self.ctx.PLUS().getText()
        return self._plus
    @plus.setter
    def plus(self, value: str) -> None:
        self._plus = value
