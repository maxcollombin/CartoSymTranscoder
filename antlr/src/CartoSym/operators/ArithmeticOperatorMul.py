from dataclasses import dataclass

@dataclass
class ArithmeticOperatorMul:
    ctx: object
    _mul: str = None
    _div: str = None
    _mod: str = None
    #mul
    @property
    def mul(self) -> str:
        if self.ctx.MUL() is not None:
            return self.ctx.MUL().getText()
        return self._mul
    @mul.setter
    def mul(self, value: str) -> None:
        self._mul = value
    #div
    @property
    def div(self) -> str:
        if self.ctx.DIV() is not None:
            return self.ctx.DIV().getText()
        return self._div
    @div.setter
    def div(self, value: str) -> None:
        self._div = value
    #mod
    @property
    def mod(self) -> str:
        if self.ctx.MOD() is not None:
            return self.ctx.MOD().getText()
        return self._mod
    @mod.setter
    def mod(self, value: str) -> None:
        self
