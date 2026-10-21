import io
import base64
import re
from urllib.parse import urlparse

from flask import Flask, render_template, request
import qrcode
from PIL import Image

app = Flask(__name__)

URL_REGEX = re.compile(r'^(https?://\S+)$')

COLOR_SCHEMES = {
    'red_black':   {'fill': 'red',     'back': 'black'},
    'black_white': {'fill': 'black',   'back': 'white'},
    'green_black': {'fill': '#00FF00', 'back': 'black'},
    'green_white': {'fill': '#00FF00', 'back': 'white'}
}

def is_valid_url(url: str) -> bool:
    if not url or not URL_REGEX.match(url):
        return False
    parsed = urlparse(url)
    return bool(parsed.scheme) and bool(parsed.netloc)

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_scheme = 'red_black'
    
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        selected_scheme = request.form.get('color_scheme', 'red_black')
        
        if not is_valid_url(url):
            return render_template('temp.html', error='Invalid URL. Include http:// or https://', selected_scheme=selected_scheme)
            
        scheme = COLOR_SCHEMES.get(selected_scheme, COLOR_SCHEMES['red_black'])
        
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
        qr.add_data(url)
        qr.make(fit=True)
        img: Image.Image = qr.make_image(fill_color=scheme['fill'], back_color=scheme['back'])
        
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        return render_template('temp.html', img_data=img_b64, url=url, selected_scheme=selected_scheme)
        
    return render_template('temp.html', selected_scheme=selected_scheme)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
