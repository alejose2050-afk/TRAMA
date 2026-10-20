"""
Formularios de autenticación y registro de usuarios para TRAMA.

Incluye:
- Registro de nuevos usuarios con perfil inicial y departamento universitario.
- Formulario de inicio de sesión con correo institucional y contraseña.
- Formulario de edición de perfil para mantener los datos de contacto al día.
"""

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from .models import Profile

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    """
    Formulario de registro para nuevos miembros de la comunidad universitaria.
    Crea el usuario con su correo institucional y contraseña, además de capturar
    su nombre, apellido y departamento de adscripción.
    """

    first_name = forms.CharField(
        label='Nombres',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ej. Carlos Eduardo',
            'autocomplete': 'given-name',
        })
    )
    last_name = forms.CharField(
        label='Apellidos',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ej. Gómez Pérez',
            'autocomplete': 'family-name',
        })
    )
    email = forms.EmailField(
        label='Correo institucional o universitario',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'usuario@universidad.edu',
            'autocomplete': 'email',
        })
    )
    department = forms.CharField(
        label='Facultad, Escuela o Departamento',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ej. Ingeniería Informática / Ciencias Básicas',
        })
    )
    role = forms.ChoiceField(
        label='Tipo de vinculación en el campus',
        choices=[
            (User.Role.USER, 'Estudiante / Miembro de la comunidad'),
            (User.Role.MANAGER, 'Docente / Gestor de actividades o laboratorio'),
        ],
        initial=User.Role.USER,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Mínimo 8 caracteres',
            'autocomplete': 'new-password',
        })
    )
    password_confirm = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Repite la contraseña',
            'autocomplete': 'new-password',
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'department', 'role', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError('Ya existe una cuenta registrada con este correo electrónico.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Las contraseñas no coinciden. Verifícalas e intenta de nuevo.')

        return cleaned_data

    def save(self, commit=True):
        """
        Crea el usuario asignándole username automático a partir del email
        y actualiza su perfil con el departamento indicado.
        """
        user = super().save(commit=False)
        email = self.cleaned_data['email']
        user.email = email
        user.username = email.split('@')[0]
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            # El Profile se crea por signal al guardar el User, luego actualizamos los campos adicionales
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.department = self.cleaned_data.get('department', '').strip()
            profile.save()

        return user


class UserLoginForm(AuthenticationForm):
    """
    Formulario de inicio de sesión de TRAMA.
    Valida credenciales contra el correo electrónico y la contraseña.
    """

    username = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'tu-correo@universidad.edu',
            'autocomplete': 'email',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ingresa tu contraseña',
            'autocomplete': 'current-password',
        })
    )


class ProfileUpdateForm(forms.ModelForm):
    """
    Formulario para actualizar datos personales y de contacto en el perfil.
    """

    first_name = forms.CharField(
        label='Nombres',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    last_name = forms.CharField(
        label='Apellidos',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = Profile
        fields = ['phone', 'department', 'bio']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. +58 412 1234567'}),
            'department': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. Escuela de Informática'}),
            'bio': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Breve resumen sobre tu labor académica o proyectos'}),
        }
        labels = {
            'phone': 'Número de teléfono',
            'department': 'Departamento o Escuela',
            'bio': 'Descripción / Biografía',
        }
