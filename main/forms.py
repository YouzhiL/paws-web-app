from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser

CHOICES=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')]

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username',)

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_state = forms.CharField(required=False)
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_state = forms.CharField(required=False)
    billing_zip = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

    
class FeedbackForm(forms.Form):
    star = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    review = forms.CharField(required=False)



class SellerFeedbackForm(forms.Form):
    star = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    review = forms.CharField(required=False)


class InventoryForm(forms.Form):
    quantity = forms.IntegerField(required=False)
    price = forms.FloatField(required=False)
    dprice = forms.FloatField(required=False)

class AddProductForm(forms.Form):
    general_product = forms.CharField(required=False)
    # name = forms.CharField(required=False)
    quantity = forms.IntegerField(required=False)
    price = forms.FloatField(required=False)
    dprice = forms.FloatField(required=False)


    
class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)
