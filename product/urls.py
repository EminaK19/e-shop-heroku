from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from .views import ProductsList, ProductDetail, CategoriesList
from .views import CategoriesList, ProductViewSet, CommentCreate

router = DefaultRouter()
router.register('', ProductViewSet)


urlpatterns = [
    # path('', ProductsList.as_view()),
    # path('detail/<str:pk>/', ProductDetail.as_view()),
    path('categories/', CategoriesList.as_view()),
    # path('create/', CreateProduct.as_view()),
    # path('update/<str:pk>/', UpdateProduct.as_view()),
    # path('delete/<str:pk>/', DeleteProduct.as_view()),
    # path('', products),
    # path('<str:pk>/', products),
    path('', include(router.urls)),
    path('comments/create/', CommentCreate.as_view()),
]