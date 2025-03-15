from flask_marshmallow import Marshmallow
from marshmallow import pre_load, fields

from .models import User


ma = Marshmallow()


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True


class UserListSchema(UserSchema):
    class Meta(UserSchema.Meta):
        fields = ('id', 'name')


class UserCreateUpdateSchema(UserSchema):
    name = fields.String(required=True)
    email = fields.Email(required=True)

    class Meta(UserSchema.Meta):
        fields = ('name', 'email')

    @pre_load
    def preproccess_data(self, data: dict):
        if 'name' in data and isinstance(data['name'], str):
            data['name'] = data['name'].title()
        return data
