# -*- coding: utf-8 -*-
{
    "name": "Teletrabajo",
    "version": "1.0.0",
    "summary": """ Teletrabajo Summary """,
    "author": "",
    "website": "",
    "category": "",
    "depends": ["base", "mail", "hr", "hr_skills"],
    "data": [
        "security/telework_request_security.xml",
        "security/ir.model.access.csv",
        "views/telework_request_views.xml",
        "views/hr_employee_views.xml",
    ],
    "assets": {
        "web.assets_backend": ["Teletrabajo/static/src/**/*"],
    },
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
