from odoo import models, fields

class EstatePropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    #SQL constraint
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'The tag name must be unique.'),
    ]

    name = fields.Char(required=True)
    color = fields.Integer('Color')
