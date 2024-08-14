from dataclasses import dataclass
from typing import List, Optional
from .Selector import Selector
from ..propertyAssignments.PropertyAssignmentList import PropertyAssignmentList
from .StylingRuleList import StylingRuleList

@dataclass
class StylingRule:
    ctx: object
    _selector: Optional[str] = None
    _symbolizer: Optional[str] = None
    _nestedRules: Optional[str] = None
    @property
    def selector(self) -> str:
        if self.ctx.selector() is not None:
            return self.ctx.selector()
        return self._selector
    @selector.setter
    def selector(self, value: Optional[str]) -> None:
        self._selector = value
    @property
    def symbolizer(self) -> str:
        if self.ctx.symbolizer() is not None:
            return self.ctx.symbolizer().getText()
        return self._symbolizer
    @symbolizer.setter
    def symbolizer(self, value: Optional[str]) -> None:
        self._symbolizer = value
    @property
    def nestedRules(self) -> str:
        if self.ctx.nestedRules() is not None:
            return self.ctx.nestedRules().getText()
        return self._nestedRules
    @nestedRules.setter
    def nestedRules(self, value: Optional[str]) -> None:
        self._nestedRules = value
    