odoo.define('website_b2c_product_price.Product', function (require) {
    "use strict";

    const { Product } = require('point_of_sale.models');
    const { PosGlobalState } = require('point_of_sale.models');

    const Registries = require('point_of_sale.Registries');

    const ProductPriceUpdate = (Product) =>
        class extends Product {
            get_price(pricelist, quantity, price_extra) {
                var self = this;
                var date = moment();

                // In case of nested pricelists, it is necessary that all pricelists are made available in
                // the POS. Display a basic alert to the user in this case.
                if (!pricelist) {
                    alert(_t(
                        'An error occurred when loading product prices. ' +
                        'Make sure all pricelists are available in the POS.'
                    ));
                }

                var pricelist_items = _.filter(
                    self.applicablePricelistItems[pricelist.id],
                    function (item) {
                        return self.isPricelistItemUsable(item, date);
                    }
                );

                var price = self.lst_price;
                if (price_extra) {
                    price += price_extra;
                }
                _.find(pricelist_items, function (rule) {
                    if (rule.min_quantity && quantity < rule.min_quantity) {
                        return false;
                    }
                    if (pricelist.use_b2c_price) {
                        price = self.customer_list_price
                    }
                    else if (rule.base === 'pricelist') {
                        let base_pricelist = _.find(self.pos.pricelists, function (pricelist) {
                            return pricelist.id === rule.base_pricelist_id[0];
                        });
                        if (base_pricelist) {
                            price = self.get_price(base_pricelist, quantity);
                        }
                    } else if (rule.base === 'standard_price') {
                        price = self.standard_price;
                    }


                    if (rule.compute_price === 'fixed') {
                        price = rule.fixed_price;
                        return true;
                    } else if (rule.compute_price === 'percentage') {
                        price = price - (price * (rule.percent_price / 100));
                        return true;
                    } else {
                        var price_limit = price;
                        price = price - (price * (rule.price_discount / 100));
                        if (rule.price_round) {
                            price = round_pr(price, rule.price_round);
                        }
                        if (rule.price_surcharge) {
                            price += rule.price_surcharge;
                        }
                        if (rule.price_min_margin) {
                            price = Math.max(price, price_limit + rule.price_min_margin);
                        }
                        if (rule.price_max_margin) {
                            price = Math.min(price, price_limit + rule.price_max_margin);
                        }
                        return true;
                    }

                    return false;
                });

                // This return value has to be rounded with round_di before
                // being used further. Note that this cannot happen here,
                // because it would cause inconsistencies with the backend for
                // pricelist that have base == 'pricelist'.
                return price;
            }
        };


    const PosGlobalStateUpdate = (PosGlobalState) =>
        class extends PosGlobalState {
            computePriceAfterFp(price, taxes) {
                const order = this.get_order();
                var pricelist = order.pricelist
                if (order && pricelist && pricelist.use_b2c_price) {
                    return price;
                }
                if (order && order.fiscal_position) {
                    let mapped_included_taxes = [];
                    let new_included_taxes = [];
                    const self = this;
                    _(taxes).each(function (tax) {
                        const line_taxes = self.get_taxes_after_fp([tax.id], order.fiscal_position);
                        if (line_taxes.length && line_taxes[0].price_include) {
                            new_included_taxes = new_included_taxes.concat(line_taxes);
                        }
                        if (tax.price_include && !_.contains(line_taxes, tax)) {
                            mapped_included_taxes.push(tax);
                        }
                    });

                    if (mapped_included_taxes.length > 0) {
                        if (new_included_taxes.length > 0) {
                            const price_without_taxes = this.compute_all(mapped_included_taxes, price, 1, this.currency.rounding, true).total_excluded
                            return this.compute_all(new_included_taxes, price_without_taxes, 1, this.currency.rounding, false).total_included
                        }
                        else {
                            return this.compute_all(mapped_included_taxes, price, 1, this.currency.rounding, true).total_excluded;
                        }
                    }
                }
                return price;
            }

            get_taxes_after_fp(taxIds, fpos) {
                const order = this.get_order();
                if (order) {
                    var pricelist = order.pricelist
                    if (order && pricelist && pricelist.use_b2c_price) {
                        return [];
                    }
                }
                else {
                    if (this.default_pricelist && this.default_pricelist.use_b2c_price) {
                        return [];
                    }
                }
                if (!fpos) {
                    return taxIds.map((taxId) => this.taxes_by_id[taxId]);
                }
                let mappedTaxes = [];
                for (const taxId of taxIds) {
                    const tax = this.taxes_by_id[taxId];
                    if (tax) {
                        const taxMaps = Object.values(fpos.fiscal_position_taxes_by_id).filter(
                            (fposTax) => fposTax.tax_src_id[0] === tax.id
                        );
                        if (taxMaps.length) {
                            for (const taxMap of taxMaps) {
                                if (taxMap.tax_dest_id) {
                                    const mappedTax = this.taxes_by_id[taxMap.tax_dest_id[0]];
                                    if (mappedTax) {
                                        mappedTaxes.push(mappedTax);
                                    }
                                }
                            }
                        } else {
                            mappedTaxes.push(tax);
                        }
                    }
                }
                return _.uniq(mappedTaxes, (tax) => tax.id);
            }
        };
    Registries.Model.extend(Product, ProductPriceUpdate);
    Registries.Model.extend(PosGlobalState, PosGlobalStateUpdate);

    return Product;
});

