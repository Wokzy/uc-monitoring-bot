import logging

from ldap_test import LdapServer

__author__ = 'Dmitriy Minor'
__all__ = ['run_ldap_server']

logger = logging.getLogger()


def run_ldap_server(dn, event):
    """
    Запуск LDAP сервера в отдельном потоке
    :param dn: DN по которому будет производиться авторизация
    :param event: Ожидания ивента, скажет остановить LDAP сервер
    """
    server = LdapServer(dn)
    server.start()
    logger.info("Start LDAP server")
    event.wait()
    server.stop()
    logger.info("Stop LDAP server")
