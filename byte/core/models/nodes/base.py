class Node(object):
    def compile(self):
        raise NotImplementedError('%s.compile() hasn\'t been implemented' % (self.__class__.__name__,))

    def __str__(self):
        statement, _ = self.compile()
        return statement
