# Flask QR‑code generator – corrected version (comments show original errors)
import io
import base64
import re
from urllib.parse import urlparse

from flask import Flask, render_template, request
import qrcode
from PIL import Image

app = Flask(__name__)

# Fixed typo in variable name and corrected regex (single back‑slash for \S)
URL_REGEX = re.compile(r'^(https?://\S+)$')

# Fixed return‑type annotation syntax (use ->, not -\u003e)
def is_valid_url(url: str) -> bool:
    if not url or not URL_REGEX.match(url):
        return False
    parsed = urlparse(url)
    return bool(parsed.scheme) and bool(parsed.netloc)

# HTTP method names must be uppercase; also match case when checking request.method
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        if not is_valid_url(url):
            # Fixed typo: render_template (was reder_template)
            return render_template('temp.html', error='Invalid URL. Include http:// or https://')
        # QR generation – keep original colour scheme (red on black) as user requested
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
        qr.add_data(url)
        qr.make(fit=True)
        img: Image.Image = qr.make_image(fill_color='red', back_color='black')
        # Create an in‑memory buffer before saving the image (was missing)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        return render_template('temp.html', img_data=img_b64, url=url)
    return render_template('temp.html')

if __name__ == '__main__':
    # Boolean literals are capitalised (True, not true)
    app.run(host='0.0.0.0', port=5000, debug=True)
