from odoo import api, fields, models


class AccountJournal(models.Model):
    _inherit = ["multi.company.abstract", "account.journal"]
    _name = 'account.journal'

    @api.model
    def create(self, vals):
        """Sobrescreve o método que cria um diário e verifica
        se o tipo for parceiro, a partir disso, atribui o
        valor das empresas para ser igual as empresas do parceiro.

        Arguments:
            vals {dict} -- Os valores de criação do diário

        Returns:
            dict -- Criação do account_journal
        """
        res = super().create(vals)
        if res.type == 'partner':
            res.write({
                'company_ids': [(6, 0, res.partner_id.company_ids.ids)]
            })
        return res
