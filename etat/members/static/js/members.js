
// Global members list
ml = new List('member-list', {
    valueNames: ['first_name', 'last_name', 'scout_name']
});

function load_members() {
    // Reload members for selected departments
    var deptree = jQuery.jstree._reference('#department_tree');
    var ids = []
    data = {}

    // Use checked departmens if checkbox is enabled
    $.each(deptree.get_checked(null, true), function (i, e) {
        ids.push(parseInt(e.id));
    });

    // Use selection if no checkbox is set
    if (ids.length == 0) {
        $.each(deptree.get_selected(), function (i, e) {
            ids.push(parseInt(e.id));
        });
    }

    data['department_ids'] = ids;

    // Collect filters
    data['roles'] = $('#roles-filter').val();
    data['gender'] = $('#gender-filter').val();
    data['inactive'] = $('#inactive-filter').is(':checked');

    $.ajax({
        dataType: 'json',
        type: 'GET',
        url: 'data/',
        data: data,
        success: function (data) {
            ml.clear()
            ml.add(data);
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
    setTimeout(function () { deptree.hide_checkboxes();}, 10);
    $('#checkselector').on('switch-change', function (e, data) {
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
    $('#gender-filter').change(load_members);
    $('#inactive-switch').on('switch-change', load_members);

    // filter collapse
    $('#filters').on('hidden', function () {
        var caret = $('a[data-target="#filters"]').find('i');
        caret.removeClass('icon-caret-up');
        caret.addClass('icon-caret-down');
    });

    $('#filters').on('shown', function () {
        var caret = $('a[data-target="#filters"]').find('i');
        caret.removeClass('icon-caret-down');
        caret.addClass('icon-caret-up');
    });
});