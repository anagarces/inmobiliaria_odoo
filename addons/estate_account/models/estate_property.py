from odoo import models
from odoo.fields import Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        for record in self:
            invoice_vals = {
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': f"Sale of property {record.name}",
                        'quantity': 1,
                        'price_unit': record.selling_price,
                    }),
                ],
            }
            self.env['account.move'].create(invoice_vals)
        return super().action_set_sold()