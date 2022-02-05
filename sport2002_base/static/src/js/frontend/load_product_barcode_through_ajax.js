odoo.define('sport2002_base.load_product_barcode_through_ajax', function(require) {
    'use strict';

    var sAnimations = require('website.content.snippets.animation');
    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');
    var config = require('web.config');
    var VariantMixin = require('sale.VariantMixin');
    var themeEvent = new sAnimations.registry.themeEvent();
    var StickyFilter = new sAnimations.registry.StickyFilter();
    var product_detail = new sAnimations.registry.product_detail();
    var priceSlider = new publicWidget.registry.price_slider();
    var quickFilter = new sAnimations.registry.te_quick_filter_main_div();
    var core = require('web.core');
    var _t = core._t;

    sAnimations.registry.WebsiteSale.include({
        /**
         * Displays SKU and change based on select varient
         * current combination.
         *
         * @override
         */
		_onChangeCombination:function (ev, $parent, combination) {
		    this._super.apply(this, arguments);
		    if( combination.sku_details ){
		        $(".js_barcode_div").html(combination.barcode_details);
		    }
		    else{
		        $(".js_barcode_div").html('N/A');
		    }
		},
    });
});