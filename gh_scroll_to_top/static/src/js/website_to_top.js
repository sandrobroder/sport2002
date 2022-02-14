odoo.define('gh_scroll_to_top.to_top', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    
	publicWidget.registry.ToTop = publicWidget.Widget.extend({
        selector: '#wrapwrap',
        events:{
			'click #btntotop': 'topFunction'
		},
        start: function () {
            var self = this;
            this._super.apply(this, arguments);
            window.addEventListener("scroll", function(ev){
                self.review_to_top();
            });
        },
        review_to_top: function(){
            if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
                document.getElementById("btntotop").style.display = "block";
            } else {
                document.getElementById("btntotop").style.display = "none";
            }
        },
        topFunction: function(){
            $("html,body").animate({ scrollTop: 0 }, "slow");
        }
    });
});