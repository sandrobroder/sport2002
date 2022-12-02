odoo.define('website_b2c_product_price', function (require) {
"use strict";

    var models = require('point_of_sale.models');
    var nmodels = models.PosModel.prototype.models;
    models.load_fields('product.product',['customer_list_price']);

    for(var i=0; i < nmodels.length; i++){
        var model=nmodels[i];
        if(model.model === 'product.product'){
            model.loaded = function(self, products){
                var using_company_currency = self.config.currency_id[0] === self.company.currency_id[0];
                var conversion_rate = self.currency.rate / self.company_currency.rate;
                self.db.add_products(_.map(products, function (product) {
                    product.lst_price = product.customer_list_price;
                    if (!using_company_currency) {
                        product.lst_price = round_pr(product.lst_price * conversion_rate, self.currency.rounding);
                    }
                    product.taxes_id = [];
                    product.categ = _.findWhere(self.product_categories, {'id': product.categ_id[0]});
                    product.pos = self;
                    return new models.Product({}, product);
                }));
            }
        } 
    }
});

