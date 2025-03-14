from flask_marshmallow import Marshmallow
from .models import User


ma = Marshmallow()

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True


class UserCreateUpdateSchema(ma.SQLAlchemyAutoSchema):
    class Meta(UserSchema.Meta):
        fields = ('name', 'email')


class UserListSchema(ma.SQLAlchemyAutoSchema):
    class Meta(UserSchema.Meta):
        fields = ('id', 'name')
