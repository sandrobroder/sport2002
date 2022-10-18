/**************************************************
        01. Search in Header
        02. Page Scroll up
        03. Theme Wishlist
        04. Shop Events
        05. cart Popover
        06. Theme layout
        07. Compare short name
**************************************************/
odoo.define('theme_clarico_vega.theme_script', function(require) {
    'use strict';

    var sAnimations = require('website.content.snippets.animation');
    var publicWidget = require('web.public.widget');
    var Widget = require('web.Widget');
    var core = require('web.core');
    var qweb = core.qweb;
    var _t = core._t
    var ajax = require('web.ajax');
    var config = require('web.config');
    var sale = new sAnimations.registry.WebsiteSale();

    //------------------------------------------
    // 01. Search in Header
    //------------------------------------------
    publicWidget.registry.productsSearchBar.include ({
        xmlDependencies: (publicWidget.registry.productsSearchBar.prototype.xmlDependencies || []).concat(['/emipro_theme_base/static/src/xml/advanced_search.xml']),
         _onKeydown: function (ev) {
            switch (ev.which) {
                case $.ui.keyCode.UP:
                case $.ui.keyCode.DOWN:
                    ev.preventDefault();
                    if (this.$menu) {
                         let $element = ev.which === $.ui.keyCode.UP ? this.$menu.children('.dropdown-item').last() : this.$menu.children('.categ_search').length ? this.$menu.find('.categ_search .dropdown-item:nth-child(2)'): this.$menu.children('.dropdown-item').first();
                        $element.focus();
                    }
                    break;
            }
            this._super.apply(this, arguments);
        },
        _render: function (res) {
        var $prevMenu = this.$menu;
        this.$el.toggleClass('dropdown show', !!res);
        if (res) {
            var products = res['products'];
            const categories = res['categories'];
            const quickLink = res['is_quick_link'];
            this.$menu = $(qweb.render('website_sale.productsSearchBar.autocomplete', {
                products: products,
                categories: categories,
                quickLink: quickLink,
                hasMoreProducts: products.length < res['products_count'],
                currency: res['currency'],
                widget: this,
            }));
            this.$menu.css('min-width', this.autocompleteMinWidth);
            this.$el.append(this.$menu);
        }
        if ($prevMenu) {
            $prevMenu.remove();
        }
    },
    });
    sAnimations.registry.themeSearch = sAnimations.Class.extend({
        selector: '#wrapwrap',
        read_events: {
            'click .te_srch_icon': '_onSearchClickOpen',
            'keyup input[name="search"]': '_onSearchClickData',
            'click .te_srch_close': '_onSearchClickClose',
            'click .te_srch_close_ept':'_onSearchClickCloseEpt',
            'click .mycart-popover .js_delete_product': '_onClickDeleteProduct',
            'submit form[action="/shop"].o_wsale_products_searchbar_form': '_onSearchSubmit'
        },
        start: function() {
            $('.variant_attribute  .list-inline-item').find('.active').parent().addClass('active_li');
            $( ".list-inline-item .css_attribute_color" ).change(function(ev) {
                var $parent = $(ev.target).closest('.js_product');
                $parent.find('.css_attribute_color').parent('.list-inline-item').removeClass("active_li");
                $parent.find('.css_attribute_color').filter(':has(input:checked)').parent('.list-inline-item').addClass("active_li");
            });
            $(document).on('click', '.validate-sign-in', function(e){
                $('.quick_view_modal > .quick_close').trigger('click');
                $("#loginRegisterPopup").modal();
                var tab = $(e.currentTarget).attr('href');
                $('.nav-tabs a[href="'+tab+'"]').tab('show')
            });
            var input_val = $('input[name="search"]').val();
            if (input_val) {
                $('.te_srch_close_ept').css("display", "block");
            }
        },
        _onSearchSubmit: function(ev){
            var search = $(".oe_search_box").val();
            ajax.jsonRpc('/search_keyword_report', 'call', {'search': search}).then(function(data) {});
        },
        _onSearchClickCloseEpt:function(ev) {
            var params = new URLSearchParams(window.location.search);
            $('input[name="search"]').val('');
            const classExists = $('.te_searchform__body,.te_sub_search').length;
            if (classExists) {
                $('.te_srch_close_ept').css("display", "none");
            }
            else if (params.get('search')){
                $('button[type="submit"]').trigger('click');
            }
        },
        _onSearchClickData: function(ev) {
            var self = ev.currentTarget;
            var input_val = $('input[name="search"]').val();
            if (input_val) {
                $('.te_srch_close_ept').css("display", "block");
            }
        },
        _onSearchClickOpen: function(ev) {
            var self = ev.currentTarget;
            //style1
            if ($(".te_header_1_right").length) {
                $(".te_search_popover").addClass("visible");
                $(self).hide()
                $(".te_srch_close").show();
                setTimeout(function(){
                    $('.o_wsale_products_searchbar_form input[name="search"]').focus();
                }, 500);
            }
            //style 2 and 3 resp view
            if ($(window).width() < 768) {
                if ($(".te_header_style_2_right").length || $(".te_header_style_3_inner_first").length) {
                    $(".te_search_popover").addClass("visible");
                    $(self).hide()
                    $(".te_srch_close").show();
                    setTimeout(function(){
                        $('.o_wsale_products_searchbar_form input[name="search"]').focus();
                    }, 500);
                }
            }
            //style4
            if ($(".te_header_4_search").length) {
                $(".te_search_4_form").addClass("open_search");
                var $h_menu = $("#oe_main_menu_navbar").height();
                $(".te_search_4_form").css({
                    top: $h_menu + 0
                });
                setTimeout(function(){
                    $('.o_wsale_products_searchbar_form input[name="search"]').focus();
                }, 500);
            }
             //style5
            if ($("header.o_header_is_scrolled .te_searchform__popup").length) {
                $('header.o_header_is_scrolled').css({'transform':'none','transition':'none'});
                $(".te_searchform__popup").addClass("open");
                $(".te_srch_close").show();
                setTimeout(function(){
                    $('.o_wsale_products_searchbar_form input[name="search"]').focus();
                }, 500);
            }
            else{
                if ($(".te_searchform__popup").length) {
                    $(".te_searchform__popup").addClass("open");
                    $(".te_srch_close").show();
                    setTimeout(function(){
                        $('.o_wsale_products_searchbar_form input[name="search"]').focus();
                    }, 500);
                }
            }
            //style7 and style9
            if ($(".te_header_7_srch_icon, .te_header_9_srch_icon").length) {
                if($(window).width() <= 767){
                    if($('.te_header_9_srch_icon').length){
                        $('.navbar-expand-md .navbar-toggler, .te_header_9_srch_icon, header .navbar-brand').hide();
                    }
                    else{
                        $(".navbar-expand-md .navbar-toggler").hide();
                    }
                }
                if ($(window).width() <= 991) {
                    if($('.te_header_9_srch_icon').length){
                        $(".te_header_9_srch_icon, div#top_menu_collapse .navbar-nav, div#top_menu_collapse_clone .navbar-nav").hide();
                    }
                    else{
                        $(".navbar-expand-md .navbar-nav, .te_header_right_icon, .te_header_navbar label.label_checkbox, div#top_menu_collapse .navbar-nav").hide();
                    }
                }
                $(".te_header_search input").css("width","100%");
                setTimeout(function(){
                    if ($(window).width() >= 992) {
                        $(".te_header_right_icon").hide();
                        $(".navbar-expand-md .navbar-nav").hide();
                    }
                    $(".te_header_search_popover").fadeIn(200);
                }, 500);
                setTimeout(function(){
                    $('.o_wsale_products_searchbar_form input[name="search"]').focus();
                }, 500);
            }
            //style8
            if ($(".te_srch_icon_mobile_header").length) {
                setTimeout(function(){
                    $('.o_wsale_products_searchbar_form input[name="search"]').focus();
                }, 500);
                if ($(window).width() <= 767) {
                    $('.ept_mobi_toggler, a.navbar-brand.logo').hide();
                }
                if ($(window).width() <= 991) {
                    $(".te_header_8_search").addClass("active");
                    $(self).hide();
                    $('a.navbar-brand.logo').hide();
                    $(".te_srch_close").show();
                }
            }
            //style10
            if ($('.te_header_style_10_right').length) {
                $(".te_search_popover").addClass("visible");
                $(self).hide()
                $(".te_srch_close").css('display','block');
                setTimeout(function(){
                    $('.o_wsale_products_searchbar_form input[name="search"]').focus();
                }, 500);
            }
        },
        _onSearchClickClose: function(ev) {
            var self = ev.currentTarget;
            //style1
            if ($(".te_header_1_right").length || $('.te_header_style_10_right').length) {
                $(".te_search_popover").removeClass("visible");
                $(self).hide();
                $(".te_srch_icon").show();
            }
            //style 2 and 3 resp view
            if ($(window).width() < 768) {
                if ($(".te_header_style_2_right").length || $(".te_header_style_3_inner_first").length || $('.te_header_10_search').length) {
                    $(".te_search_popover").removeClass("visible");
                    $(self).hide();
                    $(".te_srch_icon").show();
                }
            }
            //style4
            if ($(".te_header_4_search").length) {
                $(".te_search_4_form").removeClass("open_search");
                $(".te_search_icon_4").css("display", "inline-block");
            }
            //style5
            if ($(".te_searchform__popup").length) {
                $(".te_searchform__popup").removeClass("open");
                $(".te_srch_icon").show();
            }
            //style7 and style9
            if ($(".te_header_7_srch_icon, .te_header_9_srch_icon").length) {
                $(".te_header_right_icon, .navbar-expand-md .navbar-nav").show();
                $(".te_header_search_popover").hide();
                $(".te_header_search_popover input").css("width", "0%");
                $(".te_srch_icon").css("display", "flex");
                if($(window).width() <= 767){
                    if($('.te_header_9_srch_icon').length){
                        $('.navbar-expand-md .navbar-toggler, .te_header_11_srch_icon, header .navbar-brand').fadeIn(300);
                    }
                    else{
                        $(".navbar-expand-md .navbar-toggler").fadeIn(300);
                    }
                }
                if ($(window).width() <= 991) {
                    if($('.te_header_9_srch_icon').length){
                        $("div#top_menu_collapse .navbar-nav, div#top_menu_collapse_clone .navbar-nav").fadeIn(400);
                    }
                    else{
                        $(".te_header_right_icon, .navbar-expand-md .navbar-nav, .te_header_navbar label.label_checkbox").fadeIn(400);
                    }
                }
            }
            //style8
            if ($(".te_srch_icon_mobile_header").length) {
                if ($(window).width() <= 767) {
                    $('.ept_mobi_toggler, a.navbar-brand.logo').show();
                }
                if ($(window).width() <= 991) {
                    $(".te_header_8_search").removeClass("active");
                    $(".te_srch_icon").show();
                    $('a.navbar-brand.logo').show();
                    $(".te_srch_close").hide();
                }
            }
        },
    });

    //------------------------------------------
    // 02. Page Scroll up
    //------------------------------------------
    sAnimations.registry.themeLayout = sAnimations.Class.extend({
        selector: '.o_footer',
        read_events: {
            'click .scrollup-div': '_onClickAnimate',
        },
        _onClickAnimate: function(ev) {
            $("html, body").animate({
                scrollTop: 0
            }, 1000);
        },
    });
    //------------------------------------------
    // 03. Theme Wishlist
    //------------------------------------------
    sAnimations.registry.themeWishlist = sAnimations.Class.extend({
        selector: '#o_comparelist_table',
        read_events: {
            'click .o_wish_rm': '_onRemoveClick',
            'click .o_wish_add' : '_onAddToCartClick',
        },
        _onAddToCartClick: function(ev) {
            if($('body').hasClass('editor_enable')){
                ev.stopImmediatePropagation();
                ev.preventDefault();
            }
        },
        _onRemoveClick: function(ev) {
            if($('body').hasClass('editor_enable')){
                ev.stopImmediatePropagation();
                ev.preventDefault();
            } else{
                var ajax = require('web.ajax');
                var tr = $(ev.currentTarget).parents('tr');
                var wish = tr.data('wish-id');
                var route = '/shop/wishlist/remove/' + wish;
                ajax.jsonRpc(route, 'call', {
                    'wish': wish
                }).then(function(data) {
                    $(tr).hide();
                    if ($('.t_wish_table tr:visible').length == 0) {
                        window.location.href = '/shop';
                    }
                })
            }
        },

    });

    //------------------------------------------
    // 04. Shop Events
    //------------------------------------------
    sAnimations.registry.themeEvent = sAnimations.Class.extend({
        selector: '.oe_website_sale',
        read_events: {
            'click .te_attr_title': '_onAttribSection',
            'click .te_shop_filter_resp': '_onRespFilter',
            'click .te_filter_close': '_onFilterClose',
            'click .te_s_attr_color':'_oncolorattr',
            'click .te_show_category':'_onShowCategBtnResp',
            'click .te_show_option':'_onShowOptionBtnResp',
            'click .te_ctg_h4': '_onCategorySection',
            'keyup .js_attrib_search_ept': '_onKeyupAttribSearch',
            'click .js_attrib_search_span':'_onClickToSearch',
            'click .js_attrib_search_span i.fa-times':'_onClickToRemove',
        },
        start: function() {
            $("img.lazyload").lazyload();
            this.onShowClearVariant();
            this.onSelectAttribute();
            this._onslide();
            $(".color-changer").mCustomScrollbar({axis: "x",theme: "dark-thin",alwaysShowScrollbar: 0});
            $(".js_attributes li.nav-item").find('ul, select' ).css("display","block");
            $(".te_pricerange_content").show();
            $(".te_show_category").find('i').removeClass("fa-chevron-right").addClass("fa-chevron-down");
            $("#wsale_products_categories_collapse").find(".te_ctg_h4").addClass("te_fa-plus");
            /*if ($("#wsale_products_categories_collapse").find(".te_ctg_h4").hasClass('d-none')){
                  $("#wsale_products_categories_collapse").find(".te_ctg_h4").addClass("te_fa-plus");
            }*/
//            $("select.form-control").find(".open_select").css('display','block');
        },
        _onslide: function(){
            $('.js_attributes .main_attr').each(function (){
                if (this.getElementsByTagName('li').length > 6) {
                    $(this).find('ul').mCustomScrollbar({ axis: "y", theme: "dark-thin", alwaysShowScrollbar: 1});
                }
            });
        },
        onShowClearVariant: function() {
            $("form.js_attributes .te_shop_attr_ul input:checked, form.js_attributes .te_shop_attr_ul select").each(function() {
                var self = $(this);
                var type = ($(self).prop("tagName"));
                var type_value;
                var attr_value;
                var attr_value_str;
                var attr_name;
                var target_select;
                var curr_parent;
                var attr_title;
                var target_select = self.parents("li.nav-item").find("a.te_clear_all_variant");
                if ($(type).is("input")) {
                    type_value = this.value;
                    attr_value = $(this).parent("label").find("span").html();
                    if (attr_value) {
                        attr_value_str = attr_value.toLowerCase();
                        attr_value_str = attr_value_str.replace(/(^\s+|[^a-zA-Z0-9 ]+|\s+$)/g,"");
                        attr_value_str = attr_value_str.replace(/\s+/g, "-");
                    }
                    curr_parent = self.parents("ul");
                    target_select = curr_parent.parent("li.nav-item").find("a.te_clear_all_variant");
                    attr_name = curr_parent.parent("li.nav-item").find("a.te_clear_all_variant").attr('attribute-name');
                    attr_title = curr_parent.parent("li.nav-item").find("span")[0].innerText;   
                    if (self.parent("label").hasClass("css_attribute_color")) {
                        attr_value = self.parent("label").siblings(".te_color-name").html();
                        if(attr_value) {
                            attr_value_str = attr_value.toLowerCase();
                            attr_value_str = attr_value_str.replace(/(^\s+|[^a-zA-Z0-9 ]+|\s+$)/g,"");
                            attr_value_str = attr_value_str.replace(/\s+/g, "-");
                        }
                    }
                    var first_li = self.closest("ul").find("li").first();
                    var selected_li = self.closest("li.nav-item");
                    $(first_li).before(selected_li);
                    /*if (!curr_parent.hasClass("open_ul")) {
                        curr_parent.parent("li.nav-item").find('.te_attr_title').click();
                    }*/
                } else if ($(type).is("select")) {
                    type_value = self.find("option:selected").val();
                    attr_value = self.find("option:selected").html();
                    if(attr_value) {
                        attr_value_str = attr_value.toLowerCase();
                        attr_value_str = attr_value_str.replace(/(^\s+|[^a-zA-Z0-9 ]+|\s+$)/g,"");
                        attr_value_str = attr_value_str.replace(/\s+/g, "-");
                    }
                    attr_name = self.find("option:selected").parents("li.nav-item").find('a.te_clear_all_variant').attr('attribute-name');
                    target_select = self.parents("li.nav-item").find("a.te_clear_all_variant");
                    attr_title = self.find("option:selected").parents("li.nav-item").find("span")[0].innerText;
                }
                if (type_value) {
                    $(".te_product_filters, .te_clear_all_form_selection").css("display", "inline-block");
                    $(".te_view_all_filter_div").css("display", "inline-block");
                    if (target_select) {
                    var temp_attr_value = attr_value.toString().split('(');
                    var cust_attr_value = '';
                        switch(parseInt(temp_attr_value.length)) {
                          case 4:
                            cust_attr_value += temp_attr_value[0] +' ('+ temp_attr_value[1] +' ('+temp_attr_value[2];
                            break;
                          case 3:
                            cust_attr_value += temp_attr_value[0] +'('+ temp_attr_value[1];
                            break;
                          default:
                            cust_attr_value += temp_attr_value[0];
                        }
                        var last_attr_filter = $('.attr_filters').find('.attribute:not(.attr_val)').children().last().find('.attr_title').text();
                        if(last_attr_filter.indexOf(attr_title) != -1){
                            $(".te_view_all_filter_inner .attr_filters").append("<div class='attribute position-relative attr_val'>" + "<a data-id='" + type_value + "' class='te_clear_attr_a attr-remove "+attr_name+" "+attr_value_str+" '>"+ "<span class='position-relative'><span class='attr_value'>"+ cust_attr_value +"</span></span></a></div>");
                        }
                        else{
                            $(".te_view_all_filter_inner .attr_filters").append("<div class='attribute position-relative'>" + "<a data-id='" + type_value + "' class='te_clear_attr_a attr-remove "+attr_name+" "+attr_value_str+" '>"+ "<span class='attr_title'>" + attr_title +"</span> : <span class='position-relative'><span class='attr_value'>"+ cust_attr_value +"</span></span></a></div>");
                        }
                    }
                }
            });
            $("form.js_attributes input:checked, form.js_attributes select").each(function() {
                var self = $(this);
                var type = ($(self).prop("tagName"));
                var target_select = self.parents("li.nav-item").find("a.te_clear_all_variant");
                var type_value;
                if ($(type).is("input")) {
                    type_value = this.value;
                    var first_li = self.closest("ul").find("li").first();
                    var selected_li = self.closest("li.nav-item");
                    $(first_li).before(selected_li);
                } else if ($(type).is("select")) {
                    type_value = self.find("option:selected").val();
                }
                if (type_value) {
                    target_select.css("display", "inline-block");
                }
            });
        },

         _onKeyupAttribSearch : function(ev) {
            ev.preventDefault();
            $(ev.currentTarget).closest('ul').find('.no_found_msg').remove()
            var key = $(ev.currentTarget).val().toUpperCase()
            $(ev.currentTarget).closest('ul').find('.te_s_attr_val').each(function(){
                if ($(this).text().toUpperCase().indexOf(key) > -1) {
                    $(this).closest("li").removeClass('d-none');
                    $(ev.currentTarget).closest('ul').css('margin-bottom','0px');
                } else {
                    $(this).closest("li").addClass('d-none');
                }
            });
            if($(ev.currentTarget).closest('ul').children('li').not('.d-none').length == 0){
               $(ev.currentTarget).closest('ul').css('margin-bottom','20px');
               $(ev.currentTarget).closest('div').after('<div class="no_found_msg m-3 alert alert-danger">No result found ... </div>')
            }
         },
          _onClickToSearch : function(ev) {
            var hidden =  $(ev.currentTarget).parents('.js_attrib_search').find('.js_attrib_search_ept');
            hidden.animate({width: "toggle"});
            hidden.focus();
            $(ev.currentTarget).parents('.js_attrib_search').find(".js_attrib_search_span i").toggleClass("fa-search fa-times");
            if ( $(ev.currentTarget).parents('.js_attrib_search').find(".js_attrib_search_span i").hasClass('fa-times') ) {
                $(hidden).val('');
            }
         },
         _onClickToRemove : function(ev) {
            $(ev.currentTarget).closest('ul').find('.no_found_msg').remove();
            $(ev.currentTarget).closest('ul').find('.te_s_attr_val').closest("li").removeClass('d-none');
            $(ev.currentTarget).closest('ul').css('margin-bottom','0px');
         },

        // If any attribute are selected then automatically this section is Expand(only for type select)
        onSelectAttribute: function(ev){
            $("form.js_attributes .te_shop_attr_ul input:checked, form.js_attributes .te_shop_attr_ul select").each(function() {
                var self = $(this);
                var type = ($(self).prop("tagName"));
                var type_value;
                if ($(type).is("select")) {
                    type_value = self.find("option:selected").val();
                }
                if (type_value) {
                    self.addClass("open_select").css('display','inline-block');
                    self.siblings('.te_attr_title').addClass('te_fa-minus');
                }
            });
        },
        _onClearAttribInd: function(ev) {
            var self = ev.currentTarget;
            var id = $(self).attr("data-id");
            if (id) {
                $("form.js_attributes option:selected[value=" + id + "]").remove();
                $("form.js_attributes").find("input[value=" + id + "]").removeAttr("checked");
            }
            ajaxorformload(ev);
        },
        _onClearAttribAll: function(ev) {
            $("form.js_attributes option:selected").remove();
            $("form.js_attributes").find("input:checked").removeAttr("checked");
            ajaxorformload(ev);
        },
        _onClearAttribDiv: function(event) {
            /* This method is inherit to clear attribute div */
            var attr_name = $(event.currentTarget).attr('attribute-name');
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
        _onCategorySection: function(){
            var ctg_ul = $('.te_ctg_h4').siblings('.te_shop_ctg_list');
             if (ctg_ul.hasClass("open_ul")) {
                ctg_ul.removeClass("open_ul");
                ctg_ul.siblings(".te_ctg_h4").removeClass('te_fa-plus');
                ctg_ul.toggle('slow');
            }
            else{
                ctg_ul.addClass("open_ul");
                ctg_ul.siblings(".te_ctg_h4").addClass('te_fa-plus');
                ctg_ul.toggle('slow');
            }
        },
        _onAttribSection: function(ev) {
            var self = ev.currentTarget;
            var main_li = $(self).parents("li.nav-item");
            var ul_H = main_li.find("ul").height();
            if (main_li.find("select").length == 1) {
                $("select.form-control.open_select").css('display','block');
                var main_select = main_li.find("select");
                if (main_select.hasClass("open_select")) {
                    main_select.removeClass("open_select");
                    main_select.parent(".nav-item").find(".te_attr_title").removeClass('te_fa-minus');
                    main_select.toggle('slow');
                }
                else {
                    main_select.addClass("open_select");
                    main_select.parent(".nav-item").find(".te_attr_title").addClass('te_fa-minus');
                    main_select.toggle('slow');
                }
            }
            var main_ul = main_li.find("ul");

            if (main_ul.hasClass("open_ul")) {
                main_ul.removeClass("open_ul");
                $(main_ul).parent('.nav-item').find(".te_attr_title").removeClass('te_fa-minus');
                main_ul.toggle('slow');

            } else {
                main_ul.addClass("open_ul");
                $(main_ul).parent('.nav-item').find(".te_attr_title").addClass('te_fa-minus');
                main_ul.toggle('slow');
            }
        },
        _onRespFilter: function(ev) {
            $("#products_grid_before").addClass("te_filter_slide");
            $("#products_grid_before").mCustomScrollbar({
               axis:"y",
               theme:"dark-thin",
               alwaysShowScrollbar: 1
            });
            if($('.o_wsale_products_main_row').hasClass('filter_sidebar')) {
                $("#wrapwrap").addClass("wrapwrap_sidebar");
            }
            $("#wrapwrap").addClass("wrapwrap_trans");
            $('body').css("overflow-x", "hidden");
            $("#wsale_products_attributes_collapse").addClass("show");
//            $(".te_show_category").find("i").removeClass("fa-chevron-right")
            if($('#products_grid_before').find('#wsale_products_attributes_collapse').length < 1) {
                $("#wsale_products_categories_collapse").addClass("show");
                if($("#wsale_products_categories_collapse .show")){
                    $(".te_show_category").find("i").addClass('fa-chevron-down').removeClass('fa-chevron-up');
                }
            }
            if($("#wsale_products_attributes_collapse .show")){
                $(".te_show_option").find("i").addClass('fa-chevron-up').removeClass('fa-chevron-down');
            }
        },
        _onFilterClose: function(ev) {
            $("#products_grid_before").removeClass("te_filter_slide")
            $("#wrapwrap").removeClass("wrapwrap_trans");
        },
        _oncolorattr: function(ev){
            var self=ev.currentTarget;
            $(self).find("input").click();
        },
         _onShowCategBtnResp: function(ev){
//            $(".te_show_category").find("i").toggleClass('fa-chevron-up fa-chevron-down');
                $(".te_show_category collapsed").find("i").removeClass('fa-chevron-right');
//                $(ev.currentTarget).find("i").addClass('fa-chevron-up');
                if($(ev.currentTarget).find("i").hasClass('fa-chevron-up')){
                    $(ev.currentTarget).find("i").addClass('fa-chevron-down').removeClass('fa-chevron-up');
                }
                else{
                    $(ev.currentTarget).find("i").addClass('fa-chevron-up').removeClass('fa-chevron-down');
                }

            },
        _onShowOptionBtnResp: function(ev){
            console.log('_onShowOptionBtnResp')
//            $(".te_show_option").find("i").toggleClass('fa-chevron-down fa-chevron-up');
               if($(ev.currentTarget).find("i").hasClass('fa-chevron-down')){
                $(ev.currentTarget).find("i").addClass('fa-chevron-up').removeClass('fa-chevron-down');
            }
            else{
                $(ev.currentTarget).find("i").addClass('fa-chevron-down').removeClass('fa-chevron-up');
            }
        },
    });

    sAnimations.registry.StickyFilter = sAnimations.Animation.extend({
        selector: '#wrapwrap',
         effects: [{
            startEvents: 'scroll',
            update: '_stickyFilter',
        }],
        init: function () {
            this._super(...arguments);
            this.header_height = 20;
            this.scrolledPoint = 250;
            if($('header').hasClass('o_header_fixed')) {
                this.scrolledPoint = 50;
            }
            if($('header#top').length && !$('header').hasClass('o_header_sidebar')) {
                if($('header nav').hasClass('te_header_navbar')) {
                    this.header_height = $('header nav').height() + 20;
                } else {
                    this.header_height = $('header').height() + 20;
                }
                if($('header nav').hasClass('header10')) {
                    this.header_height = $('header nav').height() - 60;
                }
            }
            if($( window ).width() < 992 || $('.te_shop_filter_resp').hasClass('show')) {
                this.header_height = $('header').height() + 50;
                var $stickyFilter = $('.te_shop_filter_resp');
                if (!!$stickyFilter.offset()) {
                    this.stickyTop = $('div.te_shop_filter_resp').offset().top;
                    this.footerTop = $('footer').offset().top - 300;
                }
            }
        },
        _stickyFilter: function (scroll) {
            if($( window ).width() > 991 && !$('.o_wsale_products_main_row').hasClass('filter_sidebar')) {
                if($('.o_wsale_products_main_row').hasClass('enabled')){
                    var $stickySidebar = $('.te_product_sticky_sidebar');
                    if (!!$stickySidebar.offset()) {
                        var sidebar_height = $stickySidebar.innerHeight();
                        var stickyTop = $stickySidebar.offset().top;
                        var windowHeight = $( window ).height() - 125;
                        var quickView = $('.te_quick_filter_dropdown_menu').is(":visible");
                        if(!quickView) {
                            if (scroll > this.scrolledPoint) {
                                $stickySidebar.css({ position: 'sticky', top: this.header_height, height: windowHeight});
                                $stickySidebar.addClass('sticky-media');
                                $("#products_grid_before").mCustomScrollbar({
                                   axis:"y",
                                   theme:"dark-thin",
                                   alwaysShowScrollbar: 1
                                });
                            } else {
                                $stickySidebar.css({ position: 'unset', top: 'initial', height: 'auto'});
                                $stickySidebar.removeClass('sticky-media');
                                $("#products_grid_before").mCustomScrollbar("destroy");
                            }
                        } else {
                            $stickySidebar.css({ position: 'unset', top: 'initial', height: 'auto'});
                            $stickySidebar.removeClass('sticky-media');
                            $("#products_grid_before").mCustomScrollbar("destroy");
                        }
                    }
                }
            }
            if($( window ).width() < 768) {
                var $stickyFilter = $('.te_shop_filter_resp');
                if (!!$stickyFilter.offset()) {
                    if ( (this.stickyTop < scroll) ) {
                        if ( $('.o_top_fixed_element').length ){
                            $('.te_shop_pager_top').css({ position: 'sticky', top: $('header').height(), display: 'flex', width: window.innerWidth, padding: '0px 15px', margin: '0px -15px', 'background-color': '#FFF', 'z-index': '8'});
                        }
                        else{
                            $('.te_shop_pager_top').css({position: 'relative', top: 'initial'});
                        }
                    } else {
                        $('.te_shop_pager_top').css({ position: 'relative', top: 'initial', width: window.innerWidth, display: 'flex', padding: '0px 15px', margin: '0px -15px', 'background-color': '#FFF', 'z-index':'8' });
                    }
                }
            }
            if($( window ).width() > 767 && $('.te_shop_filter_resp').hasClass('show')) {
                var footerPosition = $("main").height() - $("#footer").height();
                if ( (this.stickyTop < scroll) && scroll < footerPosition - 100) {
                    $('.te_shop_filter_resp').css({'position' : 'fixed', 'bottom' : '43%', 'left' : '0px', 'z-index' : '9999', 'box-shadow' : '6px 6px 5px 1px rgba(0,0,0,0.25)', 'background' : 'white'});
                    if($( window ).width() < 992){
                        $('.filters-title-ept').css({'display':'none'});
                        $('.te_shop_filter_resp').css({'width':'6%'});
                    }
                }
                else{
                    $('.te_shop_filter_resp').css({'position' : 'unset', 'bottom' : 'unset', 'left' : 'unset', 'z-index' : 'unset', 'box-shadow' : 'unset','width':'unset'});
                    $('.filters-title-ept').css({'display':'inline-block'});
//                    $('.te_shop_filter_resp').css({'width':'unset'});
                }

            }
        },
    });

    /** Animation of menu in responsive for header style 10 **/
    sAnimations.registry.responsiveHeader10 = sAnimations.Animation.extend({
        selector: '#wrapwrap',
        read_events: {
            'click .header_sidebar': '_headerSidebar',
            'click .close_top_menu': '_closeLeftHeader',
        },
        init: function () {
            this._super(...arguments);
            this.header_height = 0;
            if($('.o_main_navbar').length) {
                this.header_height = $('.o_main_navbar').height();
            }
        },
        _headerSidebar: function() {
            $("#top_menu_collapse").addClass("header_menu_slide").css('top',this.header_height).show('slow');
            $("#top_menu_collapse").animate({
                width: '100%'
            });
            $("#wrapwrap").addClass("wrapwrap_trans_header");
        },
        _closeLeftHeader: function() {
            $("#top_menu_collapse").animate({
                width: '0'
            });
            $("#wrapwrap").removeClass("wrapwrap_trans_header");
        }
    });

    sAnimations.registry.StickyGallery = sAnimations.Animation.extend({
        selector: '#wrapwrap',
         effects: [{
            startEvents: 'scroll',
            update: '_stickyGallery',
        }],
        read_events: {
            'click .product_details_sticky .prod_add_cart .te_add_to_cart': '_onClickCart',
            'click .product_details_sticky .prod_add_cart .te_buy_now': '_onClickBuyNow',
        },
        init: function () {
            this._super(...arguments);
            this.$sticky = $('#product_detail .row.te_row_main > .col-lg-6:first-child');
            if ($(this.$sticky).length) {
                this.stickyTop = this.$sticky.offset().top;
            }
            this.header_height = 20;
            if($('header#top').length && !$('header').hasClass('o_header_sidebar')) {
                if($('header nav').hasClass('te_header_navbar')) {
                    this.header_height = $('header nav').height() + 20;
                } else {
                    this.header_height = $('header').height() + 20;
                }
                if($('header nav').hasClass('header10')) {
                    this.header_height = $('header nav').height() - 60;
                }
            }
        },
        _stickyGallery: function (scroll) {
            if($( window ).width() > 991) {
                if (!!this.$sticky.offset() && this.$sticky) {
                    if (this.stickyTop < scroll+this.header_height+this.header_height) {
                        this.$sticky.css({ position: 'sticky', top: this.header_height });
                        this.$sticky.addClass('sticky-media');
                    } else {
                        this.$sticky.css({ position: 'relative', top: 'initial'});
                        this.$sticky.removeClass('sticky-media');
                    }
                }
            }
            // Sticky add to cart bar
            if($('.product_details_sticky').length){
                if($('div#product_details a#add_to_cart').length){
                    var getPriceHtml = $('div#product_details .product_price').html();
                    var stickHeight = $('.product_details_sticky .prod_details_sticky_div').height();
                    var btnHeight = $('div#wrapwrap .product_details_sticky').height();
                    var cookie_height = 0;
                    if($('.o_cookies_discrete .s_popup_size_full').length) {
                       cookie_height = $('.s_popup_size_full .modal-content').height()
                       stickHeight = cookie_height + stickHeight
                    }
                    var fixIconHeight8 = $('.te_header_icon_right').height();
                    var fixIconHeight9 = $('.head_9_rest_icons').height();
                    var footerPosition = $("main").height() - $("#footer").height();
                    if ( scroll > $('div#product_details a#add_to_cart').offset().top && scroll < footerPosition - 200 ) {
                            if ($(window).width() >= 768){
                                $('div#wrapwrap .product_details_sticky').css('bottom', cookie_height+'px');
                                $('div#wrapwrap .product_details_sticky').fadeIn();
                                $('#product_detail').find('.o_product_feature_panel').css('bottom',stickHeight+'px').fadeIn();
                            }
                            /* Display prices on add to cart sticky*/
                            if( $( ".js_product.js_main_product" ).hasClass( "css_not_available" )){
                               $('div#wrapwrap .prod_price').html('');
                            }
                            else{
                                $('div#wrapwrap .prod_price').html(getPriceHtml);
                            }
                            /* Ipad view only */
                            if ( $(window).width() >= 768 && $(window).width() <= 991 ){
                                stickyMobileDevice(fixIconHeight8, fixIconHeight9, btnHeight, cookie_height);
                            }
                    } else {
                        if ($(window).width() >= 768){
                            $('#product_detail').find('.o_product_feature_panel').css('bottom', '0px');
                            $('div#wrapwrap .product_details_sticky').css('bottom', cookie_height+'px');
                            $('div#wrapwrap .product_details_sticky').fadeOut();
                        }
                        if ( $(window).width() >= 768 && $(window).width() <= 991 ){
                            chatBtn(fixIconHeight8, fixIconHeight9, btnHeight, cookie_height);
                        }
                    }
                    /* Mobile view sticky add to cart */
                    if ($(window).width() <= 767){
                        var relativeBtn = $(".relative_position_cart").offset().top - $("main").offset().top;
                        if (relativeBtn > scroll) {
                            stickyMobileDevice(fixIconHeight8, fixIconHeight9, btnHeight, cookie_height);
                        }
                        else {
                            $('div#wrapwrap .product_details_sticky').fadeOut();
                            chatBtn(fixIconHeight8, fixIconHeight9, btnHeight, cookie_height);
                        }
                    }
                }
                /* Sticky Add To Cart *//*
                $(".product_details_sticky .prod_add_cart #add_to_cart").click(function(e){
                    if($('body').hasClass('editor_enable')){
                        e.stopPropagation();
                    }
                    else{
                        $("div#product_details .js_product.js_main_product #add_to_cart").trigger( "click" );
                        return false;
                    }
                });
                *//* Sticky Buy Now *//*
                $(".product_details_sticky .prod_add_cart #buy_now").click(function(e){
                    if($('body').hasClass('editor_enable')){
                        e.stopPropagation();
                    }
                    else{
                        $("div#product_details .js_product.js_main_product #buy_now").trigger( "click" );
                        return false;
                    }
                });*/
            }
            /* Live Chat button */
            if( !$('div#product_details a#add_to_cart').length ){
                if ($(window).width() <= 991){
                     var fixIconHeight8 = $('.te_header_icon_right').height();
                     var fixIconHeight9 = $('.head_9_rest_icons').height();
                     if( $(fixIconHeight8).length ){
                        $('.openerp.o_livechat_button').css({'bottom': fixIconHeight8+'px'});
                     }
                     else if( $(fixIconHeight9).length ){
                        $('.openerp.o_livechat_button').css({'bottom': fixIconHeight9+'px'});
                     }
                     else{
                        $('.openerp.o_livechat_button').css({'bottom': '0px'});
                     }
                }
            }

            var HHeight = $('header#top').height();
            if (scroll >= 72) {
                $('body').addClass('fixed-header-bar');
            } else {
                $('body').removeClass('fixed-header-bar');
            }
            /* For Header 11 scroll top*/
            if (scroll >= 44) {
                $('body').addClass('fixed-header-top-bar');
            } else {
                $('body').removeClass('fixed-header-top-bar');
            }
            if($('#wrapwrap').hasClass('homepage')){
                $('#wrapwrap').addClass('header_top_overlay');
                $('#wrapwrap:not(.header_top_overlay)').css("margin-top", HHeight);
                if (scroll >= 196) {
                    $('body').addClass('fixed-header');
                } else {
                    $('body').removeClass('fixed-header');
                }
            }
            if ($('.te_header_navbar_8').length) {
                var headerHeight = $('.te_header_navbar_8').height();
                if (scroll > headerHeight) {
                    $('body').addClass('fixed-header-8-bar');
                    $('.te_header_navbar_8').addClass('start-sticky');
                } else {
                    $('body').removeClass('fixed-header-8-bar');
                    $('.te_header_navbar_8').removeClass('start-sticky');
                }
            }
            /* Prevent search bar while scrolling header */
            if($('.navbar-light.navbar-expand-lg').length){
                /* odoo default header search */
                if ($("header .te_searchform__popup.open").length) {
                    $('header').css({'transform':'none','transition':'none'});
                }
            }
            if ($('.te_header_navbar').length) {
                var headerHeight = $('.te_header_navbar').height();
                if ( scroll > headerHeight ) {
                    if($('header').hasClass('o_header_affixed') && !$("header.o_header_affixed").hasClass("o_header_is_scrolled")){
                      if ($(".te_header_1_right").length) {
                          $(".te_search_popover").removeClass("visible");
                          $('.te_srch_close').hide();
                          $(".te_srch_icon").show();
                      }
                      if ($(window).width() < 768) {
                         if ($(".te_header_style_2_right").length || $(".te_header_style_3_inner_first").length) {
                             $(".te_search_popover").removeClass("visible");
                             $('.te_srch_close').hide();
                             $(".te_srch_icon").show();
                         }
                      }
                      if ($(".te_header_4_search").length) {
                          $(".te_search_4_form").removeClass("open_search");
                          $(".te_search_icon_4").css("display", "inline-block");
                      }
                      if($(".te_searchform__popup").length){
                         $(".te_searchform__popup").removeClass("open");
                         $(".te_srch_icon").show();
                      }
                      $(".search_btn_close").trigger('click');
                      $('.o_wsale_products_searchbar_form .dropdown-menu.show').removeClass('show');
                    }
                }
            }
        },
        _onClickCart: function(e) {
            if($('body').hasClass('editor_enable')){
                e.stopPropagation();
            }
            else{
                var $form = $('#product_details .js_main_product #add_to_cart').closest('form')
                sale._handleAdd($form);
                return false;
            }
        },
        _onClickBuyNow: function(e) {
            if($('body').hasClass('editor_enable')){
                e.stopPropagation();
            }
            else{
                var $form = $('#product_details .js_main_product #buy_now').closest('form')
                sale._onClickAdd(e)
            }
        }
    });
    //function for manage sticky add to cart with live chat button
    function stickyMobileDevice(h8, h9, btnHeight, cookie_height){
        if( $(h8).length ){
            $('div#wrapwrap .product_details_sticky').css({'display':'block', 'position':'fixed', 'bottom': h8+'px', 'top':'initial'});
            $('.openerp.o_livechat_button').css({'bottom': (h8 + btnHeight) +'px'});
        }
        else if( $(h9).length ){
            $('div#wrapwrap .product_details_sticky').css({'display':'block', 'position':'fixed', 'bottom': h9+'px', 'top':'initial'});
            $('.openerp.o_livechat_button').css({'bottom': (h9 + btnHeight) +'px'});
        }
        else{
            $('div#wrapwrap .product_details_sticky').css({'display':'block', 'position':'fixed', 'bottom': cookie_height+'px', 'top':'initial'});
            $('.openerp.o_livechat_button').css({'bottom': btnHeight+'px'});
        }
    }
    //function for manage live chat button
    function chatBtn(h8, h9, btnHeight, cookie_height){
        if( $(h8).length ){
            $('.openerp.o_livechat_button').css({'bottom': h8+'px'});
        }
        else if( $(h9).length ){
            $('.openerp.o_livechat_button').css({'bottom': h9+'px'});
        }
        else{
            if (cookie_height){
                $('.openerp.o_livechat_button').css({'bottom': cookie_height+'px'});
            }
            else{
                $('.openerp.o_livechat_button').css({'bottom': '0px'});
            }
        }
    }
    /*---- Shop Functions ------*/
    //function for ajax form load
    function ajaxorformload(ev) {
        var ajax_load = $(".ajax_loading").val();
        if (ajax_load == 'True') {
            ajaxform(ev);
        } else {
            $("form.js_attributes input,form.js_attributes select").closest("form").submit();
        }
    }
    sAnimations.registry.WebsiteSale.include({
        /*
         Adds the stock checking to the regular _onChangeCombination method
        @override
        */
        _updateProductImage: function (){

        this._super.apply(this, arguments);
        },
    });

    /** Product image gallery for product page */
    sAnimations.registry.product_detail = sAnimations.Class.extend({
        selector: "#product_detail",
        productGallery: function(){
            /* Remove compare duplicate class div*/
            setTimeout(function(){
                if($('.quick_view_modal').length){
                    $('.modal-body.oe_website_sale > .o_product_feature_panel').remove();
                }
            }, 500);
            var owl_rtl = false;
            if ($('#wrapwrap').hasClass('o_rtl')) {
                owl_rtl = true;
            }
            var slider = $('#mainSlider .owl-carousel');
            var thumbnailSlider = $('#thumbnailSlider .owl-carousel');
            $('#thumbnailSlider').show();
            var duration = 400;
            var img_length = $('#len-ept-image').val();

            if($('#len-ept-image').val() < 2) {
                $('#mainSlider').addClass('mainslider-full');
            }

            if($('#len-ept-image').val() > 5) {
                var slider_length = ($('#len-ept-image').val() - 2);
                var thumb_length =  $('#len-ept-image').val() - ($('#len-ept-image').val() - 5);
            } else {
                var slider_length = 0;
                var thumb_length = 0;
            }
            slider.owlCarousel({
                nav:true,
                rtl: owl_rtl,
                navText : ['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>'],
                items:1,
                loop: $('#len-ept-image').val() > 1 ? true : false,
                rewind: true,
                responsive:{
                    768:{
                        dots: false,
                    },
                    767:{
                        dots: true,
                    },
                }
            }).on('changed.owl.carousel', function (event) {
                // On change of main item to trigger thumbnail item
                let currentIndex = event.item.index + slider_length;
                thumbnailSlider.trigger('to.owl.carousel', [currentIndex, duration, true]);
                if($('#len-ept-image').val() <= 5) {
                    thumbnailSlider.find('.owl-item').removeClass('center');
                    thumbnailSlider.find('.owl-item').eq(currentIndex - 2).addClass('center');
                }
                $("#mainSlider img").each(function() {
                    $(this).attr('loading','');
                })
            }).on('refreshed.owl.carousel', function () {
                if($('#id_lazyload').length) {
                    $("img.lazyload").lazyload();
                }
            });;

            // carousel function for thumbnail slider
                thumbnailSlider.owlCarousel({
                    loop: $('#len-ept-image').val() > 5 ? true : false,
                    center: $('#len-ept-image').val() > 5 ? true : false,
                    margin: 4,
                    rtl: owl_rtl,
                    nav:true,
                    dots: true,
                    navText : ['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>'],
                    responsive:{
                        0:{
                            items:5,
                        },
                        600:{
                            items:5
                        },
                        1000:{
                            items:5
                        }
                    }
                }).on('click', '.owl-item', function () {
                    // On click of thumbnail items to trigger same main item
                    let currentIndex = $(this).find('li').attr('data-slide-to');
                    slider.trigger('to.owl.carousel', [currentIndex, duration, true]);
                }).on('refreshed.owl.carousel', function () {
                    if($('#len-ept-image').val() <= 5) {
                        $('#thumbnailSlider .owl-carousel .owl-item').first().addClass('center');
                    }
                    if($('#id_lazyload').length) {
                        $("img.lazyload").lazyload();
                    }
                });
            var thumb_width = $('#thumbnailSlider').find('.owl-item').width();
            $('#thumbnailSlider').find('.owl-item').height(thumb_width);
            if ($(window).width() > 767) {
                if($('.o_rtl').length == 1){
                    $('#thumbnailSlider').find('.owl-carousel').css('right', (0-(thumb_width*2)));
                }
                $('#thumbnailSlider').find('.owl-carousel').css('left', (0-(thumb_width*2)));
                $('#thumbnailSlider').find('.owl-carousel').css('top', (thumb_width*2)+26);
            }
        },
    });

    //------------------------------------------
    // 06. Theme layout
    //------------------------------------------

    $(document).ready(function($) {

        /* Multi tab style 5 */
        var tabs = $('[data-class="style5"]');
        $(tabs).each(function(){
            if ( $(this).find('.active').length == 0 ){
               $(this).find('li').first().children('a').addClass('active');
               var activeFirstItem = $(this).find('.active');
               var activeItemWidth = activeFirstItem.innerWidth();
               var activeItemHeight = activeFirstItem.innerHeight();
               $(this).find(".tab_selector").css({
                    "left": 0 + "px",
                    "width": activeItemWidth + "px",
                    "height": activeItemHeight + "px",
                    "top": activeFirstItem.position.top + "px"
               });
            }
            else {
               var activeItem = $(this).find('.active');
               var activeWidth = activeItem.innerWidth();
               var activeHeight = activeItem.innerHeight();
               $(this).find(".tab_selector").css({
                 "left": activeItem.position.left + "px",
                 "width": activeWidth + "px",
                 "height": activeHeight + "px",
                 "top": activeItem.position.top + "px"
               });
            }
            $(this).find("li.nav-item").css({'width':'auto;'});
            $(this).find("li.nav-item a").css({'height':'auto;'});
        });
        var getItemHeight = tabs.find('li.nav-item').innerHeight();
        var getItemWidth = tabs.find('li.nav-item').innerWidth();
		tabs.find('.tab_selector').css({'height': getItemHeight});
		tabs.find('.tab_selector').css({'width': getItemWidth});

        $('[data-class="style5"] a').on("click", function(e){
              e.preventDefault();
              var activeWidth = $(this).innerWidth();
              var activeHeight = $(this).innerHeight();
              var itemPos = $(this).position();
              $(this).parents('[data-class="style5"]').find(".tab_selector").css({
                "left":itemPos.left + "px",
                "width": activeWidth + "px",
                "height": activeHeight + "px",
                "top": itemPos.top + "px"
              });
        });
        /* Multi tab style 6 active parent */
        if( $('[data-class="style6"] li.nav-item').hasClass('active') == 0 ){
            $('[data-class="style6"] li.nav-item').first().addClass('active');
        }
        else{
            $('[data-class="style6"]').find("a.nav-link.active").closest("li.nav-item").addClass('active');
        }
        $('[data-class="style6"] a').on("click", function(){
            $('[data-class="style6"]').find("li.nav-item").removeClass('active');
            $(this).closest("li.nav-item").addClass('active');
        });

        var parentTab = $('.nav[data-class="style6"]');
        if (parentTab){
            var numItems = parentTab.find('li').length;
            if (numItems == 12) {
               parentTab.find("li.nav-item").width("8.3%");
            }
            else if (numItems == 11) {
              parentTab.find("li.nav-item").width("9%");
            }
            else if (numItems == 10) {
              parentTab.find("li.nav-item").width("10%");
            }
            else if (numItems == 9) {
              parentTab.find("li.nav-item").width("11.1%");
            }
            else if (numItems == 8) {
              parentTab.find("li.nav-item").width("12.5%");
            }
            else if (numItems == 7) {
              parentTab.find("li.nav-item").width("14.2%");
            }
            else if (numItems == 6) {
              parentTab.find("li.nav-item").width("16.666666666666667%");
            }
            else if (numItems == 5) {
              parentTab.find("li.nav-item").width("20%");
            }
            else if (numItems == 4) {
              parentTab.find("li.nav-item").width("25%");
            }
            else if (numItems == 3) {
              parentTab.find("li.nav-item").width("33.3%");
            }
            else if (numItems == 2) {
              parentTab.find("li.nav-item").width("50%");
            }
            else{
                parentTab.find("li.nav-item").width("auto");
            }
        }

        $('[data-class="style6"]').each(function () {
            var highestBox = 0;
            $( $(this).find('li a') ).each(function () {
                if ($(this).height() > highestBox){
                   highestBox = $(this).height();
                }
            });
            $($(this).find('li a')).height(highestBox);
        });

        $(document).on('click',".te_quick_filter_dropdown",function(ev) {
            $(".te_quick_filter_dropdown_menu .te_quick_filter_ul >li").each(function() {
                var ul_H = $(this).find("ul").height();
                if (ul_H >= 177) {

                    $(this).find("ul").mCustomScrollbar({
                        axis:"y",
                        theme:"dark-thin",
                        alwaysShowScrollbar: 1,
                    });
                }
            });
        });
        $(document).on('click',".quick_close",function(ev) {
            $(".ajax_cart_model .modal-body").html("");
            $('.modal-backdrop').remove();
            $('body').css("padding-right","0");
        });
        $(document).on('click',".cart_close",function(ev) {
            $('.modal-backdrop').remove();
            $('body').css("padding-right","0");
        });
        $(document).mouseup(function(ev)
		{
		    var container = $(".quick_view_modal");
		    if (!container.is(ev.target) && container.has(ev.target).length === 0)
		    {
		        if($('#quick_view_model_shop').hasClass("show")){
		            $('.modal-backdrop').remove();
                    $('body').css("padding-right","0");
                }
		    }
		});
        if($(document).find('.te_recently_viewed'))
        {
            var r_name = $("#te_rect_cnt").text();
            $('.te_recently_viewed').find('h6').each(function(){

                $(document).find('h6.card-title').addClass("te_rect_name")
                if(r_name == 2)
                {
                    $('h6.card-title').addClass('te_2_line');
                }
                if(r_name == 3)
                {
                    $('h6.card-title').addClass('te_3_line');
                }
            });
        }
        if($('.o_comparelist_button')) {
            setTimeout(function(){
                $('.o_comparelist_button').find('a').addClass('te_theme_button');
            }, 700);
        }
        setTimeout(function(){
            $(".o_portal_chatter_composer_form").find("button").addClass("te_theme_button");
            $(".js_subscribe_btn").addClass("te_theme_button");
            $(".o_portal_sign_submit").addClass("te_theme_button");
        }, 1000);

        /*var mainHeight = $('#wrapwrap > main').height() + 250;
        if (mainHeight) {
            //$('#wrapwrap > main').css("min-height", mainHeight);
        }*/

        //extra menu dropdown
        $('.o_extra_menu_items .dropdown-menu').css("display", "none")
        $('li.o_extra_menu_items .dropdown').click(function(event) {
            event.stopImmediatePropagation();
            $(this).find(".dropdown-menu").slideToggle();
        });
        if ($(window).width() <= 1200) {
            $(".te_dynamic_ept >a").append('<span class = "fa fa-chevron-down te_icon" />');
	        $('.te_icon').attr('data-toggle', 'true');
            $('.te_icon').attr('aria-expanded', 'true');
	        $(document).on('click',"span.te_icon",function(ev) {
	        	if( $(ev.target).is('.te_icon') ) {
			       	ev.preventDefault();
					$(this).parent("a").siblings('.te_custom_submenu').slideDown('slow');
					$(this).addClass('te_icon_ctg');
	        	}
	        });
	        $(document).mouseup(function(e)
			{
			    var container = $(".te_dynamic_ept");
			    if (!container.is(e.target) && container.has(e.target).length === 0)
			    {
			        $('.te_icon').parent("a").siblings('.te_custom_submenu').slideUp('slow');
			    }
			});
            $(document).keyup(function(e) {
                 if (e.keyCode == 27) {
                    $('.te_icon').parent("a").siblings('.te_custom_submenu').slideUp('slow');
                 }
            })
        	$(document).on('click',"span.te_icon_ctg",function(ev) {
        		$(this).parent("a").siblings('.te_custom_submenu').slideUp('slow');
        		$(this).removeClass('te_icon_ctg');
        	});
        	$(document).on('click',".ctg_arrow",function(ev) {
		        $(this).toggleClass('te_down_ctg_icon');
				if($(this).hasClass('te_down_ctg_icon'))
				{
				    ev.preventDefault();
				    $(this).siblings("ul#custom_recursive").slideDown('slow');
				    return false;
				}
				else
				{
		            $(this).siblings("ul#custom_recursive").slideUp('slow');
			    }
			});
        }
        //Changed search form action in theme's search when website search is installed
        if ($("body").find(".website_search_form_main").length > 0) {
            $(".te_header_search,.te_searchform__popup").each(function() {
                $(this).find("form").attr("action", "/search-result");
            })
            $(".website_search_form_main").html("");
        }
        //Recently viewed title
        if ($('#carousel_recently_view .carousel-inner .img_hover').length >= 1) {
            $('.te_product_recent_h2').css('display', 'block')
        }
        //expertise progress bar
        $('.progress').each(function() {
            var area_val = $(this).find('.progress-bar').attr("aria-valuenow")
            $(this).find('.progress-bar').css("max-width", area_val + "%")
        })
        //Remove images in extra menu
        $("li.o_extra_menu_items").find("img").removeAttr("src alt");

        // if slider then active first slide
        if ($('.recommended_product_slider_main').length) {
            $(".theme_carousel_common").each(function() {
                $(this).find(".carousel-item").first().addClass("active");
            })
        }
        // Change in carousel to display two slide
        $('.theme_carousel_common .carousel-item').each(function() {
            var next = $(this).next();
            if (!next.length) {
                next = $(this).siblings(':first');
            }
            next.children(':first-child').clone().appendTo($(this));
        });
        // quantity design in cart lines when promotion app installed
        $(".te_cart_table .css_quantity > span").siblings("div").css("display", "none")
        // Portal script
        if ($('div').hasClass('o_portal_my_home')) {
            if (!$('a').hasClass('list-group-item')) {
                $(".page-header").css({
                    'display': 'none'
                })
            }
        }

        /** On click selected input, filter will be clear*/
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
                $('.te_view_all_filter_div .te_view_all_filter_inner .attr_filters').find('.te_clear_attr_a.'+attr_value).trigger('click');
            }
        });
        $( "select" ).change(function () {
            $(this).find("option:selected").each(function() {
                var attr_value = $(this).parents('.nav-item').find('.te_clear_all_variant').attr('attribute-name');
                if(!$(this).text()) {
                    $('.te_view_all_filter_div .te_view_all_filter_inner .attr_filters').find('.te_clear_attr_a.'+attr_value).trigger('click');
                }
            });
        });
        var product_detail = new sAnimations.registry.product_detail();
        product_detail.productGallery();
    })


    //------------------------------------------
    // 07. Compare short name
    //------------------------------------------
    $(document).ready(function(){
        var maxLength = 26;
        var number_compare_item = $("#o_comparelist_table").find('tr:first').find('td').length;
        if(number_compare_item == 4)
        {
            maxLength = 35;
        }
        else if(number_compare_item == 3)
        {
            maxLength = 46;
        }

        var ellipsestext = "...";
        $(".more").each(function(){
            var myStr = $(this).text();
            if($.trim(myStr).length > maxLength){
                var newStr = myStr.substring(0, maxLength);
                var html = newStr + '<span class="moreellipses">' + ellipsestext+ '</span>';
                $(this).html(html);
            }
        });

        /* Slider 14 animation on mouse hover */
        var lFollowX = 0,
         lFollowY = 0,
         x = 0,
         y = 0,
        friction = 1 / 30;

        function moveBackground(e) {
          x += (lFollowX - x) * friction;
          y += (lFollowY - y) * friction;

          var translate = 'translate(' + x + 'px, ' + y + 'px) scale(1.1)';

          $('.te_s14_img').css({
            '-webit-transform': translate,
            '-moz-transform': translate,
            'transform': translate
          });

          window.requestAnimationFrame(moveBackground);
        }

        $(window).on('mousemove click', function(e) {

          var lMouseX = Math.max(-100, Math.min(100, $(window).width() / 2 - e.clientX));
          var lMouseY = Math.max(-100, Math.min(100, $(window).height() / 2 - e.clientY));
          lFollowX = (20 * lMouseX) / 100;
          lFollowY = (10 * lMouseY) / 100;

        });

        moveBackground();

        var owl_rtl = false;
        if ($('#wrapwrap').hasClass('o_rtl')) {
            owl_rtl = true;
        }

        $("#myCarousel_banner_prod_slider").find(".a-submit").click(function (event) {
            sale._onClickSubmit(event)
        });

        var myCarousel_acce_full = $('.accessory_product_main.full-width .owl-carousel, .alternative_product_main.full-width .owl-carousel').owlCarousel({
            loop: false,
            rtl: owl_rtl,
            rewind: true,
            margin: 10,
            lazyLoad:true,
            nav: true,
            dots: false,
            autoplay: true,
            autoplayTimeout: 4000,
            navText : ['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>'],
            autoplayHoverPause:true,
            items: 4,
            responsive: {
                0: {
                    items: 1,
                },
                576: {
                    items: 2,
                },
                991: {
                    items: 3,
                },
                1200: {
                    items: 4,
                }
            }
        });

        var myCarousel_acce_prod = $('.accessory_product_main .owl-carousel, .alternative_product_main .owl-carousel').owlCarousel({
            loop: false,
            rtl: owl_rtl,
            rewind: true,
            margin: 10,
            lazyLoad:true,
            nav: true,
            dots: false,
            autoplay: true,
            autoplayTimeout: 4000,
            navText : ['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>'],
            autoplayHoverPause:true,
            items: 2,
            responsive: {
                0: {
                    items: 1,
                },
                576: {
                    items: 2,
                }
            }
        });
    });

    publicWidget.registry.productsRecentlyViewedSnippet.include({
        /*
         Adds the stock checking to the regular _render method
        @override
        */
        _render: function (){
            this._super.apply(this, arguments);
            var r_name = $("#te_rect_cnt").text();
            $('.te_recently_viewed').find('h6').each(function(){
                $(this).addClass("te_rect_name")
                if(r_name == 2) {
                    $('h6.card-title').addClass('te_2_line');
                }
                if(r_name == 3) {
                    $('h6.card-title').addClass('te_3_line');
                }
            });
        },
    });

    sAnimations.registry.productTab = sAnimations.Class.extend({
        selector: "#wrapwrap",
        start: function () {
            var self = this;
            self.selectProductTab();
        },

        selectProductTab: function(){
            $('#te_product_tabs').find('li:first-child').find('.nav-link').addClass('active');
            var firstAttr = $('#te_product_tabs').find('li:first-child').find('.nav-link').attr('aria-controls');
            $('.tabs_container_main .product-body .tab-pane').removeClass('active show');
            $('#'+ firstAttr).addClass('active show');
        },
    });

    var owl_rtl = false;
    if ($('#wrapwrap').hasClass('o_rtl')) {
        owl_rtl = true;
    }
    $('.te_banner_slider_content').owlCarousel({
        loop: true,
        rtl: owl_rtl,
        nav: true,
        dots: false,
        lazyLoad:true,
        navText : ['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>'],
        autoplay: true,
        autoplayTimeout: 4000,
        autoplayHoverPause:true,
        items: 1,
        responsive: {
            0: {
                items: 1,
            },
            576: {
                items: 1,
            },
        },
    });

    /* For counting number */

    sAnimations.registry.NumberCount = sAnimations.Animation.extend({
        selector: '#wrapwrap',
         effects: [{
            startEvents: 'scroll',
            update: '_numberCount',
        }],
        init: function () {
            this._super(...arguments);
            this.viewed = false;
            this.windowWidth = $(window).width();
        },
        _numberCount: function (scroll) {
            /*Refresh AOS on scroll the page */
            if(this.windowWidth > 767) {
                AOS.refresh();
            }
            if (scroll > 200 && this.isScrolledIntoView($(".te_numbers")) && !this.viewed) {
                this.viewed = true;
                $('.te_count_value').each(function () {
                    $(this).prop('Counter',0).animate({
                        Counter: $(this).text()
                    }, {
                        duration: 4000,
                        easing: 'swing',
                        step: function (now) {
                            $(this).text(Math.ceil(now));
                        }
                    });
                });
            }
        },
        isScrolledIntoView: function (elem) {
            if(elem.length){
                var docViewTop = $(window).scrollTop();
                var docViewBottom = docViewTop + $(window).height();

                var elemTop = $(elem).offset().top;
                var elemBottom = elemTop + $(elem).height();

                return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
            }
        }
    });

    $(window).on("orientationchange",function(){
      location.reload();
    });

    publicWidget.registry.ScrollReview = publicWidget.Widget.extend({
        selector: '#wrapwrap',
        events: {
            'click .ept-total-review': 'scroll_review_tab',
        },
        scroll_review_tab: function() {
            if ($("#nav_tabs_link_ratings").length > 0){
                var header_height = 10;
                if($('header#top').length && !$('header').hasClass('o_header_sidebar')) {
                    if($('header nav').hasClass('te_header_navbar')) {
                        this.header_height = $('header nav').height() + 30;
                    } else {
                        this.header_height = $('header').height() + 30;
                    }
                }
                var totalHeight = parseInt($("#te_product_tabs").offset().top) - parseInt(header_height) - parseInt($("#te_product_tabs").outerHeight());
                if ($(window).width() < 768)
                    totalHeight += 120;
                $([document.documentElement, document.body]).animate({
                    scrollTop: totalHeight
                }, 2000);
                $('#nav_tabs_link_ratings').trigger('click');
            }
        },
    });
    /* Attribute value tooltip */
    $(function () {
      $('[data-toggle="tooltip"]').tooltip({ animation:true, delay: {show: 300, hide: 100} })
    });

    /* collapsible product variants section */
    $(document.body).on('click', '.te_s_variant_text' ,function(){
        if( $(this).find('.fa-caret-down').length ){
            $(this).find('.fa-caret-down').toggleClass('fa-caret-up');
        }
        $('#products_grid .js_add_cart_variants, #product_details .js_add_cart_variants').slideToggle('slow');
    });

    publicWidget.registry.brandPage = publicWidget.Widget.extend({
        selector: ".featured-all-brands",
        read_events: {
            'click .has-brands': '_onClickAlpha',
            'click #all-brands': '_showAllBrands',
            'keyup #search_box': '_onKeyupInput'
        },
        _onClickAlpha: function(ev) {
            this.showAllBrands();
            var $this = $(ev.currentTarget);
            var value = $('#search_box').val();
            $this.children().toggleClass('selected');
            var selected_letter_arr = []
            $('.selected').each(function(i) {
                selected_letter_arr.push($.trim($(this).text()))
            });
            $('.brand-alpha-main').each(function(e) {
                var first_letter = $(this).find('.brand-name').text().substring(0, 1).toLowerCase();
                if ($.inArray(first_letter, selected_letter_arr) == -1) {
                    $(this).addClass('d-none');
                }
            });
            if (value) {
                this.removeBlocks(value);
            }
        },
        _showAllBrands: function(ev) {
            $('.selected').removeClass('selected');
            this.showAllBrands();
            var value = $('#search_box').val();
            this.removeBlocks(value);
        },

        _onKeyupInput: function(ev) {
            $('.selected').removeClass('selected');
            var value = $(ev.currentTarget).val();
            this.showAllBrands();
            this.enableBrandBox();
            if (value.length >= 1) {
                this.removeBlocks(value);
                this.disableBox(value);
            } else {
                $('.selected').removeClass('selected');
            }
        },
        showAllBrands: function() {
            $('.brand-alpha-main').each(function(e) {
                $(this).find('.brand-item.d-none').each(function(e) {
                    $(this).removeClass('d-none');
                });
                $(this).removeClass('d-none');
            });
        },
        removeBlocks: function(value) {
            $('.brand-alpha-main').each(function(i) {
                var flag = 0
                $(this).find('.brand-item').each(function(i) {
                    var brand = $(this).find('.brand-name').text()
                    if (brand.toLowerCase().indexOf(value.toLowerCase()) == -1) {
                        $(this).addClass('d-none');
                    }
                    if (!$(this).hasClass('d-none')) {
                        flag = 1;
                    }
                });
                if (flag == 0) {
                    $(this).addClass('d-none');
                }
            });
        },
        enableBrandBox: function() {
            $('.has-brands.active').each(function(i) {
                if ($(this).hasClass('disabled')) {
                    $(this).removeClass('disabled');
                }
            });
        },
        disableBox: function(value) {
            var enabled_array = new Array();
            $('.brand-alpha-main').each(function(i) {
                var flag = 0;
                $(this).find('.brand-item').each(function(i) {
                    if (flag == 0) {
                        var brand = $(this).find('.brand-name').text();
                        if (brand.toLowerCase().indexOf(value.toLowerCase()) != -1) {
                            enabled_array.push($(this).find('.brand-name').text().substring(0, 1).toLowerCase());
                            flag = 1;
                        }
                    } else {
                        return false;
                    }
                });
            });
            if (enabled_array.length == 0) {
                $('.has-brands.active').each(function(i) {
                    $(this).addClass('disabled');
                });
            } else {
                enabled_array.forEach(function(item) {
                    $('.has-brands.active').each(function(i) {
                        if ($.inArray($.trim($(this).children('.brand-alpha').text()), enabled_array) == -1) {
                            $(this).addClass('disabled');
                        }
                    });
                });
            }
        }
    });

    publicWidget.registry.StandardAffixedHeader.include({
        _updateHeaderOnScroll: function(scroll) {
            const mainPosScrolled = (scroll > this.headerHeight + this.topGap + 300);
            const reachPosScrolled = (scroll > this.scrolledPoint + this.topGap);
            const fixedUpdate = (this.fixedHeader !== mainPosScrolled);
            const showUpdate = (this.fixedHeaderShow !== reachPosScrolled);

            if (fixedUpdate || showUpdate) {
                this.$el.css('transform',
                    reachPosScrolled ?
                    `translate(0, -${this.topGap}px)` :
                    mainPosScrolled ?
                    'translate(0, -100%)' :
                    '');
                void this.$el[0].offsetWidth; // Force a paint refresh
            }

            this.fixedHeaderShow = reachPosScrolled;

            if (fixedUpdate) {
                this._toggleFixedHeader(mainPosScrolled);
            } else if (showUpdate) {
                this._adaptToHeaderChange();
            }
            // Show/hide header
            if (this.fixedHeaderShow !== reachPosScrolled) {
                this.$el.css('transform', reachPosScrolled ? `translate(0, -${this.topGap}px)` : 'translate(0, 0)');
                this.fixedHeaderShow = reachPosScrolled;
                this._adaptToHeaderChange();
            }
        },
    });

    publicWidget.registry.FixedHeader.include({
        _updateHeaderOnScroll: function(scroll) {
            if (scroll > (this.scrolledPoint + this.topGap + 300)) {
                if (!this.$el.hasClass('o_header_affixed')) {
                    this.$el.css('transform', `translate(0, -${this.topGap}px)`);
                    void this.$el[0].offsetWidth; // Force a paint refresh
                    this._toggleFixedHeader(true);
                }
            } else {
                this._toggleFixedHeader(false);
                void this.$el[0].offsetWidth; // Force a paint refresh
                this.$el.css('transform', '');
            }
        },
    });
});
