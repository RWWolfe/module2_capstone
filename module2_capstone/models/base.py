class BaseModel:
    @property
    def id(self):
        raise NotImplementedError("Every Model should have an ID property")
