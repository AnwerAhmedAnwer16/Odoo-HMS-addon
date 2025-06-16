from odoo import models, fields

class Doctor(models.Model):
    _name = 'hms.doctor'
    _description = 'Doctor'

    fname = fields.Char()
    lname = fields.Char()
    image = fields.Binary()
    patient_ids = fields.Many2many('hms.patient')
