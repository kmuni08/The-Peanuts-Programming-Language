from Error import Error


class IllegalCharacterErr(Error):
    def __init__(self, position_start, position_end, error_content):
        super().__init__(position_start, position_end, 'Illegal Character', error_content)
