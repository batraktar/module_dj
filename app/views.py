from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from app.forms import UserCreateForm, ProductForm, PurchaseForm
from app.models import Product, Purchase


class ProductListView(ListView):
    template_name = 'base.html'
    queryset = Product.objects.all()
    paginate_by = 10


class ProductCreateView(LoginRequiredMixin, CreateView):
    login_url = '/'
    form_class = ProductForm
    template_name = 'create_product.html'
    success_url = '/'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'
    slug_url_kwarg = 'slug'


class ProdUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login/'
    model = Product
    form_class = ProductForm
    template_name = 'update_product.html'
    success_url = '/'


class Registration(CreateView):
    template_name = 'registration.html'
    form_class = UserCreateForm
    success_url = '/'


class Login(LoginView):
    template_name = 'log-in.html'
    next_page = '/'


class PurchaseCreate(LoginRequiredMixin, CreateView):
    template_name = 'amount.html'
    model = Purchase
    form_class = PurchaseForm
    success_url = '/'
    http_method_names = ['post']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {'slug': self.kwargs['slug'], 'request': self.request}
        )
        return kwargs

    def form_invalid(self, form):
        return redirect('/')

    def form_valid(self, form):
        obj = form.save(commit=False)
        product = form.product
        amount = form.cleaned_data['prodquan']
        obj.product = product
        obj.user = self.request.user
        product.quantity -= amount
        obj.User.wallet -= amount * product.price
        with transaction.atomic():
            obj.save()
            product.save()
            obj.user.save()
        messages.success(self.request, 'Purchase completed successfully!')
        return super().form_valid(form=form)


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
