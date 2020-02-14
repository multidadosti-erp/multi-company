from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.onchange('company_ids')
    def onchange_company_ids(self):
        """Método que ao alterar a empresa em um cadastro de
        parceiro também muda a empresa do diário do mesmo.
        """
        for rec in self:
            rec.journal_id.sudo().write({
                'company_ids': [(6, 0, rec.company_ids.ids)]
            })
