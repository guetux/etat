
// Global members list$

// list.js table of all members
var MemberList = new List('member-list', {
            valueNames: ['first_name', 'last_name', 'scout_name']
});

// department tree compontent. This mainly eliminates the uglyness of jstree
var Departments = {
    tree : undefined, // reference to js tree

    // Get a list of all selected departments
    get_selected: function() {
        ids = [];
        _.each(Departments.tree.get_checked(null, true), function(e) {
            ids.push(parseInt(e.id, 10));
        });

        // Use selection if no checkbox is set
        if (ids.length === 0) {
            _.each(Departments.tree.get_selected(), function(e) {
                ids.push(parseInt(e.id, 10));
            });
        }
        return ids;
    },

    // Enable or disable the checkbox selector
    toggleDeepSelector: function () {
        if ($('#checkselector').bootstrapSwitch('status')) {
            Departments.tree.show_checkboxes();
        } else {
            Departments.tree.uncheck_all();
            Departments.tree.hide_checkboxes();
            $('#department_tree').trigger('selection_changed');
        }
    },

    initialize: function() {
        function selection_changed() {
            $('#department_tree').trigger('selection_changed');
        }

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
            'select_node.jstree': selection_changed,
            'deselect_node.jstree': selection_changed,
            'check_node.jstree': selection_changed,
            'uncheck_node.jstree': selection_changed,
            'loaded.jstree': function() {
                // keep reference
                Departments.tree = $.jstree._reference('#department_tree');
                Departments.tree.hide_checkboxes();
            }
        });

        $("#checkselector").on('switch-change', Departments.toggleDeepSelector);
    },

};
_.extend(Departments, Backbone.Events);


Etat.Views.MemberView = Backbone.View.extend({

    events: {
        'selection_changed #department_tree' : "loadMembers",
        "change #roles-filter"               : "loadMembers",
        "change .status-filter input"        : "loadMembers",
        "change .gender-filter"              : "filterByGender",
        "click .member-add"                  : "addMember",
        "click .member-detail"               : "showMember",
        "click .member-edit"                 : "editMember",
    },

    memberIdForEvent: function() {
        return $(event.target).parents('tr').find('td.id').text();
    },

    // Launch modal to create a new member
    addMember: function() {
        showModal('/members/add/', {width: '900px'});
    },

    // Display short stats of one member
    showMember: function(event) {
        var id = this.memberIdForEvent(event);
        showModal('/members/' + id + '/', {width: '700px'});
    },

    // Start editing a member
    editMember: function(event) {
        var id = this.memberIdForEvent(event);
        showModal('/members/' + id + '/edit/', {width: '900px'});
    },

    // File male or females in member list
    filterByGender: function() {
        var show_m = $('input[name=m]').prop('checked'),
            show_f = $('input[name=f]').prop('checked');
        if (!show_m && !show_f) {
            MemberList.filter();
        } else {
            MemberList.filter(function(member) {
                var gender = member.values().gender;
                return gender == 'm' && show_m || gender == 'f' && show_f;
            });
        }
    },

    // Get all active filters to reload member list
    collectFilters: function() {
        var filterArgs = {};
        filterArgs['departments'] = Departments.get_selected();

        filterArgs['roles'] = $('#roles-filter').val();

        var active = $('input[name=active]').prop('checked'),
            inactive = $('input[name=inactive]').prop('checked');
        if (active && !inactive) {
            filterArgs['status'] = 'active';
        } else if (inactive && !active) {
            filterArgs['status'] = 'inactive';
        } else if (!active && !inactive) {
            filterArgs['status'] = 'none';
        }

        return filterArgs;
    },

    // Reload member data form server an display them in member table
    loadMembers: function() {
        $.ajax({
            dataType: 'json',
            type: 'GET',
            url: '/api/members/',
            data: this.collectFilters(),
            success: function(members) {
                $('#member-list').find('input[type=search]').val('');
                MemberList.clear();
                if (members.length) {
                    append_roles(members);
                    MemberList.add(members);
                    MemberList.search();
                    MemberList.sort('id', { asc: true });
                }
            }
        });
    },
});



// Attaches a list of all roles to every member
function append_roles(members) {
    var selected_departments = Departments.get_selected();
        show_active = $('input[name=active]').prop('checked');
        show_inactive = $('input[name=inactive]').prop('checked');

    _.each(members, function(m) {
        roles = [];
        _.each(m.roles, function(r) {
            if (_.indexOf(selected_departments, r.department) != -1) {
                if (r.active && show_active || !r.active && show_inactive) {
                    roles.push(r.type);
                }
            }
        });
        m.roles_display = roles.join(', ');
    });
}

// Kick off things
$(function () {
    Departments.initialize();
    var memberView = new Etat.Views.MemberView({el:$('#member-view')});

    $('#ajax-modal').on('modal-saved', function() {
        memberView.loadMembers();
    });
});