from byte.statements.core.base import operation
from byte.statements.where import WhereStatement

from six import string_types


class SelectStatement(WhereStatement):
    def __init__(self, collection, model, properties=None, state=None):
        super(SelectStatement, self).__init__(collection, model, state=state)

        self.properties = properties

    def count(self):
        raise NotImplementedError

    def exists(self):
        raise NotImplementedError

    def first(self):
        raise NotImplementedError

    def group_by(self, *args, **kwargs):
        raise NotImplementedError

    def iterator(self):
        return self.execute().iterator()

    def last(self):
        raise NotImplementedError

    @operation
    def limit(self, count):
        self.state['limit'] = count

    @operation
    def offset(self, count):
        self.state['offset'] = count

    @operation
    def order_by(self, *properties):
        if 'order_by' not in self.state:
            self.state['order_by'] = []

        for prop in properties:
            options = None
            order = None

            # Parse tuple property definition
            if type(prop) is tuple:
                if len(prop) != 2:
                    raise ValueError('Invalid property definition')

                if type(prop[1]) is not dict and not isinstance(prop[1], string_types):
                    raise ValueError('Invalid property definition')

                if isinstance(prop[1], string_types):
                    prop, order = prop
                else:
                    prop, options = prop

            # Resolve `order` value
            if order:
                order = order.lower()

                if order.startswith('asc'):
                    order = 'ascending'
                elif order.startswith('desc'):
                    order = 'descending'

            # Build options dictionary
            if not options:
                options = {
                    'order': order or 'ascending'
                }

            # Resolve property key
            if isinstance(prop, string_types):
                prop = self.model.Internal.properties_by_key[prop]

            # Append property definition to state
            self.state['order_by'].append((prop, options))

    def __iter__(self):
        return self.execute().iterator()

    def __len__(self):
        return len(self.execute())
