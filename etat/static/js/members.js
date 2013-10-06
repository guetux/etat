
// Global members list
ml = new List('member-list', {
    valueNames: ['first_name', 'last_name', 'scout_name']
});

function load_members() {
    // Reload members for selected departments
    var deptree = jQuery.jstree._reference('#department_tree'),
        ids = [],
        data = {};

    // Use checked departmens if checkbox is enabled
    _.each(deptree.get_checked(null, true), function(e) {
        ids.push(parseInt(e.id, 10));
    });

    // Use selection if no checkbox is set
    if (ids.length === 0) {
        _.each(deptree.get_selected(), function(e) {
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
    }

    $.ajax({
        dataType: 'json',
        type: 'GET',
        url: '/api/members/',
        data: data,
        success: function(data) {
            ml.clear();
            if (data.length) {
                ml.add(data);
                $('#empty-msg').hide();
            } else {
                $('#empty-msg').show();
            }
            ml.search();
            ml.sort('id', { asc: true });
            $('#member-list').find('input[type=search]').val('');
        }
    });
}

$(function () {
    // Init department tree
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
        'select_node.jstree': load_members,
        'deselect_node.jstree': load_members,
        'check_node.jstree': load_members,
        'uncheck_node.jstree': load_members
    });

    // checkbox enabler
    var deptree = jQuery.jstree._reference('#department_tree');
    setTimeout(function() { deptree.hide_checkboxes();}, 10);
    $('#checkselector').on('switch-change', function(e, data) {
        if (data.value) {
            deptree.show_checkboxes();
        } else {
            deptree.uncheck_all();
            deptree.hide_checkboxes();
            load_members();
        }
    });

    // filter actions
    $('#roles-filter').change(load_members);
    $('.status-filter input').change(load_members);

    $('input[name=male]').change(function() {
        show = $(this).prop('checked');
        ml.filter(function(member) {
            return member.values().gender == 'm' && show;
        });
    });

    $('.gender-filter input').change(function() {
        var show_m = $('input[name=m]').prop('checked'),
            show_f = $('input[name=f]').prop('checked');
        if (!show_m && !show_f) {
            ml.filter();
        } else {
            ml.filter(function(member) {
                var gender = member.values().gender;
                return gender == 'm' && show_m || gender == 'f' && show_f;
            });
        }
    });
});