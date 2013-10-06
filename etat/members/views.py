from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from ..departments.models import Department

from .models import Member, RoleType
from .forms import MemberForm, AddressFormSet


def member_list(request):
    departments = Department.objects.all()
    roles = RoleType.objects.all()

    return render(request, 'members/list.html', {
        'departments': departments,
        'roles': roles,
    })


def member_view(request, m_id):
    member = get_object_or_404(Member, pk=m_id)
    return render(request, 'members/view.html', {
        'member': member,
    })


def member_edit(request, m_id):
    member = get_object_or_404(Member, pk=m_id)
    if request.method == 'POST':
        if request.FILES:
            form = MemberForm(request.POST, request.FILES, instance=member)
        else:
            form = MemberForm(request.POST, instance=member)

        address_formset = AddressFormSet(request.POST, instance=member)

        if form.is_valid() and address_formset.is_valid():
            form.save()
            address_formset.save()
            return HttpResponse('Saved', status=201)
    else:
        form = MemberForm(instance=member)
        address_formset = AddressFormSet(instance=member)

    return render(request, 'members/form.html', {
        'member': member,
        'form': form,
        'address_formset': address_formset,
    })

