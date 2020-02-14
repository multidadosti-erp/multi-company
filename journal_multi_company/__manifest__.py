# Copyright 2015 Oihane Crucelaegui
# Copyright 2015-2019 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Journal Multi Company",
    "summary": "Allow Jounals to have multiple companies",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "partner_multi_company",
        "account_financial_partner_expense"
    ],
    "author": "Tecnativa, "
              "Odoo Community Association (OCA), "
              "Luan Gomes, ",
    "category": "Journal Multi Company Management",
    "data": [
        "views/account_view.xml",
    ],
    "installable": True,
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
}
