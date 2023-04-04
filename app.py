import argparse
import binascii
import io

from flask import Flask, request, render_template, jsonify, redirect, url_for
from werkzeug.exceptions import BadRequest

import warn_old_config
from derive import derive_tag_key, derive_undiversified_key
from config import SDMMAC_PARAM, ENC_FILE_DATA_PARAM, ENC_PICC_DATA_PARAM, SYSTEM_MASTER_KEY, UID_PARAM, CTR_PARAM, REQUIRE_LRP
from libsdm import decrypt_sun_message, validate_plain_sun, InvalidMessage, EncMode, ParamMode

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.errorhandler(400)
def handler_bad_request(e):
    return render_template('error.html', code=400, msg=str(e)), 400


@app.errorhandler(403)
def handler_forbidden(e):
    return render_template('error.html', code=403, msg=str(e)), 403


@app.errorhandler(404)
def handler_not_found(e):
    return render_template('error.html', code=404, msg=str(e)), 404


@app.context_processor
def inject_demo_mode():
    demo_mode = (SYSTEM_MASTER_KEY == (b"\x00" * 16))
    return {"demo_mode": demo_mode}


@app.route('/')
def sdm_main():
    """
    Main page with a few examples.
    """
    return render_template('sdm_main.html')


@app.route('/auto_auth')
def auto_auth():
    """
    Automatically authenticate the user and redirect to another route.
    """
    try:
        _internal_sdm()
        # Redirect to your desired route after successful authentication
        return redirect(url_for('authenticated_route'))
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400


@app.route('/authenticated_route')
def authenticated_route():
    """
    The route where the user will be redirected after successful authentication.
    """
    # Add your logic here
    return render_template('authenticated_route.html')

@app.route('/authenticated')
def authenticated_route():
    return render_template('authenticated_route.html')

# Keep the rest of the code as is
# ...

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='OTA NFC Server')
    parser.add_argument('--host', type=str, nargs='?',
                        help='address to listen on')
    parser.add_argument('--port', type=int, nargs='?',
                        help='port to listen on')

    args = parser.parse_args()

    app.run(host=args.host, port=args.port)
