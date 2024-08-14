from dataclasses import dataclass

@dataclass
class ExpArray:
    ctx: object
    _arrayElements: object = None
    @property
    def arrayElements(self) -> object:
        if self.ctx.arrayElements() is not None:
            return self.ctx.arrayElements()
        return self._arrayElements
    @arrayElements.setter
    def arrayElements(self, value: object) -> None:
        self._arrayElements = value
