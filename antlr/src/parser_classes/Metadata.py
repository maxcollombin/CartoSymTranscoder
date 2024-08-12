from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Metadata:
    ctx: object
    _name: Optional[str] = None
    _title: Optional[str] = None
    _description: Optional[str] = None
    _authors: List[str] = field(default_factory=list)
    _keywords: List[str] = field(default_factory=list)
    _geoDataClasses: List[str] = field(default_factory=list)
    @property
    def name(self) -> Optional[str]:
        if self.ctx.IDENTIFIER() is not None:
            return self.ctx.IDENTIFIER().getText()
        return self._name
    @name.setter
    def name(self, value: Optional[str]) -> None:
        self._name = value
    @property
    def title(self) -> Optional[str]:
        if self.ctx.STRING() is not None:
            return self.ctx.STRING().getText()
        return self._title
    @title.setter
    def title(self, value: Optional[str]) -> None:
        self._title = value
    @property
    def description(self) -> Optional[str]:
        if self.ctx.STRING() is not None:
            return self.ctx.STRING().getText()
        return self._description
    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._description = value
    @property
    def authors(self) -> List[str]:
        if self.ctx.authors() is not None:
            return self.ctx.authors().getText()
        return self._authors
    @authors.setter
    def authors(self, value: List[str]) -> None:
        self._authors = value
    @property
    def keywords(self) -> List[str]:
        if self.ctx.keywords() is not None:
            return self.ctx.keywords().getText()
        return self._keywords
    @keywords.setter
    def keywords(self, value: List[str]) -> None:
        self._keywords = value
    @property
    def geoDataClasses(self) -> List[str]:
        if self.ctx.geoDataClasses() is not None:
            return self.ctx.geoDataClasses().getText()
        return self._geoDataClasses
    @geoDataClasses.setter
    def geoDataClasses(self, value: List[str]) -> None:
        self._geoDataClasses = value
