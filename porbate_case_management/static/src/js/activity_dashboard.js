odoo.define('porbate_case_management.activity_dashboard', function (require) {
    'use strict';
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var QWeb = core.qweb;
    var session = require('web.session');
    var user = session.user_id

    var ActivityDashboard = AbstractAction.extend({
    template: 'ActivityDashboard',
    events: {
        'click .all_stage': 'all_stage',
        'click .draft_stage': 'draft_stage',
        'click .waiting_tiss_stage': 'waiting_tiss_stage',
        'click .completion_form_stage': 'completion_form_stage',
        'click .pending_hro_approval_stage': 'pending_hro_approval_stage',
        'click .pending_payment_stage': 'pending_payment_stage',
        'click .case_to_close_stage': 'case_to_close_stage',
        'click .close_stage': 'close_stage',
        'click .total_inventory': 'total_inventory',
        'click .paid_inventory': 'paid_inventory',
        'click .partially_inventory': 'partially_inventory',
        'click .not_paid': 'not_paid',
        'click .activity_type': 'activity_type',
        'click .click-view': 'click_view',
        'click .click-origin-view': 'click_origin_view'
    },
    init: function(parent, context) {
        this._super(parent, context);
        this.upcoming_events = [];
        this.dashboards_templates = ['LoginUser', 'ManageActivity', 'ActivityTable'];

        this.login_employee = [];
    },

    start: function() {
        var self = this;
        this.set("title", 'Dashboard');
        return this._super().then(function() {
            self.render_dashboards();
        });
    },

    render_dashboards: function () {
        var self = this;
        this._rpc({
            model: 'probate.case',
            method : 'get_state_count',
            args: [[]]
        }).then(function(result){
            self.$('.table_view').html(QWeb.render('ManageActivity', {
                len_all: result.len_all,
                len_draft: result.len_draft,
                len_waiting_tiss: result.len_waiting_tiss,
                len_completion_form: result.len_completion_form,
                len_pending_hro_approval: result.len_pending_hro_approval,
                len_pending_payment: result.len_pending_payment,
                len_case_to_close: result.len_case_to_close,
                len_closed: result.len_closed,
                total_inventory:result.total_inventory,
                paid_inventory: result.paid_inventory,
                partially_inventory: result.partially_inventory,
                not_paid: result.not_paid
            }));
        });
        self.results = '';
        self._rpc({
            model: 'probate.case',
            method: 'search_read',
            domain: [["state", "=", 'case_to_close']],
            context: { active_test: false },
        }).then(function (case_to_close_stage) {
            self._rpc({
                model: 'probate.case',
                method: 'search_read',
                domain: [["state", "=", 'draft']],
                context: { active_test: false },
            }).then(function (draft_stage) {
                self._rpc({
                    model: 'probate.case',
                    method: 'search_read',
                    domain: [["state", "=", 'waiting_tiss']],
                    context: { active_test: false },
                }).then(function (waiting_tiss_stage) {
                    self._rpc({
                        model: 'probate.case',
                        method: 'search_read',
                        domain: [["state", "=", 'completion_form']],
                        context: { active_test: false },
                    }).then(function (completion_form_stage) {
                        self._rpc({
                            model: 'probate.case',
                            method: 'search_read',
                            domain: [["state", "=", 'pending_hro_approval']],
                            context: { active_test: false },
                        }).then(function (pending_hro_approval_stage) {
                            self._rpc({
                                model: 'probate.case',
                                method: 'search_read',
                                domain: [["state", "=", 'pending_payment']],
                                context: { active_test: false },
                            }).then(function (pending_payment_stage) {
                                // Menambahkan panggilan metode RPC untuk mencari rekaman dengan status 'closed'
                                self._rpc({
                                    model: 'probate.case',
                                    method: 'search_read',
                                    domain: [["state", "=", 'closed']],
                                    context: { active_test: false },
                                }).then(function (closed_stage) {
                                    self.$('.table_view_activity').html(QWeb.render('ActivityTable', {
                                        case_to_close_stage: case_to_close_stage,
                                        draft_stage: draft_stage,
                                        waiting_tiss_stage: waiting_tiss_stage,
                                        completion_form_stage: completion_form_stage,
                                        pending_hro_approval_stage: pending_hro_approval_stage,
                                        pending_payment_stage: pending_payment_stage,
                                        closed_stage: closed_stage
                                    }));
                                });
                            });
                        });
                    });
                });
            });
        });
    },
    click_view: function(e){
        var id = e.target.value;
        this.do_action({
            type: 'ir.actions.act_window',
            name: 'All Stage',
            res_model: 'probate.case',
            res_id: parseInt(id),
            views: [[false, 'form']],
            view_mode: 'form',
            target: 'current'
        });
    },
    click_origin_view: function(e){
        var id_ = e.target.value;
        var self = this;
        this._rpc({
            model: 'probate.case',
            method : 'get_activity',
            args: [[],parseInt(id_)],
        }).then(function(result){this
            self.do_action({
            type: 'ir.actions.act_window',
            name: 'Activity Origin',
            res_model: result.model,
            res_id: result.res_id,
            views: [[false, 'form']],
            view_mode: 'form',
            target: 'current'
        });
        });
    },

    all_stage: function(e) {
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        this.do_action({
            type: 'ir.actions.act_window',
            name: 'All Case',
            res_model: 'probate.case',
            domain: [],
            views: [[false, 'list'], [false, 'form']],
            view_mode: 'list',
            target: 'current',
            context: { active_test: false },
        });
    },

    draft_stage: function(e) {
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        this.do_action({
            type: 'ir.actions.act_window',
            name: 'Draft',
            res_model: 'probate.case',
            domain: [['state', '=', 'draft']],
            views: [[false, 'list'], [false, 'form']],
            view_mode: 'list',
            target: 'current',
            context: { active_test: false },
        });
    },

    completion_form_stage: function(e) {
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        this.do_action({
            type: 'ir.actions.act_window',
            name: 'Completion Form',
            res_model: 'probate.case',
            domain: [['state', '=', 'completion_form']],
            views: [[false, 'list'], [false, 'form']],
            view_mode: 'list',
            target: 'current',
            context: { active_test: false },
        });
    },

    pending_hro_approval_stage: function(e) {
        var self = this;
        e.stopPropagation();
        e.preventDefault();

        this.do_action({
            type: 'ir.actions.act_window',
            name: "Pending HRO Approval",
            res_model: 'probate.case',
            domain: [['state', '=', 'pending_hro_approval']],
            views: [[false, 'list'], [false, 'form']],
            view_mode: 'list',
            target: 'current',
            context: { active_test: false },
        });
    },

    waiting_tiss_stage: function(e) {
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        this.do_action({
            type: 'ir.actions.act_window',
            name: 'Waiting Tiss',
            res_model: 'probate.case',
            domain: [['state', '=', 'waiting_tiss']],
            views: [[false, 'list'], [false, 'form']],
            view_mode: 'list',
            target: 'current',
            context: { active_test: false },
        });

    },

    pending_payment_stage: function(e) {
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        this.do_action({
            type: 'ir.actions.act_window',
            name: "Pending Payment",
            res_model: 'probate.case',
            domain: [['state', '=', 'pending_payment']],
            views: [[false, 'list'], [false, 'form']],
            view_mode: 'list',
            target: 'current',
            context: { active_test: false },
        });
    },

    case_to_close_stage: function(e) {
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        this.do_action({
            type: 'ir.actions.act_window',
            name: "To Close",
            res_model: 'probate.case',
            domain: [['state', '=', 'case_to_close']],
            views: [[false, 'list'], [false, 'form']],
            view_mode: 'list',
            target: 'current',
            context: { active_test: false },
        });
    },
    close_stage: function(e) {
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        this.do_action({
            type: 'ir.actions.act_window',
            name: "Closed",
            res_model: 'probate.case',
            domain: [['state', '=', 'closed']],
            views: [[false, 'list'], [false, 'form']],
            view_mode: 'list',
            target: 'current',
            context: { active_test: false },
        });
    },
    total_inventory: function(e) {
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        this.do_action({
            type: 'ir.actions.act_window',
            name: "Total Inventory",
            res_model: 'probate.case.property.value',
            views: [[false, 'kanban'],[false, 'list'], [false, 'form']],
            view_mode: 'kanban',
            target: 'current',
            context: { active_test: false },
        });
    },
    paid_inventory: function(e) {
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        this.do_action({
            type: 'ir.actions.act_window',
            name: "Paid Inventory",
            res_model: 'payment.beneficaries',
            // domain: [['state', '=', 'paid']],
            views: [[false, 'kanban'],[false, 'list'], [false, 'form']],
            view_mode: 'kanban',
            target: 'current',
            context: { active_test: false },
        });
    },
    partially_inventory: function(e) {
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        this.do_action({
            type: 'ir.actions.act_window',
            name: "Partially Paid Inventory",
            res_model: 'probate.case.property.value',
            domain: [['state', '=', 'partial']],
            views: [[false, 'kanban'],[false, 'list'], [false, 'form']],
            view_mode: 'kanban',
            target: 'current',
            context: { active_test: false },
        });
    },
    not_paid: function(e) {
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        this.do_action({
            type: 'ir.actions.act_window',
            name: "Not Paid at All",
            res_model: 'probate.case.property.value',
            domain: [['state', '=', 'pending_payment']],
            views: [[false, 'kanban'],[false, 'list'], [false, 'form']],
            view_mode: 'kanban',
            target: 'current',
            context: { active_test: false },
        });
    },

    activity_type: function(e) {
        var self = this;
        e.stopPropagation();
        e.preventDefault();
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        var action = {
            type: 'ir.actions.act_window',
            name: 'Activity Type',
            res_model: 'activity.type',
            domain: [['state', 'in', ['today']]],
            views: [[false, 'list'], [false, 'form']],
            view_mode: 'list',
            target: 'current'
        }
        this.do_action({
            type: 'ir.actions.act_window',
            name: "Today's Activity",
            res_model: 'probate.case.type',
            views: [[false, 'list'], [false, 'form']],
            view_mode: 'list',
            target: 'current'
        });
    },

});
   core.action_registry.add("activity_dashboard", ActivityDashboard);
   return ActivityDashboard;
});
