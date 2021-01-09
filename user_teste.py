from dashboard_lib import user_functions
import time

class UserTeste(user_functions.User):
    def __init__(self):
        super().__init__()

    def get_permissions_e_id_from_host(self, hostname):
        query = """SELECT * FROM TABELA_USUARIOS WHERE HOSTNAME = HOSTNAME"""
        uid = hostname
        # time.sleep(5)
        print('reload')
        permissions = ['all']
        return uid, permissions
