# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)
from odoo import SUPERUSER_ID, api

modules = ['account_invoice_report_due_list',
'website_sale_show_company_data',
'website_sale_product_detail_attribute_value_image',
'website_sale_product_attribute_filter_visibility',
'website_sale_delivery_group',
'sale_commission_formula',
'sale_commission_pricelist',
'sale_financial_risk',
'product_variant_multi_link',
'product_variant_sale_price',
'pos_cash_move_reason',
'l10n_es_reports',
'emipro_theme_brand',
'emipro_theme_category_listing',
'emipro_theme_landing_page',
'emipro_theme_lazy_load',
'emipro_theme_load_more',
'emipro_theme_product_carousel',
'emipro_theme_product_label',
'emipro_theme_product_label_extended',
'emipro_theme_product_tabs',
'emipro_theme_product_timer',
'emipro_theme_quick_filter',
'ept_theme_customisation',
'garazd_product_label',
'label',
'point_of_sale_logo',
'pos_coupons_gift_voucher',
'processcontrol_block_automation',
'processcontrol_comissions_by_zone',
'processcontrol_number_of_packages',
'processcontrol_order_attributes_website',
'processcontrol_payment_mode',
'processcontrol_product_image',
'pwa_ept',
'delivery_validated_slip',
'sh_import_img_zip_shop',
'sh_import_product_var',
'sh_message',
'website_hide_public_price',
'website_maintainance',
'website_product_image_by_stock',
'add_mass_product_in_sale_knk',
'emipro_theme_banner_video',
]
def migrate(cr, version):
    _logger.info(f'Starting migration from version {version}.')
    env = api.Environment(cr, SUPERUSER_ID,{})
    model = env['ir.module.module']
    module_ids = model.search(
        [('name', 'in', modules)])
    _logger.info('uninstall module %s' % modules)
    _logger.info('ids for module: %s' % module_ids)
    for module in module_ids:
        try:
            module.button_uninstall()
        except Exception as e:
            _logger.info("======****============%r",e)
    _logger.info('module uninstalled')
    cr.execute("""
                delete from ir_model_data where module in ('account_invoice_report_due_list',
'website_sale_show_company_data',
'website_sale_product_detail_attribute_value_image',
'website_sale_product_attribute_filter_visibility',
'website_sale_delivery_group',
'sale_commission_formula',
'sale_commission_pricelist',
'sale_financial_risk',
'product_variant_multi_link',
'product_variant_sale_price',
'pos_cash_move_reason',
'l10n_es_reports',
'emipro_theme_brand',
'emipro_theme_category_listing',
'emipro_theme_landing_page',
'emipro_theme_lazy_load',
'emipro_theme_load_more',
'emipro_theme_product_carousel',
'emipro_theme_product_label',
'emipro_theme_product_label_extended',
'emipro_theme_product_tabs',
'emipro_theme_product_timer',
'emipro_theme_quick_filter',
'ept_theme_customisation',
'garazd_product_label',
'label',
'point_of_sale_logo',
'pos_coupons_gift_voucher',
'processcontrol_block_automation',
'processcontrol_comissions_by_zone',
'processcontrol_number_of_packages',
'processcontrol_order_attributes_website',
'processcontrol_payment_mode',
'processcontrol_product_image',
'pwa_ept',
'delivery_validated_slip',
'sh_import_img_zip_shop',
'sh_import_product_var',
'sh_message',
'website_hide_public_price',
'website_maintainance',
'website_product_image_by_stock',
'add_mass_product_in_sale_knk',
'emipro_theme_banner_video');
                # delete from ir_ui_view where id=2243;
                # delete from ir_ui_view where name='product.product.pack';
               
                # delete from ir_model_fields where name ='approval_by_authorised';
                # delete from ir_model_fields where name ='is_approval_by_authorised';
                # delete from ir_config_parameter where key like 'advance_purchase_ordering_ept%';
                       """)
    _logger.info('**********Delete******** generate_combination')
    # cr.execute("""
    #             delete from ir_ui_view where arch_prev like '%generate_combination%';
    #             delete from ir_ui_view where arch_prev like '%ict_id%';

    #             delete from ir_ui_view where arch_prev like '%approval_by_authorised%';
    #             delete from ir_ui_view where arch_prev like '%reorder_process_id%';
    #             delete from ir_ui_view where arch_prev like '%last_sale%';
    #             delete from ir_ui_view where arch_prev like '%sale_journal%' and model='res.company';
    #            """)
    _logger.info('**********Deleted******** generate_combination')
    _logger.info('Migration completed.')