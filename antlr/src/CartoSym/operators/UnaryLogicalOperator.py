from dataclasses import dataclass

@dataclass
class UnaryLogicalOperator:
    _not: str = None
    @property
    def not_(self) -> str:
        if self._not is not None:
            return self._not
        return self.ctx.NOT().getText()
    @not_.setter
    def not_(self, value: str) -> None:
        self._not = value
