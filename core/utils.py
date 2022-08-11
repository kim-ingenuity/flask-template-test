from sqlalchemy.engine import url


def convert_to_boolean(instance):
    """
    Returns the boolean equivalent of the instance if it's a string equal to 'True'
    or 'False'. If the instance is already boolean, the instance will be returned.

    Defaults to None for other invalid instances.
    """
    try:
        if isinstance(instance, bool):
            return instance
        if instance == 'True':
            return True
        elif instance == 'False':
            return False
        else:
            return None
    except BaseException:
        return None


class ColoredPrint:
    """
    Provides colorized console printing.
    """
    COLORS = {
        'light_green': '\033[92m',
        'yellow': '\033[93m',
        'light_red': '\033[91m',
        'light_blue': '\033[94m',
        'end_color': '\033[0m'
    }

    def normal(self, main_string, extra_string='', end='\n'):
        """
        Prints to default console color.

        Optional paramaters:
        extra_string (str): String to be appended after the main string
        end (str): String at the end. Defaults to new line. Replace with a space to continue print on same line
        """
        print(f'{main_string}{extra_string}', end=end)

    def failed(self, main_string, extra_string='', end='\n'):
        """
        Prints to a light red color to denote failure.

        Optional paramaters:
        extra_string (str): Uncolored string to be appended after the main string
        end (str): String at the end. Defaults to new line. Replace with a space to continue print on same line
        """
        print(
            f"{self.COLORS['light_red']}{main_string}{self.COLORS['end_color']}{extra_string}",
            end=end)

    def success(self, main_string, extra_string='', end='\n'):
        """
        Prints to a light green color to denote success.

        Optional paramaters:
        extra_string (str): Uncolored string to be appended after the main string
        end (str): String at the end. Defaults to new line. Replace with a space to continue print on same line
        """
        print(
            f"{self.COLORS['light_green']}{main_string}{self.COLORS['end_color']}{extra_string}",
            end=end)

    def success_alt(self, main_string, extra_string='', end='\n'):
        """
        Prints to a light blue color to denote success.

        Optional paramaters:
        extra_string (str): Uncolored string to be appended after the main string
        end (str): String at the end. Defaults to new line. Replace with a space to continue print on same line
        """
        print(
            f"{self.COLORS['light_blue']}{main_string}{self.COLORS['end_color']}{extra_string}",
            end=end)

    def warning(self, main_string, extra_string='', end='\n'):
        """
        Prints to a yellow color to denote a warning.

        Optional paramaters:
        extra_string (str): Uncolored string to be appended after the main string
        end (str): String at the end. Defaults to new line. Replace with a space to continue print on same line
        """
        print(
            f"{self.COLORS['yellow']}{main_string}{self.COLORS['end_color']}{extra_string}",
            end=end)


def make_db_connection_url(drivername, username, password, host, port, database=None, query=None, database_name=None):
        clr_print = ColoredPrint()
        missing_fields = []
        conn_url = ''

        if not drivername:
            missing_fields.append('DRIVERNAME')

        if not username:
            missing_fields.append('USERNAME')

        if not password:
            missing_fields.append('PASSWORD')

        if not password:
            missing_fields.append('PASSWORD')

        if not host:
            missing_fields.append('HOST')

        if not port:
            missing_fields.append('PORT')

        if not database and not query:
            missing_fields.append('NO ID')

        elif database and query:
            missing_fields.append('ID CONFLICT')

        if missing_fields:
            if database_name:
                clr_print.warning(f' * Missing or invalid value/s for the following {database_name} environment variable/s:')
            else:
                clr_print.warning(f' * Missing or invalid value/s for the following environment variable/s:')

            conn_prefix = f'{database_name}_CONN' if database_name else 'CONN'
            for field in missing_fields:
                if field == 'NO ID':
                    clr_print.warning(f'\t{conn_prefix}_DATABASE or {conn_prefix}_QUERY (Use only one of the variables, not both)')
                elif field == 'ID CONFLICT':
                    clr_print.warning(f'\t{conn_prefix}_DATABASE and {conn_prefix}_QUERY (Use only one of the variables, not both)')
                else:
                    clr_print.warning(f'\t{conn_prefix}_{field}')

        else:
            conn_url = url.URL(
                drivername=drivername,
                username=username,
                password=password,
                host=host,
                port=port,
                database=database,
                query=query
            )

        return conn_url
