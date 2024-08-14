from dataclasses import dataclass

@dataclass
class ExpString:
    ctx: object
    _characterLiteral: str = None
    @property
    def characterLiteral(self) -> str:
        if self.ctx.CHARACTER_LITERAL() is not None:
            return self.ctx.CHARACTER_LITERAL().getText()
        return self._characterLiteral
    @characterLiteral.setter
    def characterLiteral(self, value: str) -> None:
        self._characterLiteral = value
