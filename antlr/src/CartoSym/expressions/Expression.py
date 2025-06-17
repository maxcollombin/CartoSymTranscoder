from dataclasses import dataclass
from typing import List, Optional
from .IdOrConstant import IdOrConstant
from .ExpString import ExpString
from .ExpCall import ExpCall
from .ExpArray import ExpArray
from .ExpInstance import ExpInstance
from .ExpConstant import ExpConstant
from .Tuple import Tuple
from ..operators.ArithmeticOperatorExp import ArithmeticOperatorExp
from ..operators.ArithmeticOperatorMul import ArithmeticOperatorMul
from ..operators.ArithmeticOperatorAdd import ArithmeticOperatorAdd
from ..operators.BinaryLogicalOperator import BinaryLogicalOperator
from ..operators.RelationalOperator import RelationalOperator
from ..operators.BetweenOperator import BetweenOperator
from ..operators.UnaryLogicalOperator import UnaryLogicalOperator
from ..operators.UnaryArithmeticOperator import UnaryArithmeticOperator

@dataclass
class Expression:
    ctx: object
    _expression: object = None
    _idOrConstant: object = None
    _identifier: object = None
    _expString: object = None
    _expCall: object = None
    _expArray: object = None
    _expInstance: object = None
    _expConstant: object = None
    _arithmeticOperatorExp: object = None
    _arithmeticOperatorMul: object = None
    _arithmeticOperatorAdd: object = None
    _binaryLogicalOperator: object = None
    _relationalOperator: object = None
    _betweenOperator: object = None
    _unaryLogicalOperator: object = None
    _unaryArithmeticOperator: object = None
    _tuple: object = None

    #expression
    @property
    def expression(self) -> object:
        if self._expression is not None:
            return self._expression
        expr = self.ctx.expression()
        if isinstance(expr, list):
            return [Expression(e.getText()) for e in expr]
        return Expression(expr.getText())
    @expression.setter
    def expression(self, value: object) -> None:
        self._expression = value
    #idOrConstant
    @property
    def idOrConstant(self) -> object:
        if self.ctx.idOrConstant() is not None:
            return self.ctx.idOrConstant().getText()
        return self._idOrConstant
    @idOrConstant.setter
    def idOrConstant(self, value: object) -> None:
        self._idOrConstant = value
    #identifier
    @property
    def identifier(self) -> Optional[str]:
        if self.ctx.IDENTIFIER() is not None:
            return self.ctx.IDENTIFIER().getText()
        return self._identifier
    @identifier.setter
    def identifier(self, value: str) -> None:
        self._identifier = value
    #expString
    @property
    def expString(self) -> object:
        if self.ctx.expString() is not None:
            return self.ctx.expString().getText()
        return self._expString
    @expString.setter
    def expString(self, value: object) -> None:
        self._expString = value
    #expCall
    @property
    def expCall(self) -> object:
        if self.ctx.expCall() is not None:
            return self.ctx.expCall().getText()
        return self._expCall
    @expCall.setter
    def expCall(self, value: object) -> None:
        self._expCall = value
    #expArray
    @property
    def expArray(self) -> object:
        if self.ctx.expArray() is not None:
            return self.ctx.expArray().getText()
        return self._expArray
    @expArray.setter
    def expArray(self, value: object) -> None:
        self._expArray = value
    #expInstance
    @property
    def expInstance(self) -> object:
        if self.ctx.expInstance() is not None:
            return self.ctx.expInstance().getText()
        return self._expInstance
    @expInstance.setter
    def expInstance(self, value: object) -> None:
        self._expInstance = value
    #expConstant
    @property
    def expConstant(self) -> object:
        if self.ctx.expConstant() is not None:
            return self.ctx.expConstant().getText()
        return self._expConstant
    @expConstant.setter
    def expConstant(self, value: object) -> None:
        self._expConstant = value        
    #arithmeticOperatorExp
    @property
    def arithmeticOperatorExp(self) -> object:
        if self.ctx.arithmeticOperatorExp() is not None:
            return self.ctx.arithmeticOperatorExp().getText()
        return self._arithmeticOperatorExp
    @arithmeticOperatorExp.setter
    def arithmeticOperatorExp(self, value: object) -> None:
        self._arithmeticOperatorExp = value
    #arithmeticOperatorMul
    @property
    def arithmeticOperatorMul(self) -> object:
        if self.ctx.arithmeticOperatorMul() is not None:
            return self.ctx.arithmeticOperatorMul().getText()
        return self._arithmeticOperatorMul
    @arithmeticOperatorMul.setter
    def arithmeticOperatorMul(self, value: object) -> None:
        self._arithmeticOperatorMul = value
    #arithmeticOperatorAdd
    @property
    def arithmeticOperatorAdd(self) -> object:
        if self.ctx.arithmeticOperatorAdd() is not None:
            return self.ctx.arithmeticOperatorAdd().getText()
        return self._arithmeticOperatorAdd
    @arithmeticOperatorAdd.setter
    def arithmeticOperatorAdd(self, value: object) -> None:
        self._arithmeticOperatorAdd = value
    #binaryLogicalOperator
    @property
    def binaryLogicalOperator(self) -> object:
        if self.ctx.binaryLogicalOperator() is not None:
            return self.ctx.binaryLogicalOperator().getText()
        return self._binaryLogicalOperator
    @binaryLogicalOperator.setter
    def binaryLogicalOperator(self, value: object) -> None:
        self._binaryLogicalOperator = value    
    #relationalOperator
    @property
    def relationalOperator(self) -> object:
        if self.ctx.relationalOperator() is not None:
            return self.ctx.relationalOperator().getText()
        return self._relationalOperator
    @relationalOperator.setter
    def relationalOperator(self, value: object) -> None:
        self._relationalOperator = value
    #betweenOperator
    @property
    def betweenOperator(self) -> object:
        if self.ctx.betweenOperator() is not None:
            return self.ctx.betweenOperator().getText()
        return self._betweenOperator
    @betweenOperator.setter
    def betweenOperator(self, value: object) -> None:
        self._betweenOperator = value
    #unaryLogicalOperator
    @property
    def unaryLogicalOperator(self) -> object:
        if self.ctx.unaryLogicalOperator() is not None:
            return self.ctx.unaryLogicalOperator().getText()    
        return self._unaryLogicalOperator
    @unaryLogicalOperator.setter
    def unaryLogicalOperator(self, value: object) -> None:
        self._unaryLogicalOperator = value
    #unaryArithmeticOperator
    @property
    def unaryArithmeticOperator(self) -> object:
        if self.ctx.unaryArithmeticOperator() is not None:
            return self.ctx.unaryArithmeticOperator().getText()
        return self._unaryArithmeticOperator
    @unaryArithmeticOperator.setter
    def unaryArithmeticOperator(self, value: object) -> None:
        self._unaryArithmeticOperator = value
    #tuple
    @property
    def tuple(self) -> object:
        if self.ctx.tuple_() is not None:
            return self.ctx.tuple_().getText()
        return self._tuple
    @tuple.setter
    def tuple(self, value: object) -> None:
        self._tuple = value
