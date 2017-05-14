from byte.core.models.expressions.base import (
    BaseExpression,
    Expressions,
    Expression,
    ManyExpression,
    StringExpression,

    And,
    Between,
    Equal,
    GreaterThan,
    GreaterThanOrEqual,
    In,
    Is,
    IsNot,
    LessThan,
    LessThanOrEqual,
    Like,
    NotEqual,
    NotIn,
    Or,
    RegularExpression
)


class ProxyExpressions(Expressions):
    def and_(self, *values):
        return ProxyAnd(self, *values)

    def __and__(self, rhs):
        return ProxyAnd(self, rhs)

    def __eq__(self, rhs):
        if rhs is None:
            return ProxyIs(self, rhs)

        return ProxyEqual(self, rhs)

    def __ne__(self, rhs):
        if rhs is None:
            return ProxyIsNot(self, rhs)

        return ProxyNotEqual(self, rhs)


class BaseProxyExpression(BaseExpression):
    def transform(self, expressions):
        raise NotImplementedError


class ProxyExpression(Expression, ProxyExpressions, BaseProxyExpression):
    def __init__(self, lhs, rhs):
        super(ProxyExpression, self).__init__(None, lhs, rhs)


class ProxyManyExpression(ManyExpression, ProxyExpressions, BaseProxyExpression):
    def __init__(self, *values):
        super(ProxyManyExpression, self).__init__(None, *values)


class ProxyStringExpression(StringExpression, ProxyExpressions, BaseProxyExpression):
    def __init__(self, lhs, rhs):
        super(ProxyStringExpression, self).__init__(None, lhs, rhs)


class ProxyAnd(And, ProxyManyExpression):
    pass


class ProxyBetween(Between, ProxyExpression):
    pass


class ProxyEqual(Equal, ProxyExpression):
    pass


class ProxyGreaterThan(GreaterThan, ProxyExpression):
    pass


class ProxyGreaterThanOrEqual(GreaterThanOrEqual, ProxyExpression):
    pass


class ProxyIn(In, ProxyExpression):
    pass


class ProxyIs(Is, ProxyExpression):
    pass


class ProxyIsNot(IsNot, ProxyExpression):
    pass


class ProxyLessThan(LessThan, ProxyExpression):
    pass


class ProxyLessThanOrEqual(LessThanOrEqual, ProxyExpression):
    pass


class ProxyLike(Like, ProxyExpression):
    pass


class ProxyNotEqual(NotEqual, ProxyExpression):
    pass


class ProxyNotIn(NotIn, ProxyExpression):
    pass


class ProxyOr(Or, ProxyManyExpression):
    pass


class ProxyRegularExpression(RegularExpression, ProxyExpression):
    pass
