
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
    } else if (!active && !inactive) {
        data['status'] = 'none';
    }

    $.ajax({
        dataType: 'json',
        type: 'GET',
        url: '/api/members/',
        data: data,
        success: function(data) {
            ml.clear();
            if (data.length) {
                append_roles(data, ids, active, inactive);
                ml.add(data);
                $('#empty-msg').hide();
            }
            ml.search();
            ml.sort('id', { asc: true });
            $('#member-list').find('input[type=search]').val('');
        }
    });
}

function append_roles(members, deparment_ids, show_active, show_inactive) {
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

    // Actions
    $('#add-member').on('click', function () {
        load_modal('add/', {width: '900px'});
    });

    $( "#memberlist").on("click", ".detail", function() {
        var id = $(this).parents('tr').find('td.id').text();
        var url = '/members/' + id + '/';
        load_modal(url, {width: '700px'});
    });

    $( "#memberlist").on("click", ".edit", function() {
        var id = $(this).parents('tr').find('td.id').text();
        var url = '/members/' + id + '/edit/';
        load_modal(url, {width: '900px'});
    });


    // Modal handling
    var $modal = $('#ajax-modal');

    function load_modal(url, options) {
        $('body').modalmanager('loading');
        $modal.load(url, function(){
            $modal.modal(options);
        });
    }

    $('#ajax-modal').on('click', '.modal_link', function() {
        var url = $(this).attr('href');
            new_width = $(this).data('width') || '900px';

        $modal.load(url, function() {
            $modal.data('modal').options.width = new_width;
            $modal.modal('layout');
        });
        return false;
    });

    $('#ajax-modal').on('submit', 'form', function() {
        $modal.modal('loading');
        $(this).ajaxSubmit({
            target: '#ajax-modal',
            success: function (res, status, xhr) {
                if (xhr.status == 204) {
                    load_members();
                    $modal.modal('hide');
                }
            },
            error: function(res) {
                $modal.html('<pre>'+res.responseText+'</pre>');
            }
        });
        return false;
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