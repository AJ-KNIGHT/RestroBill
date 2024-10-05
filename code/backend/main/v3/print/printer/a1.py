from weasyprint import HTML, CSS

def html_to_pdf_with_custom_size(html_content, output_path):
    """
    Converts HTML content to PDF with specified page dimensions.

    Args:
        html_content (str): The HTML content to be converted.
        output_path (str): The path to save the generated PDF file.

    Returns:
        None
    """

    # Create a default configuration (no custom CSS)

    # Set custom page size
    # options = {
        # 'page-width': '88mm',
        # 'page-height': 'auto',
    # }

    # Write the PDF
    # HTML(string=html_content).write_pdf(
        # output_path,
        # options=options
    # )
    HTML(string=html_content).write_pdf(
        output_path
    )

    print(f"PDF generated successfully at {output_path}")
   # @page {
        # size: 88mm auto;
    # }
# Example usage
html_content = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bill</title>
    <style>
    @page {
        size: 88mm 5in;
        margin: 1px;
        padding: 0;
        }
        * {
            margin: 0;
            padding: 0;
        }

        body {
            font-family: Arial, sans-serif;
            font-size: 14px;
        }

        .bill {
            border: 1px solid black;
            margin: 0 auto;
            width: 84mm;
            height: auto;
            text-align: center;
            padding: 5px;
        }

        img {
            margin-top: 5px;
            width: 80px;
        }

        h2 {
            margin: 10px 0 0;
            font-size: 18px;
        }

        .addr {
            font-weight: normal;
            font-size: 10px;
        }

        .dotted-top {
            border-top: 3px dotted black;
        }

        .dotted-down {
            border-bottom: 3px dotted black;
        }

        span {
            display: block;
            font-weight: bold;
        }

        .p-10 {
            padding: 10px;
        }

        .p-2 {
            padding: 2px;
        }

        .mar-b-10 {
            margin-bottom: 10px;
        }

        .mar-b-20 {
            margin-bottom: 20px;
        }

        .mar-b-30 {
            margin-bottom: 30px;
        }

        table {
            margin: 0 auto;
            width: 95%;
            text-align: center;
            table-layout: fixed;
        }

        table,
        tr {
            border-bottom: 2px solid black;
            border-collapse: collapse;
            font-size: 13.5px;
        }

        th,
        td {
            padding: 10px 0;
            word-wrap: break-word;
            white-space: normal;
            width: 45px;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .pay {
            display: flex;
            justify-content: space-between;
            text-align: left;
        }

        .pay span {
            word-wrap: break-word;
            white-space: normal;
            width: 115px;
            overflow: hidden;
            text-overflow: ellipsis;
        }
    </style>
</head>
<body>
    <div class="bill">
        <div>
            <img src="http://localhost:5000/images/bill-icon.png">
        </div>
        <h2>Aboos Restaurant</h2>
        <span class="mar-b-20 addr">Palakkad Road, Pattambi</span>
        <span class="dotted-top dotted-down p-2">Bill</span>
        <div class="p-10 dotted-down">
            <span>Date: 04/10/24 08:09 PM</span>
            <span>Staff Name: amal</span>
        </div>
        <table class="mar-b-10">
            <thead>
                <tr>
                    <th>No</th>
                    <th>Name</th>
                    <th>Qty</th>
                    <th>MRP</th>
                    <th>Price</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td>Tea</td>
                    <td>1</td>
                    <td>₹10</td>
                    <td>₹10.00</td>
                </tr>
            </tbody>
        </table>
        <h4 class="mar-b-10">
            <span>Total amount : ₹10</span>
        </h4>
        <div class="pay mar-b-10">
            <div>
                <span>Payment : CASH</span>
                <span>Discount : 0.0</span>
            </div>
            <div>
                <span>Tendered : 10</span>
                <span>Change : ₹0.00</span>
            </div>
        </div>
        <span class="dotted-top dotted-down p-2 mar-b-30">Number of items: 1</span>
    </div>
</body>
</html>
"""

output_path = './pos_receipt.pdf'
html_to_pdf_with_custom_size(html_content, output_path)
