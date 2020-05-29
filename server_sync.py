import requests
from PyQt5.Qt import QObject
from PyQt5.QtCore import QRunnable, pyqtSignal


class WorkerSignals(QObject):
    result = pyqtSignal()


class ServerSync(QRunnable):
    def __init__(self, caller, server_details, user_details, sync_up_data, sync_results):
        QRunnable.__init__(self)
        self.signals = WorkerSignals()
        self.caller = caller
        self.server_address, self.class_key, self.ssl_set = server_details
        self.first_name, self.surname, self.email = user_details
        self.sync_up_data = sync_up_data
        self.sync_results = sync_results
        self.sync_results['successful'] = True

    def run(self):
        if self.ssl_set:
            protocol = "https"
            port = "443"
        else:
            protocol = "http"
            port = "80"

        request_str = "{}://{}:{}/api/test?classcode={}".format(protocol, self.server_address, port, self.class_key)
        try:
            request_data = requests.get(request_str)
            request_data.raise_for_status()
        except requests.HTTPError as http_err:
            self.sync_results['successful'] = False
            print('HTTP ERROR: {http_err}')
            self.call_return()
            return
        except Exception as err:
            self.sync_results['successful'] = False
            print('Error: {err}')
            self.call_return()
            return
        print(f"Sync up data {self.sync_up_data}")
        print("Test call successful")

        # Send all rows that are not marked as sync'd, send last sync time stamp (empty if never sync'd)
        # On success, mark all entries in database as sync'd, then add all returned entries into the database (sync'd)
        request_str = "{}://{}:{}/api/sync?classcode={}".format(protocol, self.server_address, port, self.class_key)
        try:
            request_data = requests.post(request_str, json=self.sync_up_data)
            request_data.raise_for_status()
        except requests.HTTPError as http_err:
            self.sync_results['successful'] = False
            print('HTTP ERROR: {}'.format(http_err))
            self.call_return()
            return
        except Exception as err:
            self.sync_results['successful'] = False
            print('Error: {}'.format(err))
            self.call_return()
            return

        # Add rows to the database.
        self.sync_results['synced_down_data'] = request_data.json()
        print("Sync'd down data")
        print(self.sync_results['synced_down_data'])

        self.call_return()

    def call_return(self):
        print("Call Returning")
        self.signals.result.emit()
