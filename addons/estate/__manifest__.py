{
    'name': 'estate',
    'category': 'Real Estate/Brokerage',
    'version': '1.0',
    'depends': ['base'],
    'installable': True,
    'application': True,
    'data': [
        'security/security.xml', 
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',  
        'views/estate_property_type_views.xml',    
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
    ],
}