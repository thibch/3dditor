class IdSingleton(object):
    id = 0
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(IdSingleton, cls).__new__(cls)
        return cls.instance

    def get_next_id(self):
        self.id += 1
        return self.id