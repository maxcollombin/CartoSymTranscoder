from dataclasses import dataclass
from typing import List, Optional
from .Selector import Selector
from ..propertyAssignments.PropertyAssignmentList import PropertyAssignmentList
from .StylingRuleList import StylingRuleList

@dataclass
class StylingRule:
    ctx: object
    # _name: Optional[str] = None
    _selector: Optional[Selector] = None
    _symbolizer: Optional[PropertyAssignmentList] = None
    _nestedRules: Optional[StylingRuleList] = None
    # @property
    # def name(self) -> str:
    #     if self.ctx.CHARACTER_LITERAL() is not None:
    #         return self.ctx.CHARACTER_LITERAL().getText()
    #     return self._name
    # @name.setter
    # def name(self, value: Optional[str]) -> None:
    #     self._name = value
    @property
    def selector(self) -> Selector:
        if self.ctx.selector() is not None:
            return Selector(self.ctx.selector())
        return self._selector
    @selector.setter
    def selector(self, value: Optional[Selector]) -> None:
        self._selector = value
    @property
    def symbolizer(self) -> PropertyAssignmentList:
        if self.ctx.propertyAssignmentList() is not None:
            return PropertyAssignmentList(self.ctx.propertyAssignmentList().getText())
        return self._symbolizer
    @symbolizer.setter
    def symbolizer(self, value: Optional[PropertyAssignmentList]) -> None:
        self._symbolizer = value
    @property
    def nestedRules(self) -> StylingRuleList:
        if self.ctx.stylingRuleList() is not None:
            return StylingRuleList(self.ctx.stylingRuleList().getText())
        return self._nestedRules
    @nestedRules.setter
    def nestedRules(self, value: Optional[StylingRuleList]) -> None:
        self._nestedRules = value
