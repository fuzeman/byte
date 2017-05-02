from byte.statements.where import WhereStatement
from byte.statements.write import WriteStatement


class DeleteStatement(WhereStatement, WriteStatement):
    pass
