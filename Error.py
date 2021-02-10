# CUSTOM ERROR CLASS
from string_with_arrows import *


class Error:
    def __init__(self, position_start, position_end, error_message, error_content):
        self.position_start = position_start
        self.position_end = position_end
        self.error_message = error_message
        self.error_content = error_content

    def __str__(self):
        result = f'{self.error_message}: {self.error_content}\n'
        result += f'File {self.position_start.file_name}, line {self.position_start.line_number + 1}'
        result += '\n\n' + string_with_arrows(self.position_start.file_text, self.position_start, self.position_end)
        return result
