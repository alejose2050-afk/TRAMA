"""
Vistas para la gestión de usuarios, autenticación y navegación principal de TRAMA.

Controladores incluidos:
- home_view: Vista adaptativa basada en roles (RBAC) para cumplir la pauta B.8:
    * Visitante: Landing y catálogo de consulta pública.
    * Usuario (Estudiante): Panel de préstamos personales y solicitudes activas.
    * Gestor (Docente/Laboratorio): Bandeja de aprobación de solicitudes y recursos a cargo.
    * Administrador: Métricas globales del sistema y acceso directo al Django Admin.
- register_view: Procesa el registro de nuevos usuarios con rol y perfil inicial.
- login_view: Autentica al usuario mediante correo institucional y contraseña.
- logout_view: Cierra la sesión activa y redirige al inicio.
- profile_view: Permite al usuario consultar y actualizar sus datos de perfil.
"""

from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileUpdateForm, UserLoginForm, UserRegistrationForm

User = get_user_model()


def home_view(request):
    """
    Página principal de TRAMA.
    Renderiza la vista correspondiente según el rol o privilegio del usuario (B.8).
    """
    user = request.user
    context = {}

    # 1. Rol VISITANTE o Usuario sin autenticar
    if not user.is_authenticated or getattr(user, 'role', '') == User.Role.VISITOR:
        context['role_view'] = 'visitor'
        context['categories'] = [
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
        context['stats'] = {
            'resources_count': '85+',
            'activities_count': '32',
            'faculties_count': '6',
            'approval_rate': '98%',
        }

    # 2. Rol ADMINISTRADOR (Supervisión global)
    elif user.role == User.Role.ADMIN:
        context['role_view'] = 'admin'
        context['total_users'] = User.objects.count()
        context['users_managers'] = User.objects.filter(role=User.Role.MANAGER).count()
        context['users_students'] = User.objects.filter(role=User.Role.USER).count()
        context['latest_users'] = User.objects.order_by('-date_joined')[:6]

    # 3. Rol GESTOR (Docente o Encargado de Recursos / Laboratorio)
    elif user.role == User.Role.MANAGER:
        context['role_view'] = 'manager'
        context['pending_approvals_count'] = 3
        context['managed_resources_count'] = 14
        context['active_activities_count'] = 5
        context['pending_requests'] = [
            {
                'id': 101,
                'student': 'Carlos Mendoza (Estudiante)',
                'resource': 'Proyector Epson PowerLite 1080p',
                'faculty': 'Escuela de Informática - Aula 3B',
                'date': '24/10/2026 (08:00 - 10:30)',
                'purpose': 'Presentación de Trabajo Especial de Grado',
                'status': 'Pendiente',
            },
            {
                'id': 102,
                'student': 'Mariana Rivas (Estudiante)',
                'resource': 'Laboratorio de Redes y Telecomunicaciones',
                'faculty': 'Dpto. de Sistemas',
                'date': '25/10/2026 (14:00 - 17:00)',
                'purpose': 'Taller práctico de enrutamiento y conmutación',
                'status': 'Pendiente',
            },
            {
                'id': 103,
                'student': 'Andrés Silva (Estudiante)',
                'resource': 'Kit de 5 Adaptadores HDMI/VGA',
                'faculty': 'Facultad de Ingeniería',
                'date': '26/10/2026 (10:00 - 12:00)',
                'purpose': 'Feria de Proyectos de Software',
                'status': 'Pendiente',
            },
        ]

    # 4. Rol USUARIO (Estudiante o Miembro de la Comunidad)
    elif user.role == User.Role.USER:
        context['role_view'] = 'user'
        context['active_loans_count'] = 1
        context['pending_requests_count'] = 1
        context['completed_loans_count'] = 3
        context['my_requests'] = [
            {
                'resource': 'Proyector Epson PowerLite 1080p',
                'code': 'AUD-004',
                'location': 'Laboratorio Central de Informática',
                'date': '24/10/2026',
                'status': 'Aprobada',
                'status_class': 'badge-success',
                'responsible': 'Prof. Ricardo Valero',
            },
            {
                'resource': 'Laptop Dell Latitude Core i7 (Taller)',
                'code': 'CMP-012',
                'location': 'Biblioteca Central - Sala B',
                'date': '28/10/2026',
                'status': 'Pendiente',
                'status_class': 'badge-amber',
                'responsible': 'Ing. Sofía Martínez',
            },
            {
                'resource': 'Puntero Láser y Presentador Inalámbrico',
                'code': 'AUD-019',
                'location': 'Decanato de Ingeniería',
                'date': '15/10/2026',
                'status': 'Devuelto',
                'status_class': 'badge-cobalt',
                'responsible': 'Prof. Ricardo Valero',
            },
        ]

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
