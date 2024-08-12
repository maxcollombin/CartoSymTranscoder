from dataclasses import dataclass

@dataclass
class BetweenOperator:
    ctx: object
    _between: str = None
    _not: str = None
    # between
    @property
    def operator(self):
        if self.ctx.BETWEEN() is not None:
            return self.ctx.BETWEEN().getText()
        return self._between
    @operator.setter
    def operator(self, value: str):
        self._between = value
    # not
    @property
    def not_(self):
        if self.ctx.NOT() is not None:
            return self.ctx.NOT().getText()
        return self._not
    @not_.setter
    def not_(self, value: str):
        self._not = value
