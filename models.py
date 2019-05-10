from smartninja_nosql.odm import Model

class User(Model):
    def __init__(self, name, password, **kwargs):
        self.name = name
        self.password = password
        # self.coordinates = coordinates
        
        super().__init__(**kwargs)
