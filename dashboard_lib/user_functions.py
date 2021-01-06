import abc
import socket


class User:
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def get_permissions_e_id_from_host(self, hostname):
        """
        implementar de acordo com database de usuarios utilizados
        :param hostname: hostname given by local ns
        :type hostname: str
        :return: id, permissions
        :rtype: str, list
        """
        return

    def __init__(self):
        self.codigo_unico = None
        self.permissoes = []

    def get_user_from_ip(self, ip):
        """
        returns the user and permission list from ip address of request
        :param ip: ip address of request
        :type ip: str
        :return: id code and permission list
        :rtype: (str, list)
        """
        if ip == '127.0.0.1' or ip is None:
            hostname = socket.gethostname()
        else:
            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except:
                hostname = ''
        self.codigo_unico, self.permissoes = self.get_permissions_e_id_from_host(hostname)


