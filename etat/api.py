from rest_framework import viewsets, routers

from .members.models import Member

class MemberViewSet(viewsets.ModelViewSet):
    model = Member

api = routers.DefaultRouter()
api.register(r'members', MemberViewSet)