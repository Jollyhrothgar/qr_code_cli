#!/usr/bin/env python3
"""CLI tool for generating QR codes."""

import argparse
import sys

import qrcode
from qrcode.image.styledpil import StyledPilImage


def main():
    parser = argparse.ArgumentParser(
        description="Generate QR codes from text or URLs",
        prog="qr_create",
    )
    parser.add_argument(
        "data",
        help="The string to encode in the QR code",
    )
    parser.add_argument(
        "--type",
        "-t",
        choices=["url", "text", "email", "phone", "wifi"],
        default="text",
        help="Type of data being encoded (default: text)",
    )
    parser.add_argument(
        "--size",
        "-s",
        type=int,
        default=256,
        help="Size of the output image in pixels (default: 256)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="qrcode.png",
        help="Output filename (default: qrcode.png)",
    )

    args = parser.parse_args()

    # Format data based on type
    data = format_data(args.data, args.type)

    # Generate QR code
    qr = qrcode.QRCode(
        version=None,  # Auto-size
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create image and resize to requested size
    img = qr.make_image(fill_color="black", back_color="white", image_factory=StyledPilImage)
    img = img.resize((args.size, args.size))

    # Save
    img.save(args.output)
    print(f"QR code saved to {args.output}")


def format_data(data: str, data_type: str) -> str:
    """Format data according to its type for QR code standards."""
    if data_type == "url":
        # Ensure URL has a scheme
        if not data.startswith(("http://", "https://")):
            data = "https://" + data
        return data
    elif data_type == "email":
        if not data.startswith("mailto:"):
            data = "mailto:" + data
        return data
    elif data_type == "phone":
        if not data.startswith("tel:"):
            data = "tel:" + data
        return data
    elif data_type == "wifi":
        # Expect format: SSID:password or just SSID
        if ":" in data:
            ssid, password = data.split(":", 1)
            return f"WIFI:T:WPA;S:{ssid};P:{password};;"
        else:
            return f"WIFI:T:nopass;S:{data};;"
    else:
        return data


if __name__ == "__main__":
    main()
