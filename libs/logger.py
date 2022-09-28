"""Модуль создающая логгер"""
import logging

__author__ = 'Минор Д.С'
__all__ = ['create_logger']


def create_logger():
    """
    Создает logger. Логирование происходит как в файл, так и в консоль.

    :param fs_work: Объект класса FsWorking
    :param log_path: Путь до папки, в которой будут хранится логи тестов

    :return logger: Возвращает объект логгер
    """

    logging.basicConfig(
                        format=u'%(asctime)-8s %(levelname)-8s [%('u'module)s:%(lineno)d] %(message)-8s',
                        filemode='w', level=logging.INFO)
    logger = logging.getLogger("tester")
    return logger
