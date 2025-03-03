from dataclasses import dataclass
from .PropertyAssignmentInferred import PropertyAssignmentInferred

@dataclass
class PropertyAssignmentInferredList:
    _propertyAssignmentInferred: str = None
    _propertyAssignmentInferredList: str = None
    @property
    def propertyAssignmentInferred(self):
        if self._propertyAssignmentInferred is not None:
            return self._propertyAssignmentInferred
        return PropertyAssignmentInferred(self.ctx.propertyAssignmentInferred().getText())
    @propertyAssignmentInferred.setter
    def propertyAssignmentInferred(self, value: str):
        self._propertyAssignmentInferred = value
    @property
    def propertyAssignmentInferredList(self):
        if self._propertyAssignmentInferredList is not None:
            return self._propertyAssignmentInferredList
        return PropertyAssignmentInferredList(self.ctx.propertyAssignmentInferredList().getText())
    @propertyAssignmentInferredList.setter
    def propertyAssignmentInferredList(self, value: str):
        self._propertyAssignmentInferredList = value
