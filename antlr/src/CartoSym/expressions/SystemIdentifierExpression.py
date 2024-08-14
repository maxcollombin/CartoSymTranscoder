from dataclasses import dataclass
from typing import List, Optional
from .IdentifierExpression import IdentifierExpression
from .Expression import Expression

@dataclass
class SystemIdentifierExpression:
    expression: IdentifierExpression
    @property
    def idOrConstant(self) -> Optional[str]:
        if self.expression.idOrConstant in ['dataLayer', 'viz']:
            return self.expression.idOrConstant
        return None
