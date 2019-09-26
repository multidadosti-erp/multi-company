# Copyright 2013-Today Odoo SA
# Copyright 2016 Chafique DELLI @ Akretion
# Copyright 2018 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Inter Company Module for Purchase to Sale Order',
    'summary': 'Intercompany PO/SO rules',
    'version': '11.0.1.0.0',
    'category': 'Purchase Management',
    'website': 'http://www.github.com/OCA/multi-company',
    'author': 'Odoo SA, '
              'Akretion, '
              'Tecnativa, '
              'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'installable': False,
    'depends': [
        'sale',
        'purchase',
        'account_invoice_inter_company',
    ],
    'data': [
        'views/res_company_view.xml',
        'views/res_config_view.xml',
        'views/purchase_order_view.xml',
    ],
}
