odoo.define('smart_page_scroller.top_scroller', function(require) {
'use strict';
var core = require('web.core');
var _t = core._t;

 $(document).ready(function(){

    $(window).scroll(function(){
       
        if ($(this).scrollTop() > 600) { // 300px from top
            $(back2top).fadeIn();
        } else {
            $(back2top).fadeOut();
        }
    $(back2top).click(function(){
        $('html, body').animate({scrollTop : 0},"slow");
        return false;
    });
    });
});



});