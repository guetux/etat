from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from ..departments.models import Department

from .models import Member, RoleType
from .forms import MemberForm, AddressFormSet, RoleFormSet


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


def member_add(request):

    print request.GET.get('department')

    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES or {})
        address_formset = AddressFormSet(request.POST)
        roles_formset = RoleFormSet(request.POST)
        form.full_clean()
        if form.is_valid():
            member = form.save()
            address_formset = AddressFormSet(request.POST, instance=member)
            roles_formset = RoleFormSet(request.POST, instance=member)
            (f.full_clean() for f in (address_formset, roles_formset))
            if address_formset.is_valid() and roles_formset.is_valid():
                address_formset.save()
                roles_formset.save()
                return HttpResponse('Saved', status=201)
    else:
        form = MemberForm()
        address_formset = AddressFormSet()
        roles_formset = RoleFormSet()

    for formset in (address_formset, roles_formset):
        formset.has_errors = any(formset.errors + formset.non_form_errors())

    return render(request, 'members/form.html', {
        'form': form,
        'address_formset': address_formset,
        'roles_formset': roles_formset,
    })


def member_edit(request, m_id):
    member = get_object_or_404(Member, pk=m_id)
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES or {}, instance=member)
        address_formset = AddressFormSet(request.POST, instance=member)
        roles_formset = RoleFormSet(request.POST, instance=member)

        (f.full_clean() for f in (form, address_formset, roles_formset))
        if all(f.is_valid() for f in (form, address_formset, roles_formset)):
            form.save()
            address_formset.save()
            roles_formset.save()
            return HttpResponse('Saved', status=201)
    else:
        form = MemberForm(instance=member)
        address_formset = AddressFormSet(instance=member)
        roles_formset = RoleFormSet(instance=member)

    for formset in (address_formset, roles_formset):
        formset.has_errors = any(formset.errors + formset.non_form_errors())

    return render(request, 'members/form.html', {
        'member': member,
        'form': form,
        'address_formset': address_formset,
        'roles_formset': roles_formset,
    })

