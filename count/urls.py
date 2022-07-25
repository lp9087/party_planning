from django.urls import include, path
from rest_framework import routers

from count.views import ListOfPartiesViewSet, MembersAPIView, PurchaseAPIView, CountExpenses, PurchaseExcludeAPIView

router = routers.DefaultRouter()
router.register(r'party', ListOfPartiesViewSet)
#router.register(r'members', MembersViewSet)
#router.register(r'purchase/<int:party_id>', PurchaseViewSet, basename='purchase')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/members/<uuid:party_id>/', MembersAPIView.as_view({
        "post": "create",
        "get": "list"
    })),
    path('api/purchase/<uuid:party_id>/', PurchaseAPIView.as_view({
        "post": "create",
        "get": "list"
    })),
    path('api/count_exp/<uuid:id>/', CountExpenses.as_view()),
    path('api/purchase/exclude/', PurchaseExcludeAPIView.as_view({
        "post": "create",
        "get": "list",
    })),
    #todo action
    path('api/purchase/exclude/<int:id>/', PurchaseExcludeAPIView.as_view({
        "delete": "destroy",
    })),
]

