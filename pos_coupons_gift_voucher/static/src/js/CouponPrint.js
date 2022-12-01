
odoo.define('pos_coupons_gift_voucher.CouponPrint', function(require) {
	'use strict';

	const PosComponent = require('point_of_sale.PosComponent');
	const Registries = require('point_of_sale.Registries');

	class CouponPrint extends PosComponent {
		constructor() {
			super(...arguments);
		}

		coupon_render_env() {
			var data = this.env.pos.get('coupon_print_data');
			var coup_data=this.env.pos.get_order().get_screen_data();
			return {
				widget: this,
				pos: this.env.pos,
				name: coup_data.props.data.coup_name,
				issue: coup_data.props.data.coup_issue_dt,
				expire : coup_data.props.data.coup_exp_dt,
				amount : coup_data.props.data.coup_amount,
				number : coup_data.props.data.coup_code,
				am_type : coup_data.props.data.am_type,
			};
		}

		get __receiptBarcode(){
			var coup_data=this.env.pos.get_order().get_screen_data();
			var number_bar = coup_data.props.data.coup_code;
			var trues = $("#barcode_print2").barcode(
				number_bar, // Value barcode (dependent on the type of barcode)
				"code128" // type (string)
			);
		return true
		}
	}
	
	CouponPrint.template = 'CouponPrint';
	Registries.Component.add(CouponPrint);
	return CouponPrint;
});