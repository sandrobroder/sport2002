odoo.define('emipro_theme_base.load_product_through_ajax', function(require) {
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

    publicWidget.registry.load_ajax = publicWidget.Widget.extend({
        selector: ".oe_website_sale",
        events: {
            'click .te_clear_attr_a': '_onClearAttribInd',
            'click .te_clear_all_form_selection': '_onClearAttribAll',
            'click .te_clear_all_variant': '_onClearAttribDiv',
        },
        filterData: function (event) {
            /* This method is used to check the load ajax is enable or not
             And If It's enable then send the ajax request otherwise submit the form*/
            var inputMinVal = parseFloat($("input.ept_price_min").val());
            var inputMaxVal = parseFloat($("input.ept_price_max").val());
            var minValue = parseFloat($("#price_slider_min").val());
            var maxValue = parseFloat($("#price_slider_max").val());

            // Don't submit the price filter data if price filter not appyied
            if (inputMinVal==minValue && inputMaxVal==maxValue){
                $("input.ept_price_min").removeAttr('name')
                $("input.ept_price_max").removeAttr('name')
            }
            if($(".load_products_through_ajax").length)
            {
                var through_ajax = $(".load_products_through_ajax").val();
                if(through_ajax == 'True')
                {
                    this.sendAjaxToFilter(event);
                }
            }else {
                $("form.js_attributes input,form.js_attributes select").closest("form").submit();
            }

        },
        sendAjaxToFilter: function (event) {
            /* This method is used foe send the ajax request to get the filtered data */
            $('.cus_theme_loader_layout').removeClass('d-none');
            var url = window.location.pathname;
            var frm = $('.js_attributes')

            var url_prm = frm.serialize()

            url = url + "?" + url_prm;
            window.history.pushState({}, "", url);
            $.ajax({
                url: url,
                type: 'GET',
                success: function(data) {
                    var data_replace = null;
                    data_replace = $(data).find(".o_wsale_products_main_row");
                    $(".o_wsale_products_main_row").replaceWith(data_replace);
                    data_replace = $(data).find('.products_pager:first');
                    $(".products_pager:first").replaceWith(data_replace);
                    data_replace = $(data).find('.products_pager:last');
                    $(".products_pager:last").replaceWith(data_replace);
                    data_replace = $(data).find('.te_shop_filter_resp');
                    $(".te_shop_filter_resp").replaceWith(data_replace);
                    data_replace = $(data).find('.load_more_next_page');
                    $(".load_more_next_page").replaceWith(data_replace);
                    themeEvent.onShowClearVariant();
                    themeEvent.onSelectAttribute();
                    StickyFilter._stickyFilter();
                    priceSlider.start();
                    quickFilter.start();
                    $("html, body").animate({
                        scrollTop: 0
                    }, 1000);
                    if ($(window).width() < 768) {
                        quickFilter.openQuickFilterPopup();
                        quickFilter.hideSidebar();
                        quickFilter.closeQuickFilterPopup();
                    }

                    $('.nav-item input[type="checkbox"]').click(function(){
                        if($(this).prop("checked") == false){
                            var self = $(this);
                            var attr_value;
                            if (self.parent("label").hasClass("css_attribute_color")) {
                                attr_value = self.parent("label").siblings(".te_color-name").html();
                                if(attr_value) {
                                    attr_value = attr_value.toLowerCase();
                                    attr_value = attr_value.replace(/(^\s+|[^a-zA-Z0-9 ]+|\s+$)/g,"");
                                    attr_value = attr_value.replace(/\s+/g, "-");
                                }
                            } else {
                                attr_value = self.siblings("span").html();
                                if(attr_value) {
                                    attr_value = attr_value.toLowerCase();
                                    attr_value = attr_value.replace(/(^\s+|[^a-zA-Z0-9 ]+|\s+$)/g,"");
                                    attr_value = attr_value.replace(/\s+/g, "-");
                                }
                            }
                            $('.te_view_all_filter_div .te_view_all_filter_inner').find('.te_clear_attr_a.'+attr_value).trigger('click');
                        }
                    });

                    $( "select" ).change(function () {
                        $(this).find("option:selected").each(function() {
                            var attr_value = $(this).parents('.nav-item').find('.te_clear_all_variant').attr('attribute-name');
                            if(!$(this).text()) {
                                $('.te_view_all_filter_div .te_view_all_filter_inner').find('.te_clear_attr_a.'+attr_value).trigger('click');
                            }
                        });
                    });
                    /* Custom jquery scrollbar*/
                    if($('.te_product_sidebar_scrollbar').length){
//                        $(".js_attributes .nav-item ul.nav.nav-pills").mCustomScrollbar({
//                           axis:"y",
//                           theme:"dark-thin",
//                           alwaysShowScrollbar: 2
//                        });
                    }

                    $('.cus_theme_loader_layout').addClass('d-none');
                    $('#wrapwrap').removeClass('wrapwrap_trans');
                    if($('#id_lazyload').length) {
                        $("img.lazyload").lazyload();
                    }

                }
            });
        },
        _onClearAttribInd: function(event) {
            /* This method is inherit because check while remove the filtered attribute. And filter to ajax*/
            var self = event.currentTarget;
            var id = $(self).attr("data-id");
            if (id) {
                $("form.js_attributes option:selected[value=" + id + "]").remove();
                $("form.js_attributes").find("input[value=" + id + "]").removeAttr("checked");
            }
            this.filterData(event);
        },
        _onClearAttribAll: function(event) {
            /* This method is inherit because check while remove all the filtered attribute. And filter to ajax*/
            $("form.js_attributes select").val('');
            $("form.js_attributes").find("input:checked").removeAttr("checked");
            this.filterData(event);
        },
        _onClearAttribDiv: function(event) {
            /* This method is inherit to clear attribute div */
            var attr_name = $(event.currentTarget).attr('attribute-name');
            if($('.te_view_all_filter_inner').find(".te_clear_attr_a").hasClass(attr_name)) {
                $('.te_view_all_filter_div .te_view_all_filter_inner').find('.te_clear_attr_a.'+attr_name).trigger('click');
            }
            var self = event.currentTarget;
            var curent_div = $(self).parents("li.nav-item");
            var curr_divinput = $(curent_div).find("input:checked");
            var curr_divselect = $(curent_div).find("option:selected");
            _.each(curr_divselect, function(event) {
                $(curr_divselect).remove();
            });
            _.each(curr_divinput, function(event) {
                $(curr_divinput).removeAttr("checked");
            });
            this.filterData(event);
        },
    });
});