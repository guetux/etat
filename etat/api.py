from django.db.models import Q
from django.utils.timezone import now

from rest_framework import viewsets, filters, routers

from .members.models import Member


class MemberFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        filter_args = []
        departments = request.GET.getlist('departments[]')
        roles = request.GET.getlist('roles[]')
        status = request.GET.get('status')
        gender = request.GET.get('gender')

        if departments:
            filter_args.append(Q(departments__id__in=departments))

        if roles:
            filter_args.append(Q(roles__type__id__in=roles))

        if gender:
            filter_args.append(Q(gender=gender))

        if status == 'active':
            filter_args.append(
                Q(roles__end__isnull=True) |
                Q(roles__end__gte=now())
            )
        elif status == 'inactive':
            filter_args.append(Q(roles__end__lte=now()))

        return queryset.filter(*filter_args)


class MemberViewSet(viewsets.ModelViewSet):
    model = Member
    filter_backends = (MemberFilter,)

api = routers.DefaultRouter()
api.register(r'members', MemberViewSet)