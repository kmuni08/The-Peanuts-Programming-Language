from Error import Error


class InvalidSyntaxError(Error):
    def __init__(self, position_start, position_end, error_content=''):
        super().__init__(position_start, position_end, 'Invalid Syntax', error_content)
