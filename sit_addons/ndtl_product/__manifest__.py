# -*- coding: utf-8 -*-
{
    'name': "NDTL Product",

    'summary': "Implement packaging type for products",

    'description': """
        Apply implementation to add packaging type for products.
    """,

    'author': "Nguyen Van Vu",
    'website': "1951012152vu@ou.edu.vn",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'product', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_product_views.xml',
        'views/product_template_views.xml',
    ],
    'auto_install': False,
    'installable': True
}
