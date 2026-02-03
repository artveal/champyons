from sqlalchemy.types import TypeDecorator, SmallInteger

class IntEnumType(TypeDecorator):
    impl = SmallInteger

    def __init__(self, enum_cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enum_cls = enum_cls

    def process_bind_param(self, value, dialect):
        return getattr(value, "value", value)

    def process_result_value(self, value, dialect):
        return self.enum_cls(value)
    
