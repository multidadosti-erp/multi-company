# Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestModule(TransactionCase):

    def setUp(self):
        super(TestModule, self).setUp()

        self.test_new_company = self.env['res.company'].create({
            'name': 'Company Test Active Control',
            'active': True,
        })

        self.test_new_user = self.env['res.users'].sudo().create({
            'name': 'User Test Active Control',
            'login': 'user_test_active_control',
        })

        self.main_company = self.env.ref('base.main_company')

    # Test Section
    def test_01_disable_without_user(self):
        self.assertTrue(self.test_new_company.active)

        self.test_new_company.active = False
        self.assertFalse(self.test_new_company.active)

    def test_02_disable_with_user(self):
        with self.assertRaises(ValidationError):
            self.test_new_user.company_id.active = False

    def test_03_disable_current_company(self):
        with self.assertRaises(ValidationError):
            self.main_company.active = False
