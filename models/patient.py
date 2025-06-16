
import io
import base64
import xlsxwriter
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient'

    fname = fields.Char(required=True)
    lname = fields.Char(required=True)
    bdate = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([
        ('a', 'A'), ('b', 'B'), ('ab', 'AB'), ('o', 'O')
    ])
    pcr = fields.Boolean()
    image = fields.Binary()
    address = fields.Text()
    age = fields.Integer(compute='_compute_age')
    department_id = fields.Many2one('hms.department')
    doctor_ids = fields.Many2many('hms.doctor')
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], default='undetermined')
    log_ids = fields.One2many('hms.log', 'patient_id')
    email = fields.Char(string="Email", required=True)
    _sql_constraints = [
        ('unique_email', 'unique(email)', 'Email must be unique!')
    ]

    @api.depends('bdate')
    def _compute_age(self):
        for rec in self:
            if rec.bdate:
                rec.age = fields.Date.today().year - rec.bdate.year
            else:
                rec.age = 0

    @api.onchange('pcr')
    def _onchange_pcr(self):
        if self.pcr and not self.cr_ratio:
            raise ValidationError("If PCR is checked, CR Ratio is required.")

    @api.onchange('bdate')
    def _onchange_bdate(self):
        if self.bdate:
            calculated_age = fields.Date.today().year - self.bdate.year

            if calculated_age < 30:
                self.pcr = True
                return {
                    'warning': {
                        'title': "PCR Checked Automatically",
                        'message': "PCR field has been checked because age < 30"
                    }
                }
            if calculated_age < 50:
                self.history = False

    @api.constrains('department_id')
    def _check_department_open(self):
        for rec in self:
            if rec.department_id and not rec.department_id.is_opened:
                raise ValidationError("Cannot select a closed department.")

    @api.onchange('state')
    def _onchange_state(self):
        if self.state and self.id:
            self.env['hms.log'].create({
                'patient_id': self.id,
                'description': f"State changed to {self.state}"
            })
    @api.constrains('email')
    def _check_email_format(self):
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        for rec in self:
            if rec.email and not re.fullmatch(email_pattern, rec.email):
                raise ValidationError("Invalid email format. Please enter a valid email address.")
        #################
    def export_to_excel(self):
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output)
            worksheet = workbook.add_worksheet('Patients')

            headers = ['First Name', 'Last Name', 'Email', 'Age', 'Department', 'Doctors', 'State']
            for col, header in enumerate(headers):
                worksheet.write(0, col, header)

            for row, patient in enumerate(self, start=1):
                doctors = ', '.join(doctor.fname + ' ' + doctor.lname for doctor in patient.doctor_ids)
                worksheet.write(row, 0, patient.fname)
                worksheet.write(row, 1, patient.lname)
                worksheet.write(row, 2, patient.email)
                worksheet.write(row, 3, patient.age)
                worksheet.write(row, 4, patient.department_id.name or '')
                worksheet.write(row, 5, doctors)
                worksheet.write(row, 6, patient.state)

            workbook.close()
            output.seek(0)
            return {
                'type': 'ir.actions.act_url',
                'url': '/web/content/?model=hms.patient&download=true&data=%s&filename=patients_report.xlsx' % base64.b64encode(
                    output.getvalue()),
                'target': 'self',
            }