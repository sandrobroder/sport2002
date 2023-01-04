14.0.1
----------------------------
Initial Release


14.0.2 (18th Nov 2022)
-----------------------

 Added new feature import_extra_images_with_underscore_naming_format


 14.0.3 (18th Nov 2022)
-----------------------

=> [ADD] depends processcontrol_product_image
=> [fix] import product image


 14.0.4 (29 Dec 2022)
-----------------------
=> [fix] image_variant_1920 don't write in when import template.
    record_vals = {
        'image_1920': image_base64
    }
    if self.product_model == 'pro_var':
        record_vals.update({
            'image_variant_1920': image_base64,
        })
    search_record.sudo().write(record_vals)

