from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from app.models import User, Product, Purchase


class UserCreateForm(UserCreationForm):
    image = forms.ImageField()

    class Meta:
        model = User
        fields = ('username', 'image', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        def clean_price(self):
            price = self.cleaned_data.get('price')
            if price <= 0:
                raise ValidationError("price should be more than zero")
            return price

        def clean_quantity(self):
            quantity = self.cleaned_data.get('quantity')
            if quantity <= 0:
                raise ValidationError("price should be more than zero")
            return quantity


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['prodquan']

    def __init__(self, *args, **kwargs):
        if 'slug' in kwargs:
            self.slug = kwargs.pop('slug')
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(PurchaseForm, self).__init__(*args, **kwargs)
        self.fields['prodquan'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned = super().clean()
        try:
            product = Product.objects.get(slug=self.slug)
            self.product = product
            if cleaned.get('prodquan') > product.quantity:
                self.add_error(None, 'Error')
                messages.error(self.request, 'Not enough goods')

            if self.request.user.wallet < cleaned.get('prodquan') * product.price:
                self.add_error(None, 'Error')
                messages.error(self.request, 'Not enough money')

        except Product.DoesNotExist:
            self.add_error(None, 'Error')
            messages.error(self.request, 'product is not found')
