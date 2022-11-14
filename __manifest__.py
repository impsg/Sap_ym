{
    'name' : 'SAP',
    'version' : '2.0.0',
    'summary': 'Sap Customers',
    'sequence': -100,
    'description': """SAP INVOICING""",
    'category': 'SAP',
    'data': [
        'data/cron.xml',
        'views/views.xml'

    ],

    'depends': ['base', 'crm'],

    'demo': [],

    'installable': True,
    'application': True,

    'license': 'LGPL-3',
}
