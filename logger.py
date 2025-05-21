import logging
import os

class ReverseFileHandler(logging.Handler):
    def __init__(self, filename, max_lines=100):
        super().__init__()
        self.filename = filename
        self.max_lines = max_lines

    def emit(self, record):
        try:
            msg = self.format(record)
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            else:
                lines = []

            # Inserisce in cima
            lines.insert(0, msg + '\n')
            # Limita la lunghezza
            lines = lines[:self.max_lines]

            with open(self.filename, 'w', encoding='utf-8') as f:
                f.writelines(lines)

        except Exception:
            self.handleError(record)


def return_logger():
    logger = logging.getLogger('reverse_logger')
    logger.setLevel(logging.INFO)
    log_dir = "./logs"
    os.makedirs(log_dir, exist_ok=True)
    handler = ReverseFileHandler(log_dir + '/chatbot.log', max_lines=200)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
