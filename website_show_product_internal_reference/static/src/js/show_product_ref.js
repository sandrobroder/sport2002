odoo.define('website_show_product_internal_reference.show_ref', function (require) {
    'use strict';
    require('website_sale.website_sale');

    var publicWidget = require('web.public.widget');

    publicWidget.registry.WebsiteSale.include({
        _onChangeCombination: function (ev, $parent, combination) {
            console.log(">>>>>>>>>>>>>>>>>>>>>>>>>>>>ddddddddddddd")
            if (combination.internal_ref) {
                $('#product_internal_ref').text(combination.internal_ref)
            }
            else {
                $('#product_internal_ref').text("")
            }
            this._super.apply(this, arguments);
        },
    });

});
