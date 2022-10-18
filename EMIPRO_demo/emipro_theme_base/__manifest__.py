# -*- coding: utf-8 -*-
{
    # Theme information
    'name': 'Emipro Theme Base',
    'category': 'Base',
    'summary': 'Base module containing common libraries for all Emipro eCommerce themes.',
    'version': '5.1.1',
    'license': 'OPL-1',
    'depends': [
        'website_sale_wishlist',
        'website_sale_comparison',
        'website_blog',
    ],

    'data': [
        'data/slider_styles_data.xml',
        'views/synonym_group_views.xml',
        'security/ir.model.access.csv',
        'templates/template.xml',
        'templates/product_snippet_popup.xml',
        'templates/brand_category_snippet_popup.xml',
        'templates/pwa.xml',
        'templates/assets.xml',
        'views/res_config_settings.xml',
        'views/product_template.xml',
        'views/ir_attachment.xml',
        'views/product_tabs.xml',
        'views/menu_label.xml',
        'views/website_menu_view.xml',
        'views/product_attribute_value_view.xml',
        'views/product_public_category.xml',
        'views/website.xml',
        'views/search_keyword_report_views.xml',
        'wizard/product_brand_wizard_view.xml',
        'wizard/product_document_config.xml',
        'templates/image_hotspot_popup.xml',
    ],

    # Odoo Store Specific
    'images': [
        'static/description/emipro_theme_base.jpg',
    ],

    # Author
    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'https://www.emiprotechnologies.com',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',

    # Technical
    'installable': True,
    'auto_install': False,
    'price': 19.00,
    'currency': 'EUR',
}
