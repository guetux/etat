import json

from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import now

from ..departments.models import Department

from .models import Member, RoleType


def members_list(request):
    departments = Department.objects.all()
    roles = RoleType.objects.all()

    return render(request, 'members/member_list.html', {
        'departments': departments,
        'roles': roles,
    })


def members_data(request):
    departments = request.GET.getlist('department_ids[]')
    filter_args = [
        Q(departments__id__in=departments),
    ]

    roles = request.GET.getlist('roles[]')
    if roles:
        filter_args.append(Q(roles__type__id__in=roles))

    gender = request.GET.get('gender', None)
    if gender:
        filter_args.append(Q(gender=gender))

    inactive = request.GET.get('inactive', False)
    if inactive == 'false':
        filter_args.append(
            Q(roles__end__isnull=True) |
            Q(roles__end__gte=now())
        )

    members = Member.objects.filter(*filter_args)

    member_data = members.distinct().values(
        'id',
        'scout_name',
        'first_name',
        'last_name',
    )

    print member_data
    return HttpResponse(
        json.dumps(list(member_data), cls=DjangoJSONEncoder),
        mimetype="application/json"
    )
