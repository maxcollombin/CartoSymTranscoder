from dataclasses import dataclass

@dataclass
class Tuple:
    _tuple: object = None
    _idOrConstant: object = None
    @property
    def tuple(self) -> object:
        if self._tuple is not None:
            return self._tuple
        return Tuple(self.ctx.tuple())
    @tuple.setter
    def tuple(self, value: object) -> None:
        self._tuple = value
    @property
    def idOrConstant(self) -> object:
        if self._idOrConstant is not None:
            return self._idOrConstant
        from antlr.src.parser_classes.expressions.IdOrConstant import IdOrConstant
        return IdOrConstant(self.ctx.idOrConstant())
    @idOrConstant.setter
    def idOrConstant(self, value: object) -> None:
        self._idOrConstant = value
