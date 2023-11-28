from openupgradelib import openupgrade
import logging
_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(cr, version):
    """Convert the former `agent_line` m2m relation in `commission.line.mixin` into
    the new `settlement_line_ids` o2m relation."""
    _logger.info(f'Starting Post migration from version {version}.')
    openupgrade.logged_query(
        cr,
        """
            UPDATE commission_settlement_line
            SET invoice_agent_line_id = sal_rel.agent_line_id
            FROM (
                SELECT DISTINCT ON (agent_line_id) agent_line_id, settlement_id
                FROM settlement_agent_line_rel
                ORDER BY agent_line_id
            ) AS sal_rel
            WHERE id = sal_rel.settlement_id
        """,
    )
    _logger.info('Migration completed.')