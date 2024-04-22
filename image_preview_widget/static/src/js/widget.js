/** @odoo-module **/

import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
import { ImageField } from "@web/views/fields/image/image_field";
import { patch } from "@web/core/utils/patch";

const { Component } = owl;

class ImagePreviewDialog extends Component { }
ImagePreviewDialog.components = { Dialog };
ImagePreviewDialog.template = "image_preview_widget.ImagePreviewDialog";

patch(ImageField.prototype, "patch Image Preview", {
    setup() {
        this._super();
        this.dialog = useService("dialog");
    },

    onPreview() {
        this.dialog.add(ImagePreviewDialog, {
            src: this.getUrl(this.props.name),
        });
    },
});
