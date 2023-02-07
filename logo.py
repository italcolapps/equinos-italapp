import base64
logo = 'Imagenes/banner_brio.jpg'
logo_encoded = base64.b64encode(open(logo, 'rb').read())
