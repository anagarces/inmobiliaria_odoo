from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase
from odoo.tests import tagged, Form


@tagged('post_install', '-at_install')
class EstateOfferTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property = cls.env['estate.property'].create({
            'name': 'Test Property',
            'expected_price': 100000,
        })

    def test_no_offer_on_sold_property(self):
        """Test that an offer cannot be created for a sold property."""
        offer = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': self.env['res.partner'].create({'name': 'Buyer'}).id,
            'price': 100000,
        })
        offer.action_accept_offer()
        self.property.action_set_sold()

        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'partner_id': self.env['res.partner'].create({'name': 'Another Buyer'}).id,
                'price': 100000,
            })

    def test_no_sale_without_accepted_offer(self):
        """Test that a property cannot be sold without an accepted offer."""
        with self.assertRaises(UserError):
            self.property.action_set_sold()

    def test_property_marked_as_sold(self):
        """Test that selling a valid property correctly marks it as sold."""
        offer = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': self.env['res.partner'].create({'name': 'Buyer'}).id,
            'price': 100000,
        })
        offer.action_accept_offer()
        self.property.action_set_sold()
        self.assertRecordValues(self.property, [{'state': 'sold'}])

    def test_garden_reset(self):
        """Test that unchecking Garden resets area and orientation."""
        with Form(self.env['estate.property']) as form:
            form.name = "Garden Property"
            form.expected_price = 100000
            form.garden = True
            self.assertEqual(form.garden_area, 10)
            self.assertEqual(form.garden_orientation, 'north')

            form.garden = False
            self.assertEqual(form.garden_area, 0)
            self.assertFalse(form.garden_orientation)