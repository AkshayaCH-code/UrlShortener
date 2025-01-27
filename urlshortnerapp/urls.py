from django.urls import include, path
from rest_framework.routers import DefaultRouter

from urlshortnerapp import views
# from urlshortnerapp.views import ShortenURLViewSet, RedirectURLView, AnalyticsView

# router = DefaultRouter()
# router.register(r'shorten', ShortenURLViewSet, basename='shorten')

# urlpatterns = [
#     path('shorten/',ShortenURLViewSet.as_view(), name='shorten'),
#     path('<str:short_url>/', RedirectURLView.as_view(), name='redirect_url'),
#     path('analytics/<str:short_url>/', AnalyticsView.as_view(), name='analytics'),
# ]
# urlpatterns += router.urls

urlpatterns = [
    path('', views.shorten_url_view, name='shorten_url'),  # Shortening form
    path('shorten/success/', views.shorten_success_view, name='shorten_success_view'),  # Shortened URL display
    path('analytics/<str:short_url>/', views.analytics_view, name='analytics'),  # Analytics view
    path('<str:short_url>/', views.redirect_view, name='redirect_url'),

]

