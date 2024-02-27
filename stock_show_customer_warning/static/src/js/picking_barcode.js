/** @odoo-module **/

import BarcodePickingModel from '@stock_barcode/models/barcode_picking_model';
import { _t, _lt } from "web.core";
import { patch } from 'web.utils';

patch(BarcodePickingModel.prototype, 'stock_show_customer_warning', {
    get barcodeInfo() {
        let barcodeInfo = this._super(...arguments);
        if (this.record.customer_warning_message){
            barcodeInfo.customer_warning = this.record.customer_warning_message
        }
        return barcodeInfo;
    }
});


