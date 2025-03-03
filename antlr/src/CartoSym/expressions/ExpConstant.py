from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ExpConstant:
    ctx: object
    _numericLiteral: str = None
    _hexLiteral: str = None
    _unit: Optional[str] = None
    @property
    def numericLiteral(self):
        if self.ctx.NUMERIC_LITERAL() is not None:
            return self.ctx.NUMERIC_LITERAL().getText()
        return None
    @numericLiteral.setter
    def numericLiteral(self, value):
        self._numericLiteral = value
    @property
    def hexLiteral(self):
        if self.ctx.HEX_LITERAL() is not None:
            return self.ctx.HEX_LITERAL().getText()
        return None
    @hexLiteral.setter
    def hexLiteral(self, value):
        self._hexLiteral = value
    @property
    def unit(self) -> Optional[str]:
        if self.ctx.UNIT() is not None:
            return self.ctx.UNIT().getText()
        return None
    @unit.setter
    def unit(self, value):
        self._unit = value
