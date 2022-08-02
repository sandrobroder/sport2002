odoo.define('pc_sport2002_temporary_fixed_add_to_cart.sale_cart_link', function(require) {
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
        _onClickAdd: function (ev) {
//            this._super.apply(this, arguments);
            alert("SI")
        }
    });
});