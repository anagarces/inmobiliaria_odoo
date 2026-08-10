from odoo import models, fields

class EstatePropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(required=True)

    #SQL constraint
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'The tag name must be unique.'),
    ]