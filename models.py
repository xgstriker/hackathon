from smartninja_nosql.odm import Model

class User(Model):
    def __init__(self, name, email, password, **kwargs):
        self.name = name
        self.email = email
        self.password = password
        
        super().__init__(**kwargs)
