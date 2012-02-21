from flask import Flask, request, redirect

import json
import urlparse


app = Flask(__name__)

@app.route('/authorize')
def authorize():
	'bounce the browser back to the URL passed in "redirect_uri", adding a static "code"'
	redirect_uri = request.args['redirect_uri']
	redirect_uri += '?code=12345&state='
	return redirect(redirect_uri)

@app.route('/access', methods=['POST'])
def token():
	'verify that the correct "code" was provided, and then return access and refresh tokens'
	if request.form['code'] == '12345':
		# everything checks out, return a json blob
		return json.dumps({
			'access_token': 'abcd',
			'refresh_token': 'efgh',
			'expires': 3600,
		})

	# complain about the code provided
	return json.dumps({
		'error': 'invalid_grant',
	})

if __name__ == '__main__':
	app.run(port=8001, debug=True)