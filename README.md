# receiptreader

Django project for storing and processing vendor receipts and invoices.
Will be ran on Google Cloud App Engine to distribute to a small number of restaurants in Canada

## Additional Notes

### Model Logic

- 'Document' represents a single invoice or receipt. It will own one or more images because some receipts need to be scanned in more than one images. It may also own PDF format scans.

- 'File' is a JPG or PDF of a receipt or invoice. When uploaded each File automatically creates a new Document, however it may later be attached to another existing Document instead if is a part of a multi page scan

- Each Document needs to be assigned to a single Vendor. For now this will be done manually but later may be done using ML.

- Each Vendor has one YAML configuration, and once a Document has a vendor selected it is assigned that YAML config.

- When an File is uploaded, OCR is performed and a JSON is returned

- If a File is assigned to another Document, it's previous Document is deleted


