from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    #SQL constraint
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.'),
    ]

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")
            ],
            copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(
    "estate.property.type",
    related="property_id.property_type_id",
    string="Property Type",
    store=True
)

    #Calcular validez de una oferta
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            start_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = start_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - start_date).days


    @api.model
    def create(self, vals):
        property_record = self.env['estate.property'].browse(vals['property_id'])

        if property_record.offer_ids:
            max_price = max(property_record.offer_ids.mapped('price'))
            if vals['price'] < max_price:
                raise UserError(
                    "The offer amount must be higher than the existing offers."
                )

        property_record.state = "offer_received"

        return super().create(vals)

#Acciones para botones en page de ofertas
    def action_accept_offer(self):
        for record in self:
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"

    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"