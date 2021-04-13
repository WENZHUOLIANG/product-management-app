from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

class Product(models.Model):
    _name = "project.wa.product"

    # product information
    product_id = fields.Char(string='Product Id')
    product_description = fields.Char(string='Product Description')
    start_date = fields.Date(string='Start Date')
    inactive_date = fields.Date(string='Inactive Date')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved')],
        'State', default="draft")

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'submitted'),
                   ('submitted', 'draft'),
                   ('submitted', 'approved')]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        _logger.info('change state')
        for product in self:
            if product.is_allowed_transition(product.state, new_state):
                product.state = new_state
            else:
                msg = _('Moving from %s to %s is not allowed') % (product.state, new_state)
                raise UserError(msg)

    def make_submitted(self):
        self.change_state('submitted')

    def make_approved(self):
        # sync the workarea item into final table and deactivate the existing record from final table
        self.change_state('approved')
        self.env['project.product'].search([('product_id', '=', self.product_id),
                                            ('inactive_date', '=', None)]).inactive_date = datetime.now()
        self.env['project.product'].create({'product_id': self.product_id,
                                            'product_description': self.product_description,
                                            'start_date': datetime.now(),
                                            })

    def make_rejected(self):
        self.change_state('draft')

    def name_get(self):
        result = []
        for record in self:
            rec_name = "%s (%s)" % (record.product_description, record.product_id)
            result.append((record.id, rec_name))
        return result