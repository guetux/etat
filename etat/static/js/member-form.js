
Etat.Views.MemberForm = Backbone.View.extend({
    events : {
        'click #add-address'        : 'addAddress',
        'click #add-role'           : 'addRole',
        'click #add-reachability'   : 'addReachability',
        'change input[name$=main]'  : 'onlyOneAddress',
    },

    addAddress: function(event) {
        $('a[href=#addresses]').tab('show');
        $('#addresses .extra').fadeIn();
        $(event.target).prop('disabled', true);
        return false;
    },

    addRole: function(event) {
        $('a[href=#roles]').tab('show');
        $('#roles .extra').fadeIn();
        $(event.target).prop('disabled', true);
        return false;
    },

    addReachability: function(event) {
        $('a[href=#reachability]').tab('show');
        $('#reachability .extra').fadeIn();
        $(event.target).prop('disabled', true);
        return false;
    },

    onlyOneAddress: function(event) {
        $('input[name$=main][id!='+event.target.id+']').prop('checked', false);
    },

    currentDate: function() {
        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth()+1;
        var yyyy = today.getFullYear();
        return dd + '.' + mm + '.' + yyyy;
    },

    initialize: function() {
        // preselect new role deparmtent and type (if possible) for new roles
        if (this.$el.hasClass('add')) {
            var selected = _(Departments.get_selected()).first();
            if (selected) {
                var dep = $('#department_tree #' + selected);
                var id = dep.attr('id');
                var default_role = dep.data('default_role');
                $('#roles .extra select[name$=department]:first').val(id);
                $('#roles .extra select[name$=type]:first').val(default_role);
                $('#roles .extra input[name$=start]:first').val(this.currentDate());
            }
        }

        // Initialize chosen and datepicker
        $(".member-form select").chosen({width: '100%'});
        $("input.date").datepicker({format: 'dd.mm.yyyy'});
    }
});

