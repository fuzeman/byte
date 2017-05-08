from byte.statements.write import WriteStatement


class InsertStatement(WriteStatement):
    def __init__(self, collection, model, items=None, properties=None, query=None, state=None):
        super(InsertStatement, self).__init__(collection, model, state=state)

        self.items = items
        self.properties = properties
        self.query = query

    def upsert(self):
        raise NotImplementedError
