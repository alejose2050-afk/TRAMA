"""
Formularios de autenticación y registro de usuarios para TRAMA.
Adaptado a la estructura académica universitaria (Facultades, Escuelas y Departamentos).

Incluye:
- Registro de integrantes de la comunidad universitaria con su adscripción académica.
- Formulario de inicio de sesión con correo universitario y contraseña.
- Formulario de edición de perfil para mantener los datos de contacto al día.
"""

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .models import Profile

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    """
    Formulario de registro para la comunidad universitaria.
    Captura datos de identidad, correo institucional y el departamento
    o área de adscripción académica.
    """

    first_name = forms.CharField(
        label='Nombres',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ej. Alejandro José',
            'autocomplete': 'given-name',
        })
    )
    last_name = forms.CharField(
        label='Apellidos',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ej. Gutiérrez Pérez',
            'autocomplete': 'family-name',
        })
    )
    email = forms.EmailField(
        label='Correo institucional o personal',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'usuario@universidad.edu.ve o tu correo personal',
            'autocomplete': 'email',
        })
    )
    department = forms.CharField(
        label='Facultad / Escuela o Departamento Académico',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ej. Facultad de Ingeniería - Informática',
        })
    )
    role = forms.ChoiceField(
        label='Rol o Condición Universitaria',
        choices=[
            (User.Role.USER, 'Estudiante (Pregrado / Postgrado)'),
            (User.Role.MANAGER, 'Docente / Coordinador / Encargado de Laboratorio'),
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
        user = super().save(commit=False)
        email = self.cleaned_data['email']
        user.email = email
        user.username = email.split('@')[0]
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.department = self.cleaned_data.get('department', '').strip()
            profile.save()

        return user


class UserLoginForm(AuthenticationForm):
    """
    Formulario de inicio de sesión de TRAMA.
    """

    username = forms.EmailField(
        label='Correo electrónico registrado',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'usuario@universidad.edu.ve o tu correo',
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
    Formulario para actualizar datos personales del perfil de usuario.
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
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. 0414-1234567'}),
            'department': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. VPDS - Subprograma Ingeniería en Informática'}),
            'bio': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Breve resumen académico o mención'}),
        }
        labels = {
            'phone': 'Número de teléfono o WhatsApp',
            'department': 'Vicerrectorado / Subprograma',
            'bio': 'Descripción académica',
        }
