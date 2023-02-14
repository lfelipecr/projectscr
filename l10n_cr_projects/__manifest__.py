{
    "name": "L10N CR PROYECTOS/COMPRAS/CAMINOS",
    'summary': """
        Modulo mejorado para proyectos Costa Rica.""",
    'description': """
       Modulo para creación de:
        1. Caminos.
        2. Relación caminos->proyectos y proyectos->compras""",
    'version': '0.1',
    "author": "Jhonny",
    'license': 'LGPL-3',
    "depends": ['base','stock','project','purchase','l10n_cr_territories','purchase_stock','product'],
    "data": [
        # security
        "security/ir.model.access.csv",
        # data
        "data/sequence.xml",
        # views
        "views/project_camino_views.xml",
        "views/project_views.xml",
        "views/menus.xml",
        "views/purchase_views.xml",
        "views/project_work_report_views.xml",
    ],
}
