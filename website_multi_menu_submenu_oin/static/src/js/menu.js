odoo.define('website_multi_menu_submenu_oin.website_menu', function (require) {
    'use strict';

    $(document).ready(function () {
        $('.dropdown-menu a.dropdown-toggle').on(
            'click',
            function (e) {
                e.preventDefault();
                e.stopPropagation();
                if (!$(this).next().hasClass('show')) {
                    $(this).parents('.dropdown-menu').first().find(
                            '.show').removeClass("show");
                }
                var $subMenu = $(this).next();
                if (!$(this).next().hasClass('show')) {
                    $subMenu.addClass('show');
                } else {
                    $subMenu.removeClass('show');
                }
                $(this).parents('li.nav-item.dropdown.show').on(
                        'hidden.bs.dropdown',
                        function (e) {
                            $('.dropdown-menu .show').removeClass("show");
                });
            return false;
        });
    });
});
