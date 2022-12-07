from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, authenticate, logout
from .utils import get_user_from_request
from django.contrib.auth.models import User
from django.views.generic import CreateView


# Create your views here.


class LoginView(CreateView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        return {
            'user': get_user_from_request(self.request),
            'form': kwargs['form'] if kwargs.get('form') else self.form_class
        }

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )

            if user:
                login(request, user)
                return redirect('/products')
            else:
                form.add_error('username', 'bad request')

            return render(request, self.template_name, context=self.get_context_data(form=form))


# def login_view(request):
#     if request.method == 'GET':
#         data = {
#             'form': LoginForm,
#             'user': get_user_from_request(request)
#         }
#
#         return render(request, 'users/login.html', context=data)
#
#     if request.method == 'POST':
#         form = LoginForm(data=request.POST)
#
#         if form.is_valid():
#             user = authenticate(
#                 username=form.cleaned_data.get('username'),
#                 password=form.cleaned_data.get('password')
#             )
#             if user:
#                 login(request, user)
#                 return redirect('/products')
#             else:
#                 form.add_error('username', 'bad request')
#
#         data = {
#             'form': form,
#             'user': get_user_from_request(request)
#         }
#
#         return render(request, 'users/login.html', context=data)


class LogoutView(CreateView):
    def get(self, request, *args):
        logout(request)
        return redirect('/products')


# def logout_view(request):
#     logout(request)
#     return redirect('/products')


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'

    def get_context_data(self, **kwargs):
        return {
            'user': get_user_from_request(self.request),
            'form': kwargs['form'] if kwargs.get('form') else self.form_class
        }

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            if form.cleaned_data.get('password1') == form.cleaned_data.get('password2'):
                user = User.objects.create_user(
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('password1')
                )
                login(request, user)
                return redirect('/products')
            else:
                form.add_error('password1', 'password do not match')

        return render(request, self.template_name, context=self.get_context_data(form=form))


# def register_view(request):
#     if request.method == 'GET':
#         data = {
#             'form': RegisterForm,
#             'user': get_user_from_request(request)
#         }
#
#         return render(request, 'users/register.html', context=data)
#
#     if request.method == 'POST':
#         form = RegisterForm(data=request.POST)
#
#         if form.is_valid():
#             if form.cleaned_data.get('password1') == form.cleaned_data.get('password2'):
#                 user = User.objects.create_user(
#                     username=form.cleaned_data.get('username'),
#                     password=form.cleaned_data.get('password1')
#                 )
#                 login(request, user)
#                 return redirect('/products')
#             else:
#                 form.add_error('password1', 'password do not match')
#
#         data = {
#             'form': form,
#             'user': get_user_from_request(request)
#         }
#
#         return render(request, 'users/register.html', context=data)
