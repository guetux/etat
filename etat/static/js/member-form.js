
Etat.Views.MemberForm = Backbone.View.extend({
    events : {
        'change input[name$=main]'  : 'onlyOneAddress',
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

    initWidgets: function() {
        $(".member-form select").chosen({width: '100%'});
        $(".member-form input.date").datepicker({format: 'dd.mm.yyyy'});
    },

    initialize: function() {
        // preselect new role deparmtent and type (if possible) for new roles
        // if (this.$el.hasClass('add')) {
        //     var selected = _(Departments.get_selected()).first();
        //     if (selected) {
        //         var dep = $('#department_tree #' + selected);
        //         var id = dep.attr('id');
        //         var default_role = dep.data('default_role');
        //         $('#roles .extra select[name$=department]:first').val(id);
        //         $('#roles .extra select[name$=type]:first').val(default_role);
        //         $('#roles .extra input[name$=start]:first').val(this.currentDate());
        //     }
        // }

        $('.member-tab-nav a').click(function() {
            $(this).tab('show');
        });

        $('.addresses tr').formset({
            prefix: 'addresses',
            formCssClass: 'addresses-formset',
            added: this.initWidgets
        });

        $('.reachability tr').formset({
            prefix: 'reachabilities',
            formCssClass: 'reachability-formset',
            added: this.initWidgets
        });

        $('#roles tr').formset({
            prefix: 'roles',
            formCssClass: 'roles-formset',
            added: this.initWidgets
        });

        this.initWidgets();

    }
});

