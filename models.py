from smartninja_nosql.odm import Model


class User(Model):
    def __init__(self, name, password, **kwargs):
        self.name = name
        self.password = password

        super().__init__(**kwargs)


class Loc(Model):
    def __init__(self, lat, lng, locname, **kwargs):
        self.lat = lat
        self.lng = lng
        self.locname = locname

        super().__init__(**kwargs)


class uID(Model):
    def __init__(self, value, **kwargs):
        self.value = value

        super().__init__(**kwargs)


