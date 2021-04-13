from odoo import api, fields, models
from datetime import datetime

class Product(models.Model):
    _name = "project.product"

    # product information
    product_id = fields.Char(string='Product Id')
    product_description = fields.Char(string='Product Description')
    start_date = fields.Date(string='Start Date')
    inactive_date = fields.Date(string='Inactive Date')

    def name_get(self):
        result = []
        for record in self:
            rec_name = "%s (%s)" % (record.product_description, record.product_id)
            result.append((record.id, rec_name))
        return result

    def create_workarea(self):
        # implement the logic of copying final table data into the workarea table
        self.env['project.wa.product'].create({'product_id': self.product_id,
                                               'product_description': self.product_description,
                                               'start_date': datetime.now(),
                                               })
        return True
