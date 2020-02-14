from odoo.addons.journal_multi_company.tests.test_common import TestCommon


class TestResPartner(TestCommon):

    def setUp(self):
        super().setUp()

    def test_onchange_company_ids(self):
        journal = self.env['account.journal'].create({
            'name': 'Test Journal',
            'code': 'INV',
            'type': 'partner',
            'partner_id': self.partner.id,
            'company_ids': [(6, 0, [1])],
        })

        self.assertEqual(journal.company_ids.ids, self.partner.company_ids.ids)

        self.partner.write({
            'company_ids': [(6, 0, [78])],
            'journal_id': journal.id
        })

        self.partner.onchange_company_ids()

        self.assertEqual(journal.company_ids.ids, [78])
