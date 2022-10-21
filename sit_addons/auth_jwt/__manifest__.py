# -*- coding: utf-8 -*-
{
    'name': "JWT Authentication",

    'summary': """Implement JWT authentication for endpoints""",

    'description': """
        Implement to allow user authentication with JWT. Authorization header
        will be required on endpoints if specified.
    """,

    'author': "Nguyen Van Vu",
    'website': "1951012152vu@ou.edu.vn",

    'category': 'Authentication',
    'version': '12.0.1.0.1',

    'depends': ['base','sit_api_base'],

    'data': [
        # 'security/ir.model.access.csv',
    ],

    'installable': True,
    'application': True,
}
