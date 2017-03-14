from byte.base import BaseExpression, BaseProperty


def resolve_value(value):
    if isinstance(value, Expression):
        return value.value

    return value


class Expression(BaseExpression):
    def __init__(self, value):
        self.value = resolve_value(value)

    def __eq__(self, other):
        return (
            type(self) is type(other) and
            self.value == other.value
        )

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.value)


class CompoundExpression(BaseExpression):
    def __init__(self, left, right):
        self.left = resolve_value(left)
        self.right = resolve_value(right)

    def matches(self, left, right):
        raise NotImplementedError

    def execute(self, item):
        return self.matches(
            self.__get_value(item, self.left),
            self.__get_value(item, self.right)
        )

    def __get_value(self, item, operand):
        if isinstance(operand, BaseProperty):
            return operand.get(item)

        return operand

    def __eq__(self, other):
        return (
            type(self) is type(other) and
            self.left == other.left and
            self.right == other.right
        )

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.left, self.right)


class MultiExpression(BaseExpression):
    def __init__(self, *values):
        self.values = [resolve_value(value) for value in values]

    def __eq__(self, other):
        return (
            type(self) is type(other) and
            self.values == other.values
        )

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, ', '.join([
            repr(value)
            for value in self.values
        ]))


class IsNull(Expression):
    pass


class In(Expression):
    def __init__(self, prop, items):
        super(In, self).__init__(prop)

        self.items = items

    def __eq__(self, other):
        return (
            type(self) is type(other) and
            self.prop == other.prop and
            self.items == other.items
        )

    def __repr__(self):
        return 'In(%r, %r)' % (self.prop, self.items)


class And(MultiExpression):
    pass


class Or(MultiExpression):
    pass


class Equal(CompoundExpression):
    def matches(self, left, right):
        return left == right


class NotEqual(CompoundExpression):
    pass


class LessThan(CompoundExpression):
    pass


class LessThanOrEqual(CompoundExpression):
    pass


class GreaterThan(CompoundExpression):
    pass


class GreaterThanOrEqual(CompoundExpression):
    pass
