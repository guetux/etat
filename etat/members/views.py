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


