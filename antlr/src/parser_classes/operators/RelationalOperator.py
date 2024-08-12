from dataclasses import dataclass
from typing import List, Optional

@dataclass
class RelationalOperator:
    ctx: object
    _eq: Optional[str] = None
    _lt: Optional[str] = None
    _lteq: Optional[str] = None
    _gt: Optional[str] = None
    _gteq: Optional[str] = None
    _in_: Optional[str] = None
    _not: Optional[str] = None
    _is: Optional[str] = None
    _like: Optional[str] = None
    _not_like: Optional[str] = None
    # eq
    @property
    def eq(self) -> Optional[str]:
        if self.ctx.EQ() is not None:
            return self.ctx.EQ().getText()
        return self._eq
    @eq.setter
    def eq(self, value: Optional[str]) -> None:
        self._eq = value
    # lt
    @property
    def lt(self) -> Optional[str]:
        if self.ctx.LT() is not None:
            return self.ctx.LT().getText()
        return self._lt
    @lt.setter
    def lt(self, value: Optional[str]) -> None:
        self._lt = value
    # lteq
    @property
    def lteq(self) -> Optional[str]:
        if self.ctx.LTEQ() is not None:
            return self.ctx.LTEQ().getText()
        return self._lteq
    @lteq.setter
    def lteq(self, value: Optional[str]) -> None:
        self._lteq = value
    # gt
    @property
    def gt(self) -> Optional[str]:
        if self.ctx.GT() is not None:
            return self.ctx.GT().getText()
        return self._gt
    @gt.setter
    def gt(self, value: Optional[str]) -> None:
        self._gt = value
    # gteq
    @property
    def gteq(self) -> Optional[str]:
        if self.ctx.GTEQ() is not None:
            return self.ctx.GTEQ().getText()
        return self._gteq
    @gteq.setter
    def gteq(self, value: Optional[str]) -> None:
        self._gteq = value
    # in
    @property
    def _in(self) -> Optional[str]:
        if self.ctx.IN() is not None:
            return self.ctx.IN().getText()
        return self._in
    @_in.setter
    def _in(self, value: Optional[str]) -> None:
        self._in_ = value
    # not
    @property
    def not_(self) -> Optional[str]:
        if self.ctx.NOT() is not None:
            return self.ctx.NOT().getText()
        return None
    @not_.setter
    def not_(self, value: Optional[str]) -> None:
        self._not = value
    # is
    @property
    def is_(self) -> Optional[str]:
        if self.ctx.IS() is not None:
            return self.ctx.IS().getText()
        return None
    @is_.setter
    def is_(self, value: Optional[str]) -> None:
        self._is = value
    # like
    @property
    def like(self) -> Optional[str]:
        if self.ctx.LIKE() is not None:
            return self.ctx.LIKE().getText()
        return self._like
    @like.setter
    def like(self, value: Optional[str]) -> None:
        self._like = value
    # not like
    @property
    def not_like(self) -> Optional[str]:
        if self.ctx.NOT() is not None and self.ctx.LIKE() is not None:
            return f"{self.ctx.NOT().getText()} {self.ctx.LIKE().getText()}"
        return self._not_like    
    @not_like.setter
    def not_like(self, value: Optional[str]) -> None:
        self._not_like = value
