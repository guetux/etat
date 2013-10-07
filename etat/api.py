from django.db.models import Q
from django.utils.timezone import now

from rest_framework import viewsets, filters, serializers, routers

from .departments.models import Department, DepartmentType
from .members.models import Member, RoleType, Role


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
        elif status == 'none':
            return queryset.none()

        return queryset.filter(*filter_args).distinct()


class RoleInlineSerializer(serializers.ModelSerializer):
    type = serializers.RelatedField(read_only=True)

    class Meta:
        model = Role
        fields = ('department', 'type')

    def to_native(self, obj):
        data = super(RoleInlineSerializer, self).to_native(obj)
        data['active'] = obj.active
        return data


class MemberSerializer(serializers.ModelSerializer):
    roles = RoleInlineSerializer(many=True)

    class Meta:
        model = Member

class DepartmentViewSet(viewsets.ModelViewSet):
    model = Department


class DepartmentTypeViewSet(viewsets.ModelViewSet):
    model = DepartmentType


class MemberViewSet(viewsets.ModelViewSet):
    model = Member
    filter_backends = (MemberFilter,)
    serializer_class = MemberSerializer


class RoleTypeViewSet(viewsets.ModelViewSet):
    model = RoleType


class RoleViewSet(viewsets.ModelViewSet):
    model = Role


api = routers.DefaultRouter()
api.register(r'departments', DepartmentViewSet)
api.register(r'department_types', DepartmentTypeViewSet)
api.register(r'members', MemberViewSet)
api.register(r'role_types', RoleTypeViewSet)
api.register(r'roles', RoleViewSet)