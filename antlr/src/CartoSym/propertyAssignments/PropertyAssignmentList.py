from dataclasses import dataclass
from .PropertyAssignment import PropertyAssignment

@dataclass
class PropertyAssignmentList:
    ctx: object
    _propertyAssignment: str = None
    _propertyAssignmentList: str = None
    @property
    def propertyAssignment(self):
        if self._propertyAssignment is not None:
            return self._propertyAssignment
        return PropertyAssignment(self.ctx.propertyAssignment().getText())
    @propertyAssignment.setter
    def propertyAssignment(self, value: str):
        self._propertyAssignment = value
    @property
    def propertyAssignmentList(self):
        if self._propertyAssignmentList is not None:
            return self._propertyAssignmentList
        return PropertyAssignmentList(self.ctx.propertyAssignmentList().getText())
    @propertyAssignmentList.setter
    def propertyAssignmentList(self, value: str):
        self._propertyAssignmentList = value
