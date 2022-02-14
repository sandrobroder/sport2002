/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
odoo.define('website_lazy_loading.wk_lazy', function (require) {
    "use strict";

    var ajax = require('web.ajax');

    $(document).ready(function() {
        var count = 2;
        var page = 1;
        var ppg = 20;
        var offset = 0;
        var loading_item = true;
        var is_empty = true;
        count = parseInt(count);
        page = parseInt(page);
        offset = parseInt(offset);
        if ($('#products_grid').length > 0) {
            $('#wrapwrap').scroll(function() {
                var curr_position = $(window).scrollTop() + $(window).height() > $(document).height() - 250;
                if(curr_position && is_empty && loading_item) {
                    try {
                        loading_item = false;
                        offset = ppg;
                        ppg = ppg + 8;
                        var view = 'grid';
                        var category= 0;
                        var attributes = [];
                        var search = "";
                        $("div#wk_loader").addClass('show');
                        if($(".selected_filters .selected_category").length){
                          category = $(".selected_filters .selected_category").attr("data-index");
                        }
                        if ($(".selected_filters .attributes").length){
                          var attributes = $(".selected_filters .attributes .attrib_list").attr("data-list");
                        }
                        else{
                          attributes = null;
                        }
                        var url = window.location.href;
                        let start = url.indexOf("search=");
                        if(start > 0){
                          url = url.substring(start+7,)
                          var end = url.indexOf("&");
                          if (end > 0){
                            search = url.substring(0,end);
                          }
                          else{
                            search = url;
                          }
                        }
                        if ($('.oe_list').length) {
                            view = 'list';
                        }
                        ajax.jsonRpc("/lazy/load", 'call', {'search':search, 'page':page, 'ppg':ppg, 'offset':offset, 'view':view, 'category_selected':category,'attributes':attributes})
                            .then(function (data) {
                                if (data) {
                                    $("div#wk_loader").hide();
                                    var path = window.location.pathname;
                                    if (view == 'list') {
                                        $("#products_grid div.oe_list:last").after(data.data_grid);
                                    } else {
                                        $("#products_grid table tr:last").after(data.data_grid);
                                    }
                                    if (data.count == 0) {
                                        $("div#wk_loader").text("You've reached the end.");
                                        $("div#wk_loader").css("background-image", "none");
                                        $("div#wk_loader").css("display", "unset");
                                        is_empty = false;
                                    }
                                }
                              loading_item = true;
                            })

                    } catch (error) {
                        console.log("++++++++++++++++++" + error);
                    }

                }
            });
        }
    });

})
