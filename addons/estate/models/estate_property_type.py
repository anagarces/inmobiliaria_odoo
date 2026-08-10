from odoo import models, fields

class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(required=True)

    #SQL constraint
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'The property type name must be unique.'),
    ]