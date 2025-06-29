from odoo import models, fields

class PatientLog(models.Model):
    _name = 'hms.log'
    _description = 'Patient Log History'

    patient_id = fields.Many2one('hms.patient')
    created_by = fields.Many2one('res.users', default=lambda self: self.env.user)
    created_at = fields.Datetime(default=fields.Datetime.now)
    description = fields.Text()
