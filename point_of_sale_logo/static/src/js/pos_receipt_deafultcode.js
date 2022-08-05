odoo.define('module_name.receipt', function (require) {
  'use strict';
  var models = require('point_of_sale.models');
  var _super_orderline = models.Orderline.prototype;
  models.Orderline = models.Orderline.extend({
    export_for_printing: function () {
      var line = _super_orderline.export_for_printing.apply(this, arguments);
      line.default_code = this.get_product().default_code;
      return line;
    },
  });
});
