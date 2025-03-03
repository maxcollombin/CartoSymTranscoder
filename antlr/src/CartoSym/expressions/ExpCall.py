from dataclasses import dataclass

@dataclass
class ExpCall:
    ctx: object
    _identifier: object = None
    _arguments: object = None
    #identifier
    @property
    def identifier(self) -> str:
        if self.ctx.IDENTIFIER() is not None:
            return self.ctx.IDENTIFIER().getText()
        return self._identifier
    @identifier.setter
    def identifier(self, value: str) -> None:
        self._identifier = value
    #arguments
    @property
    def arguments(self) -> object:
        if self.ctx.arguments() is not None:
            return self.ctx.arguments().getText()
        return self._arguments
    @arguments.setter
    def arguments(self, value: object) -> None:
        self._arguments = value
    