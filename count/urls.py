from django.urls import include, path
from rest_framework import routers

from count.views import ListOfPartiesViewSet, MembersViewSet, PurchaseViewSet, CountExpenses

router = routers.DefaultRouter()
router.register(r'party', ListOfPartiesViewSet)
router.register(r'members', MembersViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/count_exp/<int:id>/', CountExpenses.as_view()),
    path("api/purchase/<int:party_id>/", PurchaseViewSet.as_view({
        "get": "retrieve",
        "post": "create",
        "put": "update",
        "patch": "update",
        "delete": "destroy",
    })),
]

