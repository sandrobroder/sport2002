odoo.define('pos_coupons_gift_voucher.pos', function(require) {
	"use strict";

	var models = require('point_of_sale.models');
	var core = require('web.core');
	var rpc = require('web.rpc');
	var field_utils = require('web.field_utils');
	var session = require('web.session');
	var time = require('web.time');
	var utils = require('web.utils');
	var QWeb = core.qweb;
	var _t = core._t;

	models.load_fields('product.product', ['type','is_coupon_product']);

	models.load_models({
		model: 'pos.gift.coupon',
		fields: ['name','apply_coupon_on', 'c_barcode', 'user_id', 'issue_date', 'expiry_date',
		 'partner_id', 'order_ids', 'active', 'amount', 'description','used','coupon_count', 
		 'coupon_apply_times','expiry_date','partner_true','partner_id'],
		domain: null,
		loaded: function(self, pos_gift_coupon) { 
			self.pos_gift_coupon = pos_gift_coupon;    
		},
	});

	var posorder_super = models.Order.prototype;
	models.Order = models.Order.extend({
		initialize: function(attr, options) {
			this.is_coupon_used = this.is_coupon_used || false;
			this.coupon_id = this.coupon_id || false;
			this.coup_maxamount = this.coup_maxamount || false;
			posorder_super.initialize.call(this,attr,options);
		},

		set_is_coupon_used: function(is_coupon_used){
			this.is_coupon_used = is_coupon_used;
			this.trigger('change',this);
		},

		get_is_coupon_used: function(is_coupon_used){
			return this.is_coupon_used;
		},

		export_as_JSON: function() {
			var self = this;
			var loaded = posorder_super.export_as_JSON.call(this);
			loaded.is_coupon_used = self.is_coupon_used || false;
			loaded.coupon_id = self.coupon_id;
			loaded.coup_maxamount = self.coup_maxamount;
			return loaded;
		},

		init_from_JSON: function(json){
			posorder_super.init_from_JSON.apply(this,arguments);
			this.is_coupon_used = json.is_coupon_used || false;
			this.coupon_id = json.coupon_id;
			this.coup_maxamount = json.coup_maxamount;
		},

		remove_orderline: function( line ){
			var prod = line.product;
			if(prod && prod.is_coupon_product){
				this.set_is_coupon_used(false);
			}
			this.assert_editable();
			this.orderlines.remove(line);
			this.coupon_id = false;	
			this.select_orderline(this.get_last_orderline());
		},

	});
});
