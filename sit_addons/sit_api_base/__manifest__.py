# -*- coding: utf-8 -*-
{
    'name': "SIT API Base",
    'summary': """The base module for API.""",
    'description': """
        API Base to itegrate odoo framework which support:
            - Json RPC 2.0
            - Restful API (Comming soon)
    """,
    'author': "SmartInnoTech",
    'website': "https://www.smartinnotech.io",
    'category': 'API',
    'version': '12.0.0.1',
    'depends': ['base',
                # OCA
                'base_jsonify',
                # Cyberos
                'product_image_url'],
    'data': [],
    'external_dependencies': {
        
    }
}
