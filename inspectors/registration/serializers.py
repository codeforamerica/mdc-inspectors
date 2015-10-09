from inspectors.extensions import ma
from .models import (
        User
        )

class UserSchema(ma.ModelSchema):

    class Meta:
        model = User

user_schema = UserSchema()
