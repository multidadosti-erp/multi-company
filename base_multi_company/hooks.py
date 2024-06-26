# Copyright 2015-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2017 LasLabs Inc.
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import api, SUPERUSER_ID


__all__ = [
    'create_company_assignment_view',
    'post_init_hook',
    'uninstall_hook',
]


def create_company_assignment_view(cr):
    cr.execute("""
        CREATE OR REPLACE VIEW res_company_assignment
            AS SELECT id, name, parent_id
            FROM res_company;
    """)

    """ Multidados: Substitui regra do Odoo """
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        # Força a tabela users a regra correta de consulta para multi-company
        rule = env.ref('base.res_users_rule')
        rule.write({
            'domain_force': ("['|',('company_id','=',False),"
                              "('company_ids','in',user.company_ids.ids)]"
            ),
        })

def set_security_rule(env, rule_ref):
    """Set the condition for multi-company in the security rule.

    :param: env: Environment
    :param: rule_ref: XML-ID of the security rule to change.
    """
    rule = env.ref(rule_ref)
    if not rule:  # safeguard if it's deleted
        return
    rule.write({
        'active': True,
        'domain_force': (
            "['|', ('company_ids', 'in', user.company_id.ids),"
            " ('visible_for_all_companies', '=', True)]"
        ),
    })


def post_init_hook(cr, rule_ref, model_name):
    """ Set the `domain_force` and default `company_ids` to `company_id`.

    Args:
        cr (Cursor): Database cursor to use for operation.
        rule_ref (string): XML ID of security rule to write the
            `domain_force` from.
        model_name (string): Name of Odoo model object to search for
            existing records.
    """
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        set_security_rule(env, rule_ref)
        # Copy company values
        model = env[model_name]
        table_name = model._fields['company_ids'].relation
        column1 = model._fields['company_ids'].column1
        column2 = model._fields['company_ids'].column2
        SQL = """
            INSERT INTO %s
            (%s, %s)
            SELECT id, company_id FROM %s WHERE company_id IS NOT NULL
            ON CONFLICT DO NOTHING
        """ % (table_name, column1, column2, model._table)
        env.cr.execute(SQL)


def uninstall_hook(cr, rule_ref):
    """ Restore product rule to base value.

    Args:
        cr (Cursor): Database cursor to use for operation.
        rule_ref (string): XML ID of security rule to remove the
            `domain_force` from.
    """
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        # Change access rule
        rule = env.ref(rule_ref)
        rule.write({
            'active': False,
            'domain_force': (
                " ['|', ('company_id', '=', user.company_id.id),"
                " ('company_id', '=', False)]"
            ),
        })
