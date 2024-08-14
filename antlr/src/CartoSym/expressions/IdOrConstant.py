from dataclasses import dataclass
from .ExpConstant import ExpConstant

@dataclass
class IdOrConstant:
    ctx: object
    _identifier: object = None
    _expConstant: object = None
    #identifier
    @property
    def identifier(self) -> str:
        if self.ctx.IDENTIFIER() is not None:
            return self.ctx.IDENTIFIER().getText()
        return self._identifier
    @identifier.setter
    def identifier(self, value: str) -> None:
        self._identifier = value
    #expConstant
    @property
    def expConstant(self) -> object:
        if self.ctx.expConstant() is not None:
            return self.ctx.expConstant().getText()
        return self._expConstant
    @expConstant.setter
    def expConstant(self, value: object) -> None:
        self._expConstant = value
