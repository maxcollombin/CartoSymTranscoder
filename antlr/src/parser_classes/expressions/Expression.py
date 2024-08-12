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
        return Expression(self.ctx.expression())
    @expression.setter
    def expression(self, value: object) -> None:
        self._expression = value
    #idOrConstant
    @property
    def idOrConstant(self) -> object:
        if self._idOrConstant is not None:
            return self._idOrConstant
        return IdOrConstant(self.ctx.idOrConstant())
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
        if self._expString is not None:
            return self._expString
        return ExpString(self.ctx.expString())
    @expString.setter
    def expString(self, value: object) -> None:
        self._expString = value
    #expCall
    @property
    def expCall(self) -> object:
        if self._expCall is not None:
            return self._expCall
        return ExpCall(self.ctx.expCall())
    @expCall.setter
    def expCall(self, value: object) -> None:
        self._expCall = value
    #expArray
    @property
    def expArray(self) -> object:
        if self._expArray is not None:
            return self._expArray
        return ExpArray(self.ctx.expArray())
    @expArray.setter
    def expArray(self, value: object) -> None:
        self._expArray = value
    #expInstance
    @property
    def expInstance(self) -> object:
        if self._expInstance is not None:
            return self._expInstance
        return ExpInstance(self.ctx.expInstance())
    @expInstance.setter
    def expInstance(self, value: object) -> None:
        self._expInstance = value
    #expConstant
    @property
    def expConstant(self) -> object:
        if self._expConstant is not None:
            return self._expConstant
        return ExpConstant(self.ctx.expConstant())
    @expConstant.setter
    def expConstant(self, value: object) -> None:
        self._expConstant = value
    #arithmeticOperatorExp
    @property
    def arithmeticOperatorExp(self) -> object:
        if self._arithmeticOperatorExp is not None:
            return self._arithmeticOperatorExp
        return ArithmeticOperatorExp(self.ctx.arithmeticOperatorExp())
    @arithmeticOperatorExp.setter
    def arithmeticOperatorExp(self, value: object) -> None:
        self._arithmeticOperatorExp = value
    #arithmeticOperatorMul
    @property
    def arithmeticOperatorMul(self) -> object:
        if self._arithmeticOperatorMul is not None:
            return self._arithmeticOperatorMul
        return ArithmeticOperatorMul(self.ctx.arithmeticOperatorMul())
    @arithmeticOperatorMul.setter
    def arithmeticOperatorMul(self, value: object) -> None:
        self._arithmeticOperatorMul = value
    #arithmeticOperatorAdd
    @property
    def arithmeticOperatorAdd(self) -> object:
        if self._arithmeticOperatorAdd is not None:
            return self._arithmeticOperatorAdd
        return ArithmeticOperatorAdd(self.ctx.arithmeticOperatorAdd())
    @arithmeticOperatorAdd.setter
    def arithmeticOperatorAdd(self, value: object) -> None:
        self._arithmeticOperatorAdd = value
    #binaryLogicalOperator
    @property
    def binaryLogicalOperator(self) -> object:
        if self._binaryLogicalOperator is not None:
            return self._binaryLogicalOperator
        return BinaryLogicalOperator(self.ctx.binaryLogicalOperator())
    @binaryLogicalOperator.setter
    def binaryLogicalOperator(self, value: object) -> None:
        self._binaryLogicalOperator = value
    #relationalOperator
    @property
    def relationalOperator(self) -> object:
        if self._relationalOperator is not None:
            return self._relationalOperator
        return RelationalOperator(self.ctx.relationalOperator())
    @relationalOperator.setter
    def relationalOperator(self, value: object) -> None:
        self._relationalOperator = value
    #betweenOperator
    @property
    def betweenOperator(self) -> object:
        if self._betweenOperator is not None:
            return self._betweenOperator
        return BetweenOperator(self.ctx.betweenOperator())
    @betweenOperator.setter
    def betweenOperator(self, value: object) -> None:
        self._betweenOperator = value
    #unaryLogicalOperator
    @property
    def unaryLogicalOperator(self) -> object:
        if self._unaryLogicalOperator is not None:
            return self._unaryLogicalOperator
        return UnaryLogicalOperator(self.ctx.unaryLogicalOperator())
    @unaryLogicalOperator.setter
    def unaryLogicalOperator(self, value: object) -> None:
        self._unaryLogicalOperator = value
    #unaryArithmeticOperator
    @property
    def unaryArithmeticOperator(self) -> object:
        if self._unaryArithmeticOperator is not None:
            return self._unaryArithmeticOperator
        return UnaryArithmeticOperator(self.ctx.unaryArithmeticOperator())
    @unaryArithmeticOperator.setter
    def unaryArithmeticOperator(self, value: object) -> None:
        self._unaryArithmeticOperator = value
    #tuple
    @property
    def tuple(self) -> object:
        if self._tuple is not None:
            return self._tuple
        return Tuple(self.ctx.tuple())
    @tuple.setter
    def tuple(self, value: object) -> None:
        self._tuple = value
