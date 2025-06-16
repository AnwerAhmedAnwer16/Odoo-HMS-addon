from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string="Related Patient")

    @api.constrains('related_patient_id')
    def _check_unique_patient(self):
        for rec in self:
            if rec.related_patient_id:
                existing = self.search([
                    ('id', '!=', rec.id),
                    ('related_patient_id', '=', rec.related_patient_id.id)
                ])
                if existing:
                    raise ValidationError("This patient is already linked to another customer.")

    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise ValidationError("Cannot delete a customer linked to a patient.")
        return super().unlink()
