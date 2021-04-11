# -*- coding: utf-8 -*-
{
    'name': "Product Management App",

    'summary': """
        Product Management App""",

    'description': """
        Product Management
    """,
    'depends': [],

    'author': "Wenzhuo Liang",
    'website': "todo",

    # for the full list
    'version': '0.1',

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/project_product.xml',
        'views/project_wa_product.xml',
    ],
    # 'installable': True,
    'application': True
}