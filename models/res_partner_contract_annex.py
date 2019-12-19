import math

from odoo import api, fields, models


class ContractOrderAnnex(models.Model):
    _name = "res.partner.contract.annex"
    _description = "Contract Order Annex"

    name = fields.Char(string="Name", help="The Number of Annex")
    order_id = fields.Many2one("sale.order", string="Order", required=True,)
    contract_id = fields.Many2one(
        "res.partner.contract", string="Contract", readonly=True,
    )

    @api.onchange("contract_id")
    def _onchange_contract_id(self):
        # Compute name if there is no custom name
        contract_number = self.contract_id.name
        annex_number = self.contract_id.contract_annex_number

        self.name = "{contract}--{annex}".format(
            contract=contract_number, annex=annex_number
        )

        # Compute domain for order_id because of bug with
        # not working correctly domain in model
        return {
            "domain": {
                "order_id": [
                    ("partner_id", "=", self.contract_id.partner_id.id),
                    ("contract_annex_id", "=", False),
                ]
            }
        }

    @api.model
    def create(self, values):
        record = super().create(values)

        # Fill annex_id to domain it in future
        record.order_id.contract_annex_id = record.id

        # Add counter
        record.contract_id.contract_annex_number += 1

        return record

    @api.multi
    def action_print_form(self):
        view = self.env.ref("client_contracts.res_partner_wizard_print_annex_view")
        return {
            "name": "Print Form of Contract Annex",
            "type": "ir.actions.act_window",
            "res_model": "res.partner.contract.wizard",
            "view_mode": "form",
            "view_id": view.id,
            "target": "new",
            "context": {"self_id": self.id},
        }

    def modf(self, arg):
        """Math.modf function for using in XML ir.action.server code
        Uses in data/fields_default.xml
        """
        return math.modf(arg)