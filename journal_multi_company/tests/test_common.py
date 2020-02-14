from odoo.tests.common import TransactionCase


class TestCommon(TransactionCase):

    def setUp(self):
        super().setUp()

        self.partner = self.env['res.partner'].create({
            'name': 'Test',
            'email': 'a@example.com',
            'company_ids': [(6, 0, [1, 78])],
        })
