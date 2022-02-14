odoo.define('button', function (require) {
"use strict";

var core = require('web.core');
var Tour = require('web.Tour');

var _t = core._t;

$(document).ready(function() {
    $("back2top").click(function(event) {
        event.preventDefault();
        $("html, body").animate({ scrollTop: 0 }, "slow");
        return false;
    });

});
