from flask import Flask, render_template
from html2image import Html2Image
import os

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

@app.route('/')
def index():
    return render_template("test.html")

@app.route('/bill')
def bill():
    # Render the HTML content from the template
    html_content = render_template("bill.html")

    # Initialize Html2Image
    hti = Html2Image(output_path='./static')  # Save the image in the static folder

    # Save the HTML content to a temporary file with UTF-8 encoding
    html_file_path = 'temp.html'
    with open(html_file_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

    # Set the desired width (in pixels) and a reasonable height (e.g., 600 pixels)
    width_pixels = int(85 * 3.779527559)  # Convert mm to pixels
    height_pixels = 600  # Set a fixed height

    hti.size = (width_pixels, height_pixels)  # Set width and height

    # Take a screenshot of the HTML file
    output_image_path = 'output_image.png'
    
    try:
        hti.screenshot(html_file=html_file_path, save_as=output_image_path)
        image_url = f"/code/backend/main/v3/print/{output_image_path}"  # URL to access the generated image
        print(f"Image saved at: {image_url}")  # Print image URL for debugging
    except Exception as e:
        print(f"Error generating image: {e}")
        image_url = None

    return render_template("print.html", image_url=image_url)  # Return rendered template with image URL

if __name__ == '__main__':
    app.run(debug=True)