from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import View, FormView, CreateView, DetailView, TemplateView, ListView, UpdateView
from core.forms import SignupForm, ProfileChangeForm, PostForm

# from core.models import People
from core.models import Post


class SignupView(SuccessMessageMixin, CreateView):
    template_name = 'registration/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('login')
    # success_message = "Username created. Now Login"

    """
    here cleaned_data contains all the submitted fields and values
    {'username': 'das11dsas', 'email': 'sadas@ads.com', 'age': 34, 'password1': 'essen123', 'password2': 'essen123'}
    in dictionary format
    """

    def get_success_message(self, cleaned_data):
        return f"{cleaned_data['username']} was successfully created. Now login"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('core:home'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.send_mail()
        return super(SignupView, self).form_valid(form)


class ProfileShowView(TemplateView):
    # model = get_user_model()
    template_name = 'core/profile_show.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id != self.kwargs['id']:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ProfileUpdateView(SuccessMessageMixin, UpdateView):
    model = get_user_model()
    template_name = 'core/profile_update.html'
    form_class = ProfileChangeForm
    success_message = "User updated Successfully!"
    # The name of the URLConf keyword argument that contains the slug. By default, slug_url_kwarg is 'slug'.
    # slug_url_kwarg = 'id'
    # slug_field = 'id'  # The name of the field on the model that contains the slug. By default, slug_field is 'slug'.
    # The name of the URLConf keyword argument that contains the primary key. By default, pk_url_kwarg is 'pk'.
    pk_url_kwarg = 'id'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id != self.kwargs['id']:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class PostListView(ListView):
    model = Post
    template_name = 'core/home.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'core/post_detail.html'

    def dispatch(self, request, *args, **kwargs):
        hits = self.get_object()
        hits.view += 1
        hits.save()
        return super(PostDetailView, self).dispatch(request, *args, **kwargs)


class PostCreateView(CreateView):
    # model = Post
    form_class = PostForm
    template_name = 'core/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        title = form.cleaned_data['title']
        form.instance.slug = slugify(title)
        return super(PostCreateView, self).form_valid(form)