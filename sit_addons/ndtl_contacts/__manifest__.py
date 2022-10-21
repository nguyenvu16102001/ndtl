# -*- coding: utf-8 -*-
{
    'name': "NDTL Contacts",

    'summary': """
        Modify module """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Nguyen Van Vu",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'auth_jwt','product_brand'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'data/district.state.csv',

        'views/retailer_request_form.xml',
        'views/inherited_res_partner_views.xml',
        'views/inherited_res_users_views.xml',
        'views/country_district_views.xml',
        
        'wizard/ndtl_wizard_res_partner_views.xml',
    ],

}
