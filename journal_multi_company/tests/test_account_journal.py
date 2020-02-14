from odoo.addons.journal_multi_company.tests.test_common import TestCommon


class TestJournal(TestCommon):

    def setUp(self):
        super().setUp()

    def test_create(self):
        journal = self.env['account.journal'].create({
            'name': 'Test Journal',
            'code': 'INV',
            'type': 'partner',
            'partner_id': self.partner.id,
            'company_ids': [(6, 0, [1])],
        })

        self.assertEqual(journal.company_ids.ids, self.partner.company_ids.ids)

        journal = self.env['account.journal'].create({
            'name': 'Test Journal',
            'code': 'INV',
            'type': 'sale',
            'partner_id': self.partner.id,
            'company_ids': [(6, 0, [1])],
        })

        self.assertNotEqual(journal.company_ids.ids, self.partner.company_ids.ids)
        self.assertEqual(journal.company_ids.ids, [1])
