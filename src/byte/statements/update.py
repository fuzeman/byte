from byte.statements.where import WhereStatement
from byte.statements.write import WriteStatement


class UpdateStatement(WhereStatement, WriteStatement):
    def __init__(self, collection, model, data=None, state=None):
        super(UpdateStatement, self).__init__(collection, model, state=state)

        self.data = data
