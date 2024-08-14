from dataclasses import dataclass

@dataclass
class StylingRuleList:
    ctx: object
    _stylingRule: str = None
    _stylingRuleList: str = None
    @property
    def stylingRule(self):
        if self._stylingRule is not None:
            return self._stylingRule
        return self.ctx.stylingRule().getText()
    @stylingRule.setter
    def stylingRule(self, value: str):
        self._stylingRule = value
    @property
    def stylingRuleList(self):
        if self._stylingRuleList is not None:
            return self._stylingRuleList
        return self.ctx.stylingRuleList()
    @stylingRuleList.setter
    def stylingRuleList(self, value: str):
        self._stylingRuleList = value

