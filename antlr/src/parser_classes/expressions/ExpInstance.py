from dataclasses import dataclass
from ..propertyAssignments.PropertyAssignmentInferredList import PropertyAssignmentInferredList

@dataclass
class ExpInstance:
    ctx: object
    _identifier: object = None
    _propertyAssignmentInferredList: object = None
    #identifier
    @property
    def identifier(self) -> str:
        if self.ctx.IDENTIFIER() is not None:
            return self.ctx.IDENTIFIER().getText()
        return self._identifier
    @identifier.setter
    def identifier(self, value: str) -> None:
        self._identifier = value
    #propertyAssignmentInferredList
    @property
    def propertyAssignmentInferredList(self) -> object:
        if self.ctx.propertyAssignmentInferredList() is not None:
            return self.ctx.propertyAssignmentInferredList().getText()
        return self._propertyAssignmentInferredList
    @propertyAssignmentInferredList.setter
    def propertyAssignmentInferredList(self, value: object) -> None:
        self._propertyAssignmentInferredList = value
