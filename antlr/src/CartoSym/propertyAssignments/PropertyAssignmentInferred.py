from dataclasses import dataclass

@dataclass
class PropertyAssignmentInferred:
    ctx: object
    _propertyAssignment: str = None
    _expression: str = None

    @property
    def propertyAssignment(self):
        if self._propertyAssignment is not None:
            return self._propertyAssignment
        return self.ctx.propertyAssignment().getText()

    @propertyAssignment.setter
    def propertyAssignment(self, value: str):
        self._propertyAssignment = value

    @property
    def expression(self):
        if self._expression is not None:
            return self._expression
        return self.ctx.expression()

    @expression.setter
    def expression(self, value: str):
        self._expression = value
