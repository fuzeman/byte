class Artist(Model):
    id = Property(int, primary_key=True)

    name = Property(str)
