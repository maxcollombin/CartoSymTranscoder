from dataclasses import dataclass

@dataclass
class BinaryLogicalOperator:
    ctx: object
    _and: str = None
    _or: str = None
    #and
    @property
    def and_(self) -> str:
        if self.ctx.AND() is not None:
            return self.ctx.AND().getText()
        return self._and
    @and_.setter
    def and_(self, value: str) -> None:
        self._and = value
    #or
    @property
    def or_(self) -> str:
        if self.ctx.OR() is not None:
            return self.ctx.OR().getText()
        return self._or
    @or_.setter
    def or_(self, value: str) -> None:
        self._or = value
