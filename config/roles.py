from rolepermissions.roles import AbstractUserRole

class Administrador(AbstractUserRole):
    available_permissions = {
        "gerir_mandato": True,
        "gerir_usuarios": True,
        "editar_planejamento": True,
    }

class Gestor(AbstractUserRole):
    available_permissions = {
        "gerir_usuarios": True,
        "editar_planejamento": True,
    }

class Assessor(AbstractUserRole):
    available_permissions = {
        "editar_planejamento": False,
    }