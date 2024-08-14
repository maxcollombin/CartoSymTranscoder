from dataclasses import dataclass

@dataclass
class ArithmeticOperatorExp:
    ctx: object
    _pow: str = None
    @property
    def pow(self) -> str:
        if self.ctx.POW() is not None:
            return self.ctx.POW().getText()
        return self._pow
    @pow.setter
    def pow(self, value: str) -> None:
        self._pow = value
