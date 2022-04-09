from math import prod
from multiprocessing import context
from urllib import request
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from numpy import product
from main.models import CustomUser, Product, OrderItem, Order, Address, General_Product, ProductFB, Category

from main.forms import CustomUserCreationForm, CheckoutForm, CouponForm, RefundForm, PaymentForm, FeedbackForm,InventoryForm, AddProductForm
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q




User = get_user_model()
# Create your views here.

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

def homepage(request):
    return render(request, template_name='main/home.html')


def productspage(request):
    # items = [
    # {
    #     'name' : 'Phone',
    #     'price' : '500'
    # },
    # {
    #     'name' : 'Laptop',
    #     'price' : '1000'
    # }
    # ]

    query = request.GET.get('search')
    category = request.GET.get('category')
    if query:
        # lookups= Q(product_name__icontains=query)
        # products = General_Product.objects.filter(lookups)
        products = General_Product.objects.filter(product_name__icontains=query)

    
    elif category:
        products = General_Product.objects.filter(category__name=category)
        
        # page_num = request.GET.get("page")
        # paginator = Paginator(products, 2)
        # try:
        #     products = paginator.page(page_num)
        # except PageNotAnInteger:
        #     products = paginator.page(1)
        # except EmptyPage:
        #     products = paginator.page(paginator.num_pages)             
    else:
        products = General_Product.objects.all()
    categories = Category.objects.all()
    
    return render(request, template_name='main/products.html', context={'products':products, 'categories': categories})
    # return render(request, template_name='main/products.html', context={'products':products, 'categories': categories})
    # if request.method == 'POST':
    #     purchased = request.POST.get('purchased')
    #     if purchased:
    #         # if in stock
    #         purchased_object = Product.objects.get(product_name = purchased)
    #         purchased_object.quantity -= 1
    #         purchased_object.save()
    #         messages.success(request, f'Congratulations, you just bought {purchased_object.product_name} for {purchased_object.price}')
    #     add_to_bag = request.POST.get('add_to_bag')

class ItemDetailView(DetailView):
    model = General_Product

    template_name = "main/product_detail.html"
    
    # return render(self.request, 'main/product_detail.html', context)
    def get_context_data(self, *args, **kwargs):
        
        # context = items.filter(general_product = model)
        init_context = super(ItemDetailView,
             self).get_context_data(*args, **kwargs)

        # add extra field 
        context = {'object': init_context['object'], 'sellers': Product.objects.filter(general_product = init_context['object'])}
        return context


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'main/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("products")

class OrderHistoryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.filter(user=self.request.user)
            context = {
                'object': order
            }
            return render(self.request, 'main/order_history.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have any submitted order")
            return redirect("products")

class SellerOrderView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            # items = OrderItem.objects.filter(product__seller=self.request.user,ordered=True).order_by('-ordered_date')
            orders = Order.objects.filter(items__product__seller = self.request.user)

            context = {
                'object': orders,
                # 'items' : items,
            }
            return render(self.request, 'main/seller_order.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not receive any order")
            return redirect("products")

class SellerOrderDetailView(LoginRequiredMixin, DetailView):
    model = Order

    template_name = "main/seller_order_detail.html"



class OrderDetailView(LoginRequiredMixin, DetailView):
    


    model = Order

    # def get_context_data(self, *args, **kwargs):
    #     context = super(OrderDetailView,
    #          self).get_context_data(*args, **kwargs)
    #     # add extra field 
    #     context["category"] = "MISC"        
    #     return context
    #     context = super(OrderDetailView,
    #          self).get_context_data(*args, **kwargs)
    template_name = "main/order_detail.html"
    def post(self, *args, **kwargs):
        data = self.request.POST
        action = data.get('fulfill')
        if action == 'fulfill':




@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        product=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        # if order.items.filter(product__slug=item.slug).exists():
        if order.items.filter(product=item).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(product__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                product=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("product_detail", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product_detail", slug=slug)

@login_required
def product_feedback(request, slug):
    item = get_object_or_404(General_Product, slug=slug)
    if request.method == 'GET':
        return render(request, template_name='main/product_feedback.html', context={'object':item})
        return redirect("product_feedback",slug =slug)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data.get('star')
            review = form.cleaned_data.get('review')
            # fbq = item.feedback.all().get( user = request.user)
            # if fbq:
            #     messages.warning(request, "You have already given a feedback")
            #     return redirect("product_detail", slug=slug)
            # else:

            feedback = ProductFB.objects.create(user = request.user, israted = True, rating = int(rating), review = review)
            # if not feedback.israted:
                # feedback.israted = True
                # feedback.rating = int(rating)
                # feedback.review = review
                # feedback.save()
            item.feedback.add(feedback)
            item.save()
            messages.success(request, "Successfully added review")
            return redirect("product_detail", slug=slug)
            # else:
            #     messages.warning(request, "You have already given a feedback")
            #     return redirect("product_detail", slug=slug)


@login_required
def edit_inventory(request, slug):
    item = get_object_or_404(Product, slug=slug)
    if request.method == 'GET':
        return render(request, template_name='main/edit_inventory.html', context={'item':item})
    if request.method == 'POST':
        form = InventoryForm(request.POST or None)
        if form.is_valid():
            quantiy = form.cleaned_data.get('quantity')
            price = form.cleaned_data.get('price')
            discount_price = form.cleaned_data.get('dprice')
            item.quantity = quantiy
            item.price = price
            item.discount_price = discount_price
            item.save()
            messages.success(request, "Successfully edit inventory")
            return redirect("inventory")


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product", slug=slug)


# def get_coupon(request, code):
#     try:
#         coupon = Coupon.objects.get(code=code)
#         return coupon
#     except ObjectDoesNotExist:
#         messages.info(request, "This coupon does not exist")
#         return redirect("checkout")


# class AddCouponView(View):
#     def post(self, *args, **kwargs):
#         form = CouponForm(self.request.POST or None)
#         if form.is_valid():
#             try:
#                 code = form.cleaned_data.get('code')
#                 order = Order.objects.get(
#                     user=self.request.user, ordered=False)
#                 order.coupon = get_coupon(self.request, code)
#                 order.save()
#                 messages.success(self.request, "Successfully added coupon")
#                 return redirect("checkout")
#             except ObjectDoesNotExist:
#                 messages.info(self.request, "You do not have an active order")
#                 return redirect("checkout")


def loginpage(request):
    if request.method == 'GET':
        return render(request, template_name='main/login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('products')
        else:
            return redirect('login')


def logoutpage(request):
    logout(request)
    return redirect('home')

def signuppage(request):
    if request.method == 'GET':
        return render(request, template_name='main/signup.html')
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = password)
            login(request,user)
            return redirect('home')
        else: 
            return redirect('signup')

def accountpage(request):
    if request.method == 'GET':
        
        if request.user.is_authenticated:
            return render(request, template_name='main/account.html',context={'user':request.user})

        else:
            return render(request, template_name='main/login.html')
    
    if request.method == 'POST':
        pass

class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})
            return render(self.request, "main/checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                for item in order.items.all():
                    item_inventory = Product.objects.get(general_product =item.product.general_product, seller =  item.product.seller)
                    item_inventory.quantity -= item.quantity
                    item_inventory.save()

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_state = form.cleaned_data.get(
                        'shipping_state')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_state, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            state=shipping_state,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_state = form.cleaned_data.get(
                        'billing_state')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_state, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            state=billing_state,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")

                # payment_option = form.cleaned_data.get('payment_option')

                # if payment_option == 'S':
                #     return redirect('payment', payment_option='stripe')
                # elif payment_option == 'P':
                #     return redirect('payment', payment_option='paypal')
                # else:
                #     messages.warning(
                #         self.request, "Invalid payment option selected")
                #     return redirect('checkout')
                self.request.user.balance -= order.get_total()
                self.request.user.save()
                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()
                order.ordered = True
                order.save()

                messages.success(self.request, "Your order was successful!")
                return redirect("/home")
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("order-summary")

class InventoryView(View):
    def get(self, *args, **kwargs):
        try:
            # orders = Order.objects.filter(user = self.request.user)
            # return render(self.request, "main/intentory.html", context = {'orders': orders})
            object = Product.objects.filter(seller = self.request.user)
            general = General_Product.objects.all()
            category = Category.objects.all()
            form = AddProductForm()

            context = {
                'object': object,
                'general_product':general,
                'form':form
    
            }
            return render(self.request, "main/inventory.html", context = context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have any selling product")
            return redirect("products")
    def post(self, *args, **kwargs):

        form = AddProductForm(self.request.POST or None)
        if form.is_valid():
            general = form.cleaned_data.get('general_product')
            # name = form.cleaned_data.get('name')
            quantiy = form.cleaned_data.get('quantity')
            price = form.cleaned_data.get('price')
            discount_price = form.cleaned_data.get('dprice')
            product = Product.objects.filter(seller=self.request.user)
            if product.exists():
                messages.warning(self.request, "You are selling this product now, you can choose to edit the quantity")
                return redirect("inventory")

            item = Product.objects.create(seller = self.request.user, general_product = General_Product.objects.get(product_name = general),quantity = quantiy,price = price, discount_price = discount_price)
            # item.general_product = General_Product.objects.get(product_name = general)
            # # item.name = name
            # item.quantity = quantiy
            # item.price = price
            # item.discount_price = discount_price
            item.save()
            messages.success(self.request, "Successfully edit inventory")
            return redirect("inventory")

        