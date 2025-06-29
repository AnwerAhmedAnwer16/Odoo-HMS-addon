from odoo import models, fields

class Department(models.Model):
    _name = 'hms.department'
    _description = 'Hospital Department'

    name = fields.Char()
    capacity = fields.Integer()
    is_opened = fields.Boolean(default=True)
    patient_ids = fields.One2many('hms.patient', 'department_id')
