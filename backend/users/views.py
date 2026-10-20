"""
Vistas para la gestión de usuarios, autenticación y navegación principal de TRAMA.

Controladores incluidos:
- home_view: Vista de bienvenida, presentación y catálogo inicial de la plataforma.
- register_view: Procesa el registro de nuevos usuarios con rol y perfil inicial.
- login_view: Autentica al usuario mediante correo institucional y contraseña.
- logout_view: Cierra la sesión activa y redirige al inicio.
- profile_view: Permite al usuario consultar y actualizar sus datos de perfil.
"""

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileUpdateForm, UserLoginForm, UserRegistrationForm


def home_view(request):
    """
    Página principal de TRAMA.
    Muestra la propuesta de valor de la plataforma, categorías de recursos
    y accesos rápidos para la comunidad universitaria.
    """
    # Categorías representativas de recursos del campus universitario
    categories = [
        {
            'title': 'Equipos Audiovisuales',
            'desc': 'Proyectores de alta luminosidad, micrófonos, sistemas de sonido y punteros láser para ponencias.',
            'icon': 'projector',
            'badge': 'Alta demanda',
            'count': 18,
        },
        {
            'title': 'Cómputo y Portátiles',
            'desc': 'Laptops para talleres de programación, tabletas digitalizadoras y adaptadores de red.',
            'icon': 'laptop',
            'badge': 'Préstamo por horas',
            'count': 24,
        },
        {
            'title': 'Laboratorios y Espacios',
            'desc': 'Aulas especializadas, laboratorios de redes, salas de conferencias y auditorios.',
            'icon': 'building',
            'badge': 'Reserva previa',
            'count': 12,
        },
        {
            'title': 'Mobiliario y Eventos',
            'desc': 'Sillas plegables, pizarras móviles, atriles institucionales y mamparas para ferias de proyectos.',
            'icon': 'archive',
            'badge': 'Para actividades',
            'count': 35,
        },
    ]

    context = {
        'categories': categories,
        'stats': {
            'resources_count': '85+',
            'activities_count': '32',
            'faculties_count': '6',
            'approval_rate': '98%',
        }
    }
    return render(request, 'home.html', context)


def register_view(request):
    """
    Controlador para el registro de nuevos integrantes de la universidad.
    Crea la cuenta, asigna el perfil correspondiente e inicia la sesión.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f'¡Bienvenido a TRAMA, {user.first_name}! Tu cuenta universitaria ha sido creada exitosamente.'
            )
            return redirect('home')
        else:
            messages.error(
                request,
                'Hubo un problema al procesar el formulario. Revisa los campos señalados.'
            )
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """
    Controlador para inicio de sesión de usuarios registrados.
    Soporta redirección segura mediante el parámetro 'next'.
    """
    if request.user.is_authenticated:
        return redirect('home')

    next_url = request.GET.get('next', 'home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Sesión iniciada. ¡Hola de nuevo, {user.first_name}!')
            
            # Redirección al destino solicitado o al inicio
            target = request.POST.get('next') or next_url or 'home'
            return redirect(target)
        else:
            messages.error(
                request,
                'Credenciales incorrectas. Verifica tu correo institucional y contraseña.'
            )
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form, 'next': next_url})


def logout_view(request):
    """
    Cierra la sesión del usuario actual y lo redirige a la página principal.
    """
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'Has cerrado tu sesión en TRAMA. ¡Hasta pronto!')
    return redirect('home')


@login_required
def profile_view(request):
    """
    Permite al usuario autenticado consultar y actualizar su información de perfil.
    """
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            # Actualiza nombre y apellido en el modelo User
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            form.save()
            messages.success(request, 'Tus datos de perfil se actualizaron correctamente.')
            return redirect('users:profile')
    else:
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        form = ProfileUpdateForm(instance=profile, initial=initial_data)

    return render(request, 'users/profile.html', {'form': form, 'user_obj': user})
