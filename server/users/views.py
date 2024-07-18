import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.contrib.sessions.models import Session


# декоратор для перенаправления ошибки на клиент
def json_login_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Вы не авторизованы'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapped_view


def get_csrf(request):
    response = JsonResponse({'detail': 'CSRF cookie set'})
    response['X-CSRFToken'] = get_token(request)
    return response

@require_POST
def signup_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if username is None or password is None or email is None:
        return JsonResponse({'detail': 'Пожалуйста предоставьте данные'}, status=400)
    
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    if user is None:
        return JsonResponse({'detail': 'Авторизация не удалась'}, status=400)
    
    return JsonResponse({'detail': 'Успешная регистрация'})

@require_POST
def login_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if username is None or password is None:
        return JsonResponse({'detail': 'Пожалуйста предоставьте логин и пароль'}, status=400)

    user = authenticate(username=username, password=password)
    
    if user is None:
        return JsonResponse({'detail': 'Неверные данные'}, status=400)

    login(request, user)
    return JsonResponse({'detail': 'Успешная авторизация'})

  
@json_login_required
def logout_view(request):
    logout(request)
    return JsonResponse({'detail': 'Вы успешно вышли'})

  
@ensure_csrf_cookie
def session_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': False})
    return JsonResponse({
        'isAuthenticated': True
    })

  
@json_login_required
def user_info(request):
    return JsonResponse({
        'isAuthenticated': True,
        'username': request.user.username,
        'user_id': request.user.id
    })
