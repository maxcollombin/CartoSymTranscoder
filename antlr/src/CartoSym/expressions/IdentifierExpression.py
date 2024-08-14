from dataclasses import dataclass
from .Expression import Expression

@dataclass
class IdentifierExpression(Expression):
    _name: str = None
    # @property
    # def name(self) -> str:
    #     """Property to retrieve the identifier."""
    #     if self._name is None and hasattr(self.ctx, 'IDENTIFIER'):
    #         self._name = self.ctx.IDENTIFIER().getText()
    #     return self._name
    # @name.setter
    # def name(self, value: str) -> None:
    #     """Setter pour l'attribut name."""
    #     self._name = value
