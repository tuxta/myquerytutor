from PyQt5.QtCore import QSettings


class AppSettings:
    def __init__(self):
        self.settings = QSettings('Tuxtas', 'MyQueryTutor')

    def has_settings(self):
        if self.settings.contains('MainWindow/geometry'):
            return True
        else:
            return False

    def set_geometry(self, main_win, splitter_1, splitter_2):
        self.settings.setValue("MainWindow/geometry", main_win)
        self.settings.setValue("MainWindow/splitter_1", splitter_1)
        self.settings.setValue("MainWindow/splitter_2", splitter_2)

    def get_geometry(self):
        return self.settings.value("MainWindow/geometry")

    def get_splitter_1_geometry(self):
        return self.settings.value('MainWindow/splitter_1', [], int)

    def get_splitter_2_geometry(self):
        return self.settings.value('MainWindow/splitter_2', [], int)

    def set_user_details(self, first_name, surname, email):
        self.settings.setValue("User/FirstName", first_name)
        self.settings.setValue("User/Surname", surname)
        self.settings.setValue("User/email", email)

    def get_user_details(self):
        first_name = self.settings.value("User/FirstName")
        surname = self.settings.value("User/Surname")
        email = self.settings.value("User/email")
        return first_name, surname, email

    def set_server_details(self, server_address, class_key, time_stamp, ssl_on):
        self.settings.setValue("Server/address", server_address)
        self.settings.setValue("Server/class_key", class_key)
        self.settings.setValue("Server/time_stamp", time_stamp)
        self.settings.setValue("Server/ssl", ssl_on)
        self.settings.sync()

    def get_server_details(self):
        server = self.settings.value("Server/address")
        class_key = self.settings.value("Server/class_key")
        ssl_val = self.settings.value("Server/ssl")
        if ssl_val == 'true':
            ssl = True
        else:
            ssl = False
        return server, class_key, ssl

    def set_time_stamp(self, time_stamp):
        self.settings.setValue("Server/time_stamp", time_stamp)

    def get_time_stamp(self):
        return self.settings.value("Server/time_stamp")
