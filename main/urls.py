from unicodedata import name
from django.urls import URLPattern
from django.urls import path
from main import views

#app_name = 'main'
urlpatterns = [
    path('home/', views.homepage, name = 'home'),
    path('products/',views.productspage, name = 'products'),
    path('login/',views.loginpage,name = 'login'),
    path('logout/',views.logoutpage,name = 'logout'),
    path('signup/',views.signuppage,name = 'signup'),
    path('account/<pk>/',views.accountpage,name = 'account'),
    path('history-order/',views.OrderHistory,name = 'history-order'),
    path('inventory/',views.InventoryView.as_view(),name = 'inventory'),
    path('seller-order/', views.SellerOrderView.as_view(), name='seller-order'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    # path('product_detail',views.ItemDetailView.as_view(), name='product_detail'),
    path('product/<slug>/', views.ItemDetailView.as_view(), name='product_detail'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    # path('add-coupon/', views.AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', views.remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('product_feedback/<slug>/', views.product_feedback, name='product_feedback'),
    path('edit_feedback/<slug>/', views.edit_feedback, name='edit_feedback'),
    path('get_seller_feedback_url/<pk>/', views.seller_feedback, name='seller_feedback'),
    
    path('edit-inventory/<slug>/', views.edit_inventory, name='edit-inventory'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('detailed-order-page/<slug>/', views.OrderDetailView.as_view(), name = 'detailed-order-page'),
    path('seller-detail-order/<slug>/', views.SellerOrderDetailView.as_view(), name = 'seller-detail-order'),
    path('fulfill/<pk>/', views.fulfill,name='fulfill'),
    path('upvote/<pk>/', views.upvote,name='upvote'),
    
]