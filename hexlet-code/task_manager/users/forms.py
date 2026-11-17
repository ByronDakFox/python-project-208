from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.auth.models import User


class UserForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username')
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'username': 'Nombre de usuario',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Contraseña (confirmación)'