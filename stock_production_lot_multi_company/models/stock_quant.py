from psycopg2 import Error
from odoo import api, models

import logging

_logger = logging.getLogger(__name__)


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.model
    def _merge_quants(self):
        """ Método sobrescre do Core para adicionar filtro por empresa
        """
        query = """
            WITH dupes AS (
                SELECT min(id) as to_update_quant_id,
                        (array_agg(id ORDER BY id))[2:array_length(array_agg(id), 1)] as to_delete_quant_ids,
                        SUM(reserved_quantity) as reserved_quantity,
                        SUM(quantity) as quantity
                FROM stock_quant
                WHERE (company_id is NULL or company_id = {0})
                GROUP BY product_id, company_id, location_id, lot_id, package_id, owner_id, in_date
                HAVING count(id) > 1
            ),
            _up AS (
                UPDATE stock_quant q
                    SET quantity = d.quantity,
                        reserved_quantity = d.reserved_quantity
                FROM dupes d
                WHERE d.to_update_quant_id = q.id
            )
            DELETE FROM stock_quant
            WHERE id in (SELECT unnest(to_delete_quant_ids) from dupes)
               OR id in (SELECT sq.id FROM stock_quant sq
                         JOIN stock_production_lot spl on sq.lot_id = spl.id
                         WHERE spl.company_id IS NOT NULL
                           AND sq.company_id IS NOT NULL
                           AND spl.company_id != {0})
        """.format(self.env.user.company_id.id)

        try:
            with self.env.cr.savepoint():
                self.env.cr.execute(query)
        except Error as e:
            _logger.info('an error occured while merging quants: %s', e.pgerror)
