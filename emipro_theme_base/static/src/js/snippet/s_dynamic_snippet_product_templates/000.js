odoo.define('emipro_theme_base.s_dynamic_snippet_prod_temp', function (require) {
'use strict';

const publicWidget = require('web.public.widget');
const DynamicSnippetCarousel = require('website.s_dynamic_snippet_carousel');
var wSaleUtils = require('website_sale.utils');
const {Markup} = require('web.utils');

const DynamicSnippetProdTemp = DynamicSnippetCarousel.extend({
    selector: '.s_dynamic_snippet_prod_temp',
    _getCategorySearchDomain() {
        const searchDomain = [];
        let productCategoryId = this.$el.get(0).dataset.productCategoryId;
        if (productCategoryId && productCategoryId !== 'all') {
            if (productCategoryId === 'current') {
                productCategoryId = undefined;
                const productCategoryField = $("#product_details").find(".product_category_id");
                if (productCategoryField && productCategoryField.length) {
                    productCategoryId = parseInt(productCategoryField[0].value);
                }
                if (!productCategoryId) {
                    this.trigger_up('main_object_request', {
                        callback: function (value) {
                            if (value.model === "product.public.category") {
                                productCategoryId = value.id;
                            }
                        },
                    });
                }
                if (!productCategoryId) {
                    // Try with categories from product, unfortunately the category hierarchy is not matched with this approach
                    const productTemplateId = $("#product_details").find(".product_template_id");
                    if (productTemplateId && productTemplateId.length) {
                        searchDomain.push(['public_categ_ids.product_tmpl_ids', '=', parseInt(productTemplateId[0].value)]);
                    }
                }
            }
            if (productCategoryId) {
                searchDomain.push(['public_categ_ids', 'child_of', parseInt(productCategoryId)]);
            }
        }
        return searchDomain;
    },
    _getBrandSearchDomain() {
        const searchDomain = [];
        let productBrandId = this.$el.get(0).dataset.productBrandId;
        if (productBrandId && productBrandId !== 'all') {
            if (productBrandId === 'current') {
                productBrandId = undefined;
                const productBrandField = $("#product_details").find(".product_brand_id");
                if (productBrandField && productBrandField.length) {
                    productBrandId = parseInt(productBrandField[0].value);
                }
                if (!productBrandId) {
                    this.trigger_up('main_object_request', {
                        callback: function (value) {
                            if (value.model === "product.brand") {
                                productBrandId = value.id;
                            }
                        },
                    });
                }
            }
            if (productBrandId) {
                searchDomain.push(['product_brand_id', '=', parseInt(productBrandId)]);
            }
        }
        return searchDomain;
    },
    _getTagSearchDomain() {
        const searchDomain = [];
        let productTagIds = this.$el.get(0).dataset.productTagIds;
        if (productTagIds) {
            searchDomain.push(['product_variant_ids.all_product_tag_ids', 'in', JSON.parse(productTagIds).map(productTag => productTag.id)]);
        }
        return searchDomain;
    },
    _getSelectedProdTempSearchDomain() {
        const searchDomain = [];
        let productTemplateIds = this.$el.get(0).dataset.productTemplateIds;
        if (productTemplateIds && productTemplateIds != '[]') {
            searchDomain.push(['id', 'in', JSON.parse(productTemplateIds).map(productTemplate => productTemplate.id)]);
        }
        return searchDomain;
    },
    _getSearchDomain: function () {
        const searchDomain = this._super.apply(this, arguments);
        searchDomain.push(...this._getSelectedProdTempSearchDomain());
        searchDomain.push(...this._getCategorySearchDomain());
        searchDomain.push(...this._getBrandSearchDomain());
        searchDomain.push(...this._getTagSearchDomain());
        const productNames = this.$el.get(0).dataset.productNames;
        if (productNames) {
            const nameDomain = [];
            for (const productName of productNames.split(',')) {
                // Ignore empty names
                if (!productName.length) {
                    continue;
                }
                // Search on name, internal reference and barcode.
                if (nameDomain.length) {
                    nameDomain.unshift('|');
                }
                nameDomain.push(...[
                    '|', '|', ['name', 'ilike', productName],
                              ['default_code', '=', productName],
                              ['barcode', '=', productName],
                ]);
            }
            searchDomain.push(...nameDomain);
        }
        return searchDomain;
    },
    _getRpcParameters: function () {
        const productTemplateId = $("#product_details").find(".product_template_id");
        return Object.assign(this._super.apply(this, arguments), {
            productTemplateId: productTemplateId && productTemplateId.length ? productTemplateId[0].value : undefined,
        });
    },
    async _fetchData() {
        if (this._isConfigComplete()) {
            const nodeData = this.el.dataset;
            const data = {
                'add2cart': this.$el.attr('data-add2cart'),
                'wishlist': this.$el.attr('data-wishlist'),
                'quickview': this.$el.attr('data-quickview'),
                'rating': this.$el.attr('data-rating'),
                'product_label': this.$el.attr('data-product_label'),
            };
            const filterFragments = await this._rpc({
                'route': '/website/snippet/filters',
                'params': Object.assign({
                    'filter_id': parseInt(nodeData.filterId),
                    'template_key': nodeData.templateKey,
                    'limit': parseInt(nodeData.numberOfRecords),
                    'search_domain': this._getSearchDomain(),
                    'with_sample': this.editableMode,
                    'product_context': data,
                    'context': {
                        '_bugfix_force_minimum_max_limit_to_16': !!nodeData.forceMinimumMaxLimitTo16,
                    },
                }, this._getRpcParameters()),
            });
            this.data = filterFragments.map(Markup);
        } else {
            this.data = [];
        }
    },
});
publicWidget.registry.dynamic_snippet_prod_temp = DynamicSnippetProdTemp;

return DynamicSnippetProdTemp;
});
