from smartninja_nosql.odm import Model


class User(Model):
    def __init__(self, name, password, **kwargs):
        self.name = name
        self.password = password
        # self.coordinates = coordinates

        super().__init__(**kwargs)


class Loc(Model):
    def __init__(self, lat, lng, **kwargs):
        self.lat = lat
        self.lng = lng

        super().__init__(**kwargs)
