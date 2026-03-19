# -*- coding: utf-8 -*-
{
    "name": "Teletrabajo",
    "version": "1.0.0",
    "summary": """ Teletrabajo Summary """,
    "author": "",
    "website": "",
    "category": "",
    "depends": ["base", "mail", "hr", "hr_skills", "hr_holidays"],
    "data": [
        "security/telework_security.xml",
        "security/ir.model.access.csv",
        "data/hr_leave_type_data.xml",
        "views/hr_employee_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "Teletrabajo/static/src/css/telework_timeoff.css",
            "Teletrabajo/static/src/**/*",
        ],
    },
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
