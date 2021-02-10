from Error import Error
from string_with_arrows import *


class RunTimeError(Error):
    def __init__(self, position_start, position_end, error_content, context):
        super().__init__(position_start, position_end, 'Run Time Error', error_content)
        self.context = context

    def __str__(self):
        result = self.generate_traceback()
        result += f'{self.error_message}: {self.error_content}'
        result += '\n\n' + string_with_arrows(self.position_start.file_text, self.position_start, self.position_end)
        return result

    def generate_traceback(self):
        result = ''
        position = self.position_start
        ctx = self.context
        while ctx:
            result = f' File {position.file_name}, line {str(position.line_number + 1)}, in {ctx.display_name} \n' \
                     + result
            position = ctx.parent_entry_position
            ctx = ctx.parent

        return 'Traceback (most recent call last ):\n' + result
