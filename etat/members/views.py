from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from etat.utils.deletion import deletion_tree

from .models import Member, RoleType
from .forms import MemberForm, AddressFormSet, RoleFormSet, ReachabilityFormSet


def member_list(request):
    roles = RoleType.objects.all()

    return render(request, 'members/list.html', {
        'roles': roles,
    })


def member_view(request, m_id):
    member = get_object_or_404(Member, pk=m_id)
    return render(request, 'members/view.html', {
        'member': member,
    })


def member_add(request):
    if request.method == 'POST':
        member_form = MemberForm(request.POST, request.FILES or {})
        address_formset = AddressFormSet(request.POST)
        roles_formset = RoleFormSet(request.POST)
        reachability_formset = ReachabilityFormSet(request.POST)

        member_form.full_clean()
        if member_form.is_valid():
            member = member_form.save(commit=False)
            address_formset = AddressFormSet(request.POST, instance=member)
            roles_formset = RoleFormSet(request.POST, instance=member)
            reachability_formset = ReachabilityFormSet(request.POST, instance=member)

            formsets_valid = True
            for formset in (address_formset, roles_formset, reachability_formset):
                formset.full_clean()
                if not formset.is_valid():
                    formset.has_errors = True
                    formsets_valid = False

            if formsets_valid:
                member.save()
                address_formset.save()
                roles_formset.save()
                reachability_formset.save()
                return HttpResponse('Saved', status=204)
    else:
        member_form = MemberForm()
        address_formset = AddressFormSet()
        roles_formset = RoleFormSet()
        reachability_formset = ReachabilityFormSet()

    for formset in (address_formset, roles_formset):
        formset.has_errors = any(formset.errors + formset.non_form_errors())

    return render(request, 'members/form.html', {
        'member_form': member_form,
        'address_formset': address_formset,
        'roles_formset': roles_formset,
        'reachability_formset': reachability_formset,
    })


def member_edit(request, m_id):
    member = get_object_or_404(Member, pk=m_id)
    if request.method == 'POST':
        member_form = MemberForm(request.POST, request.FILES or {}, instance=member)
        address_formset = AddressFormSet(request.POST, instance=member)
        roles_formset = RoleFormSet(request.POST, instance=member)
        reachability_formset = ReachabilityFormSet(request.POST, instance=member)

        formsets_valid = True
        for formset in (address_formset, roles_formset, reachability_formset):
            formset.full_clean()
            if not formset.is_valid():
                formset.has_errors = True
                formsets_valid = False

        if member_form.is_valid() and formsets_valid:
            member_form.save()
            address_formset.save()
            roles_formset.save()
            reachability_formset.save()
            return HttpResponse('Saved', status=204)
    else:
        member_form = MemberForm(instance=member)
        address_formset = AddressFormSet(instance=member)
        roles_formset = RoleFormSet(instance=member,)
        reachability_formset = ReachabilityFormSet(instance=member)

    return render(request, 'members/form.html', {
        'member': member,
        'member_form': member_form,
        'address_formset': address_formset,
        'roles_formset': roles_formset,
        'reachability_formset': reachability_formset,
    })


def member_delete(request, m_id):
    member = get_object_or_404(Member, pk=m_id)
    if request.method == 'POST':
        member.delete()
        return HttpResponse('Deleted', status=204)

    return render(request, 'members/delete.html', {
        'member': member,
        'to_delete': deletion_tree(member),
    })