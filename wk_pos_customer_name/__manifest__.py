# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
    "name"          :   "POS Delivery Customer Name",
    "summary"       :   """CUSTOM : POS Delivery Customer Name""",
    "category"      :   "Point Of Sale",
    "version"       :   "1.0.0",
    "author"        :   "Webkul Software Pvt. Ltd.",
    "license"       :   "Other proprietary",
    "website"       :   "https://store.webkul.com",
    "description"   :   """POS Delivery Customer Name""",
    "depends"       :   ['point_of_sale'],
    "assets"        :   {
                            'point_of_sale.assets': [
                                "/wk_pos_customer_name/static/src/xml/pos.xml",
                            ],
                        },
    "application"   :   True,
    "installable"   :   True,
    "auto_install"  :   False,
    "pre_init_hook" :   "pre_init_check",
}