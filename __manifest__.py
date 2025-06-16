{
    'name': 'Hospital Management System',
    'version': '1.0',
    'author':'Awnwer',
    'category': 'Healthcare',
    'summary': 'Manage patients, doctors, departments, and logs in hospitals',
    'description': """
        Custom HMS (Hospital Management System) for managing hospital data.
        Includes patients, doctors, departments, logs, and tracking state/history.
    """,
    'depends': ['base','contacts','sale_management','crm'],
    'data': [
        'security/hms_security.xml',
        'security/ir.model.access.csv',
        'views/patient_views.xml',
        'views/res_partner_inherit.xml',
        'reports/patient_report_template.xml',
        'reports/patient_report_template_pdf.xml',
        'reports/pdf_report_defintion.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
