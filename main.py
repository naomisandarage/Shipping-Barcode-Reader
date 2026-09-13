import cv2
import zxingcpp
from parsers import parse_barcode

image = cv2.imread("ShippingLabelExample.jpeg")
results = zxingcpp.read_barcodes(image)

for barcode in results:
    if barcode.format == zxingcpp.BarcodeFormat.PDF417:
        parsed_data = parse_barcode(barcode.text)
        recipient = parsed_data.get("recipient", {})

        print("=== SHIPPING LABEL DATA ===")
        print(f"Recipient:  {recipient.get('name')}")
        print(f"Address:    {recipient.get('street')}, {
              recipient.get('city')}")

        print("\n=== PACKAGE INFO ===")
        pkg = parsed_data.get('package', {})
        print(f"Tracking #: {pkg.get('tracking_number')}")
        print(f"Weight:     {pkg.get('weight')}")
        print(f"Contents:   {pkg.get('description')}")
