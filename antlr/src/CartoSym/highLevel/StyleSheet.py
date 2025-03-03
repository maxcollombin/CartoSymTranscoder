from dataclasses import dataclass
from .Metadata import Metadata
from .StylingRuleList import StylingRuleList

@dataclass
class StyleSheet:
    ctx: object
    _metadata: object = None
    _stylingRuleList: object = None
    @property
    def metadata(self):
        if self._metadata is not None:
            return self._metadata
        return Metadata(self.ctx.metadata())
    @metadata.setter
    def metadata(self, value: object):
        self._metadata = value
    @property
    def stylingRuleList(self):
        if self._stylingRuleList is not None:
            return self._stylingRuleList
        return StylingRuleList(self.ctx.stylingRuleList().getText())
    @stylingRuleList.setter
    def stylingRuleList(self, value: object):
        self._stylingRuleList = value