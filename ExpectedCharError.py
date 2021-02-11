from Error import Error


class ExpectedCharError(Error):
    def __init__(self, position_start, position_end, error_content):
        super().__init__(position_start, position_end, 'Expected Character', error_content)
