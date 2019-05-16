from smartninja_nosql.odm import Model


class User(Model):
    def __init__(self, name, password, map_id, **kwargs):
        self.name = name
        self.password = password
        self.map_id = map_id

        super().__init__(**kwargs)


class Loc(Model):
    def __init__(self, lat, lng, location_name, uid, **kwargs):
        self.lat = lat
        self.lng = lng
        self.location_name = location_name
        self.uid = uid

        super().__init__(**kwargs)


class uID(Model):
    def __init__(self, value, **kwargs):
        self.value = value

        super().__init__(**kwargs)


class Users(Model):
    def __init__(self, value, **kwargs):
        self.value = value

        super().__init__(**kwargs)


