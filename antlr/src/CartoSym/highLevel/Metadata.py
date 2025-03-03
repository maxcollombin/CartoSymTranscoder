from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Metadata:
    ctx: object
    _name: Optional[str] = None
    _title: Optional[str] = None
    _description: Optional[str] = None
    _authors: Optional[str] = None
    _keywords: List[Optional[str]] = field(default_factory=list)
    _geoDataClasses: Optional[str] = None
    @property
    def name(self) -> Optional[str]:
        if self.ctx.IDENTIFIER() is not None and self.ctx.IDENTIFIER().getText() == 'name':
            return self.ctx.IDENTIFIER().getText()
        return self._name
    @name.setter
    def name(self, value: Optional[str]) -> None:
        self._name = value
    @property
    def title(self) -> Optional[str]:
        if self.ctx.CHARACTER_LITERAL() is not None and self.ctx.IDENTIFIER().getText() == 'title':
            return self.ctx.CHARACTER_LITERAL().getText()
        return self._title
    @title.setter
    def title(self, value: Optional[str]) -> None:
        self._title = value
    @property
    def description(self) -> Optional[str]:
        if self.ctx.CHARACTER_LITERAL() is not None and self.ctx.IDENTIFIER().getText() == 'description':
            return self.ctx.CHARACTER_LITERAL().getText()
        return self._description
    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._description = value
    @property
    def authors(self) -> Optional[str]:
        if self.ctx.IDENTIFIER() is not None and self.ctx.IDENTIFIER().getText() == 'authors':
            return self.ctx.IDENTIFIER().getText()
        return self._authors
    @authors.setter
    def authors(self, value: Optional[str]) -> None:
        self._authors = value
    @property
    def keywords(self) -> List[Optional[str]]:
        if self.ctx.IDENTIFIER() is not None and self.ctx.IDENTIFIER().getText() == 'keywords':
            characterLiterals = self.ctx.CHARACTER_LITERAL()
            if not isinstance(characterLiterals, list):
                characterLiterals = [characterLiterals]
            return [literal.getText() for literal in characterLiterals]
        return self._keywords
    @keywords.setter
    def keywords(self, value: List[Optional[str]]) -> None:
        self._keywords = value
    @property
    def geoDataClasses(self) -> Optional[str]:
        if self.ctx.IDENTIFIER() is not None and self.ctx.IDENTIFIER().getText() == 'geoDataClasses':
            return self.ctx.IDENTIFIER().getText()
        return self._geoDataClasses
    @geoDataClasses.setter
    def geoDataClasses(self, value: Optional[str]) -> None:
        self._geoDataClasses = value
