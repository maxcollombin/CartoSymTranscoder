from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
from .IdentifierExpression import IdentifierExpression
from .Expression import Expression
from .Visualization import Visualization

@dataclass
class IdentifierExpression:
    name: str

@dataclass
class SystemIdentifierExpression:
    expression: IdentifierExpression
    @property
    def idOrConstant(self) -> Optional[str]:
        if self.expression.idOrConstant in ['dataLayer', 'viz']:
            return self.expression.idOrConstant
        return None

# Classe abstraite Expression
class Expression(ABC):
    @abstractmethod
    def evaluate(self) -> Optional[str]:
        """Méthode abstraite que toutes les sous-classes doivent implémenter."""
        pass

@dataclass
class IdentifierExpression(Expression):
    name: str

    def evaluate(self) -> Optional[str]:
        """Retourne le nom de l'identifiant."""
        return self.name


@dataclass
class SystemIdentifierExpression(Expression):
    expression: IdentifierExpression

    @property
    def idOrConstant(self) -> Optional[str]:
        """Retourne l'identifiant ou une constante si elle est valide."""
        if self.expression.evaluate() in ['dataLayer', 'viz']:
            return self.expression.evaluate()
        return None

    def evaluate(self) -> Optional[str]:
        """Implémentation de la méthode abstraite."""
        return self.idOrConstant