
// Global members list$

MemberView = {

    memberList: new List('member-list', {
        valueNames: ['first_name', 'last_name', 'scout_name']
    }),

    departmentTree: undefined,
    initDepartmentTree: function() {
        $('#department_tree').jstree({
            plugins: ["themes", "html_data", "ui", "cookies", "checkbox"],
            themes: {
                theme: 'apple',
                dots: false,
                icons: false,
            },
            core: {
                animation: 200,
            }
        }).bind({
            'select_node.jstree': this.loadMembers,
            'deselect_node.jstree': this.loadMembers,
            'check_node.jstree': this.loadMembers,
            'uncheck_node.jstree': this.loadMembers,
            'loaded.jstree': function() {
                console.log('tree is read!');
                var tree = $.jstree._reference('#department_tree');
                tree.hide_checkboxes();
                MemberView.departmentTree = tree;
            }
        });
    },

    initialize: function() {
        this.initDepartmentTree();
        this.bindEvents();
    },

    bindEvents: function() {
        $('#checkselector').on('switch-change', MemberView.toggleDeepSelector);
        $('#roles-filter').change(MemberView.loadMembers);
        $('.status-filter input').change(MemberView.loadMembers);
        $('.gender-filter input').change(MemberView.filterByGender);
        $('#add-member').on('click', MemberView.addMember);

        $('#memberlist').on("click", ".detail", function() {
            var id = $(this).parents('tr').find('td.id').text();
            MemberView.showMember(id);
        });
        $( "#memberlist").on("click", ".edit", function() {
            var id = $(this).parents('tr').find('td.id').text();
            MemberView.editMember(id);
        });
    },

    toggleDeepSelector: function () {
        if ($('#checkselector').bootstrapSwitch('status')) {
            MemberView.departmentTree.show_checkboxes();
        } else {
            MemberView.departmentTree.uncheck_all();
            MemberView.departmentTree.hide_checkboxes();
            MemberView.loadMembers();
        }
    },

    addMember: function() {
        showModal('/members/add/', {width: '900px'});
    },

    showMember: function(id) {
        showModal('/members/' + id + '/', {width: '700px'});
    },

    editMember: function(id) {
        showModal('/members/' + id + '/edit/', {width: '900px'});
    },

    filterByGender: function() {
        var show_m = $('input[name=m]').prop('checked'),
            show_f = $('input[name=f]').prop('checked');
        if (!show_m && !show_f) {
            MemberView.memberList.filter();
        } else {
            MemberView.memberList.filter(function(member) {
                var gender = member.values().gender;
                return gender == 'm' && show_m || gender == 'f' && show_f;
            });
        }
    },

    loadMembers: function() {
        // Reload members for selected departments
        var ids = [],
            data = {};

        // Reinitialize for now
        if (MemberView.departmentTree === undefined) {
            console.log('not ready to load members yet');
            return;
        }

        // Use checked departmens if checkbox is enabled
        _.each(MemberView.departmentTree.get_checked(null, true), function(e) {
            ids.push(parseInt(e.id, 10));
        });

        // Use selection if no checkbox is set
        if (ids.length === 0) {
            _.each(MemberView.departmentTree.get_selected(), function(e) {
                ids.push(parseInt(e.id, 10));
            });
        }

        data['departments'] = ids;

        // Collect filters
        data['roles'] = $('#roles-filter').val();

        var active = $('input[name=active]').prop('checked'),
            inactive = $('input[name=inactive]').prop('checked');
        if (active && !inactive) {
            data['status'] = 'active';
        } else if (inactive && !active) {
            data['status'] = 'inactive';
        } else if (!active && !inactive) {
            data['status'] = 'none';
        }

        $.ajax({
            dataType: 'json',
            type: 'GET',
            url: '/api/members/',
            data: data,
            success: function(data) {
                $('#member-list').find('input[type=search]').val('');
                MemberView.memberList.clear();
                if (data.length) {
                    MemberView.append_roles(data, ids, active, inactive);
                    MemberView.memberList.add(data);
                    MemberView.memberList.search();
                    MemberView.memberList.sort('id', { asc: true });
                }

            }
        });
    },

    append_roles: function(members, deparment_ids, show_active, show_inactive) {
        _.each(members, function(m) {
            roles = [];
            _.each(m.roles, function(r) {
                if (_.indexOf(deparment_ids, r.department) != -1) {
                    if (r.active && show_active || !r.active && show_inactive) {
                        roles.push(r.type);
                    }
                }
            });
            m.roles_display = roles.join(', ');
        });
    }
};

$(function () {
    MemberView.initialize();
});