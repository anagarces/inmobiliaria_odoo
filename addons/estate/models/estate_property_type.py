from odoo import models, fields

class Estate_Property_Type(models.Model):

    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(required=True)