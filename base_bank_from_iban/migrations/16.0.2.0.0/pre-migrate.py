# -*- coding: utf-8 -*-
from openupgradelib import openupgrade, openupgrade_160
import logging
_logger = logging.getLogger(__name__)
from odoo import SUPERUSER_ID, api

table_renames = [
    ("sale_commission", "commission"),
    ("sale_commission_settlement", "commission_settlement"),
    ("sale_commission_make_invoice", "commission_make_invoice"),
    ("sale_commission_settlement_line", "commission_settlement_line"),
    ("sale_commission_make_settle", "commission_make_settle"),
]
model_renames = [
    ("sale.commission", "commission"),
    ("sale.commission.mixin", "commission.mixin"),
    ("sale.commission.line.mixin", "commission.line.mixin"),
    ("sale.commission.settlement", "commission.settlement"),
    ("sale.commission.make.invoice", "commission.make.invoice"),
    ("sale.commission.settlement.line", "commission.settlement.line"),
    ("sale.commission.make.settle", "commission.make.settle"),
]


def _handle_settlement_line_commission_id(cr):
    """On the new version, this field is computed stored, but the compute method
    doesn't resolve correctly the link here (as it's handled in `account_commission`),
    so we pre-create the column and fill it properly according old expected data.
    """
    openupgrade.logged_query(
        cr, "ALTER TABLE commission_settlement_line ADD commission_id int4"
    )
    openupgrade.logged_query(
    cr,
        """
        UPDATE commission_settlement_line csl
        SET commission_id = aila.commission_id
        FROM settlement_agent_line_rel rel
        JOIN account_invoice_line_agent aila ON aila.id = rel.agent_line_id
        WHERE rel.settlement_id = csl.id
        AND csl.commission_id IS NULL
        """,
    )



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
    installed_module_ids = model.search(
        [('name', 'in', ['commission'])])
    installed_module_ids.button_install()
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
'emipro_theme_banner_video'); """)
    _logger.info('**********Delete******** generate_combination')
   
    _logger.info('**********Deleted******** generate_combination')
    _logger.info('Migration completed.')
    _logger.info("============installe commession")
    openupgrade.rename_tables(cr, table_renames)
    openupgrade.rename_models(cr, model_renames)
    _handle_settlement_line_commission_id(cr)
    cr.execute("""
delete from ir_ui_view where name='res.config.settings.emipro.base';
""")
    _logger.info("============module migrate")
    