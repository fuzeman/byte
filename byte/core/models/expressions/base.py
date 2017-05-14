from byte.core.models.nodes import Node
from byte.core.models.property import BaseProperty


class Expressions(object):
    def and_(self, *values):
        raise NotImplementedError

    def __and__(self, rhs):
        raise NotImplementedError

    def __eq__(self, rhs):
        raise NotImplementedError

    def __ne__(self, rhs):
        raise NotImplementedError


class BaseExpression(Node, Expressions):
    def __init__(self, compiler):
        self.compiler = compiler


class Expression(BaseExpression):
    def __init__(self, compiler, lhs, rhs):
        super(Expression, self).__init__(compiler)

        self.lhs = lhs
        self.rhs = rhs

    def resolve_lhs(self, item):
        if isinstance(self.lhs, BaseProperty):
            return self.lhs.get(item)

        return self.lhs

    def resolve_rhs(self, item):
        if isinstance(self.rhs, BaseProperty):
            return self.rhs.get(item)

        return self.rhs

    def execute(self, item):
        raise NotImplementedError('%s.execute() hasn\'t been implemented' % (self.__class__.__name__,))


class ManyExpression(BaseExpression):
    def __init__(self, compiler, *values):
        super(ManyExpression, self).__init__(compiler)

        self.values = values


class StringExpression(Expression):
    def __add__(self, other):
        return self.concat(other)

    def __radd__(self, other):
        return other.concat(self)


class And(ManyExpression):
    pass


class Between(Expression):
    pass


class Equal(Expression):
    def execute(self, item):
        return self.resolve_lhs(item) == self.resolve_rhs(item)


class GreaterThan(Expression):
    pass


class GreaterThanOrEqual(Expression):
    pass


class In(Expression):
    pass


class Is(Expression):
    pass


class IsNot(Expression):
    pass


class LessThan(Expression):
    pass


class LessThanOrEqual(Expression):
    pass


class Like(Expression):
    pass


class NotEqual(Expression):
    pass


class NotIn(Expression):
    pass


class Or(ManyExpression):
    pass


class RegularExpression(Expression):
    pass
