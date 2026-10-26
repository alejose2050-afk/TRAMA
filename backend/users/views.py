"""
Vistas para la gestión de usuarios, autenticación y navegación principal de TRAMA.
Orientado a la gestión académica universitaria.

Controladores incluidos:
- home_view: Vista adaptativa basada en roles de usuario (RBAC):
    * Visitante: Portada y catálogo de consulta para la comunidad universitaria.
    * Usuario (Estudiante): Panel de solicitudes personales de equipos y espacios para proyectos.
    * Gestor (Docente/Coordinador): Bandeja de aprobación de préstamos y recursos a su cargo.
    * Administrador: Métricas globales del sistema piloto y consola de control.
- register_view: Procesa el registro con rol y adscripción académica.
- login_view: Autentica al usuario mediante correo y contraseña.
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
    Renderiza la vista correspondiente según el rol o privilegio del usuario en el sistema.
    """
    user = request.user
    context = {}

    # 1. Rol VISITANTE o Usuario sin autenticar
    if not user.is_authenticated or getattr(user, 'role', '') == User.Role.VISITOR:
        context['role_view'] = 'visitor'
        context['categories'] = [
            {
                'title': 'Video Beams y Audiovisual',
                'desc': 'Proyectores de video, cornetas amplificadas y punteros láser para defensas de proyecto y clases.',
                'icon': 'projector',
                'badge': 'Uso en aula',
                'count': 4,
            },
            {
                'title': 'Laboratorios de Computación',
                'desc': 'Salas de cómputo y laboratorio de redes en Barinas I para prácticas de programación y sistemas.',
                'icon': 'laptop',
                'badge': 'Práctica por horas',
                'count': 3,
            },
            {
                'title': 'Espacios y Auditorios',
                'desc': 'Auditorio Central de Barinas I y Salón de Usos Múltiples para ponencias y eventos académicos.',
                'icon': 'building',
                'badge': 'Reserva previa',
                'count': 2,
            },
            {
                'title': 'Conectividad y Accesorios',
                'desc': 'Regletas, extensiones eléctricas, cables de red UTP y adaptadores HDMI para talleres.',
                'icon': 'archive',
                'badge': 'Apoyo técnico',
                'count': 5,
            },
        ]
        context['stats'] = {
            'resources_count': '14',
            'activities_count': '3',
            'faculties_count': 'VPDS Barinas',
            'approval_rate': '100%',
        }

    # 2. Rol ADMINISTRADOR (Supervisión global)
    elif user.role == User.Role.ADMIN:
        context['role_view'] = 'admin'
        context['total_users'] = User.objects.count()
        context['users_managers'] = User.objects.filter(role=User.Role.MANAGER).count()
        context['users_students'] = User.objects.filter(role=User.Role.USER).count()
        context['latest_users'] = User.objects.order_by('-date_joined')[:6]

    # 3. Rol GESTOR (Docente o Jefe de Subprograma / Encargado de Laboratorio)
    elif user.role == User.Role.MANAGER:
        context['role_view'] = 'manager'
        context['pending_approvals_count'] = 2
        context['managed_resources_count'] = 6
        context['active_activities_count'] = 2
        context['pending_requests'] = [
            {
                'id': 101,
                'student': 'Carlos Mendoza (Estudiante)',
                'resource': 'Video Beam Epson Aula 4',
                'faculty': 'VPDS Barinas I - Pabellón 1',
                'date': 'Viernes 24/10/2026 (08:30 - 10:00)',
                'purpose': 'Defensa de Proyecto Socio-Tecnológico III',
                'status': 'Pendiente',
            },
            {
                'id': 102,
                'student': 'Mariana Rivas (Estudiante)',
                'resource': 'Laboratorio de Computación 2',
                'faculty': 'VPDS Barinas I - Edificio de Aulas',
                'date': 'Lunes 27/10/2026 (14:00 - 16:30)',
                'purpose': 'Taller práctico del Subproyecto Redes y Conmutación',
                'status': 'Pendiente',
            },
        ]

    # 4. Rol USUARIO (Estudiante de Pregrado / Postgrado)
    elif user.role == User.Role.USER:
        context['role_view'] = 'user'
        context['active_loans_count'] = 1
        context['pending_requests_count'] = 1
        context['completed_loans_count'] = 2
        context['my_requests'] = [
            {
                'resource': 'Video Beam Epson PowerLite',
                'code': 'VB-002',
                'location': 'Barinas I - Pabellón 1',
                'date': '24/10/2026',
                'status': 'Aprobada',
                'status_class': 'badge-success',
                'responsible': 'Prof. Ricardo Valero (Jefe de Subprograma)',
            },
            {
                'resource': 'Regleta de 6 Tomas y Extensión de 10m',
                'code': 'ACC-005',
                'location': 'Laboratorio de Computación 1',
                'date': '28/10/2026',
                'status': 'Pendiente',
                'status_class': 'badge-amber',
                'responsible': 'Ing. Carlos Rivas (Soporte Técnico)',
            },
            {
                'resource': 'Puntero Láser y Presentador Inalámbrico',
                'code': 'VB-008',
                'location': 'Barinas I - Sala de Profesores',
                'date': '15/10/2026',
                'status': 'Devuelto',
                'status_class': 'badge-cobalt',
                'responsible': 'Prof. Ricardo Valero (Jefe de Subprograma)',
            },
        ]

    return render(request, 'home.html', context)


def register_view(request):
    """
    Controlador para el registro de nuevos integrantes universitarios.
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
                'Hubo un problema al procesar el formulario. Revisa los datos ingresados.'
            )
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """
    Controlador para inicio de sesión de usuarios registrados.
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
                'Credenciales incorrectas. Verifica tu correo registrado y contraseña.'
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
