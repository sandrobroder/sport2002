odoo.define('customer_ref_unique_code', function (require) {
"use strict";

var models = require('point_of_sale.models');
var PosDB = require('point_of_sale.DB');

    models.load_fields("res.partner",['ref_unique_code']);

    PosDB.include({
        _partner_search_string: function(partner){
            var str =  partner.name;
            if(partner.barcode){
                str += '|' + partner.barcode;
            }
            if(partner.address){
                str += '|' + partner.address;
            }
            if(partner.phone){
                str += '|' + partner.phone.split(' ').join('');
            }
            if(partner.mobile){
                str += '|' + partner.mobile.split(' ').join('');
            }
            if(partner.email){
                str += '|' + partner.email;
            }
            if(partner.vat){
                str += '|' + partner.vat;
            }
            if (partner.ref_unique_code) {
                str += '|' + partner.ref_unique_code;
            }
            str = '' + partner.id + ':' + str.replace(':','') + '\n';
            return str;
        },
    });

});

