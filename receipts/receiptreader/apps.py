from django.apps import AppConfig

class ReceiptreaderConfig(AppConfig):
    name = 'receiptreader'

    def ready(self):
        import .signals
