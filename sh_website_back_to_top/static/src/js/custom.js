odoo.define("sh_website_back_to_top.back_to_top", function (require) {
    "use strict";

    var publicWidget = require("web.public.widget");
    var animations = require('website.content.snippets.animation');


    $(document).on('click', 'a.js_cls_sh_website_back_to_top', function (ev) {
        ev.stopPropagation();
        ev.preventDefault();

        $('#wrapwrap').stop().animate({
            scrollTop: 0
        }, 2000, 'easeInOutExpo');
    });




    publicWidget.registry.sh_ecomate_back_to_top = animations.Animation.extend({
        selector: "#wrapwrap",
        disabledInEditableMode: true,
        effects: [{
            startEvents: 'scroll',
            update: '_add_remove_back_to_top_btn_on_scroll',
        }],

        /**
         * @constructor
         */
        init: function () {
            this._super(...arguments);
            var self = this;
            this.button = '<a href="" class="btn btn-secondary js_cls_sh_website_back_to_top"><i class="fa fa-chevron-up" aria-hidden="true"></i></a>';
            this.amount_scrolled = 300;
            $('body').append(this.button);
        },

        //--------------------------------------------------------------------------
        /**
         * Called when the window is scrolled
         *
         * @private
         * @param {integer} scroll
         */
        _add_remove_back_to_top_btn_on_scroll: function (scroll) {
            var self = this;
            if (scroll > self.amount_scrolled) {
                $(document).find('a.js_cls_sh_website_back_to_top').fadeIn('slow');
            } else {
                $(document).find('a.js_cls_sh_website_back_to_top').fadeOut('slow');
            }
        },


    });
});


