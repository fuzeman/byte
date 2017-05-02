from byte import Model, Property


class Artist(Model):
    id = Property(int, primary_key=True)

    name = Property(str)
