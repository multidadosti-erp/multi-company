# Copyright 2015-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html.html

from odoo import api, models


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def create(self, vals):
        res = super(ResUsers, self).create(vals)
        if 'company_id' in vals:
            res.partner_id.company_ids = [(6, 0, [vals['company_id']])]
        elif 'company_ids' in vals:
            res.partner_id.company_ids = vals['company_ids']
        return res

    @api.multi
    def write(self, vals):
        res = super(ResUsers, self).write(vals)
        if 'company_id' in vals:
            for user in self.sudo():
                if user.partner_id.company_ids:
                    user.partner_id.company_ids = \
                        [(6, 0, [vals['company_id']])]
        return res
