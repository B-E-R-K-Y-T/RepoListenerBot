import logging


class SanLogger:
    def __init__(self, name="SanLogger", log_file="app.log"):
        # Создаем экземпляр логгера
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Создаем обработчик для записи в файл
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Создаем обработчик для вывода в консоль
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Создаем форматтер и настраиваем обработчики
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Добавляем обработчики к логгеру
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


logger = SanLogger()


if __name__ == "__main__":
    logger = SanLogger()

    logger.debug("Это отладочное сообщение.")
    logger.info("Это информационное сообщение.")
    logger.warning("Это предупреждающее сообщение.")
    logger.error("Это сообщение об ошибке.")
    logger.critical("Это критическое сообщение.")
