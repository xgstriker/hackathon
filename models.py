from smartninja_nosql.odm import Model


class User(Model):
    def __init__(self, name, password, **kwargs):
        self.name = name
        self.password = password


        super().__init__(**kwargs)

    def get_name(self):
        return self.name

    def get_pass(self):
        return self.password

    def get_lat(self):
        return self.lat

    def get_lng(self):
        return self.lng


