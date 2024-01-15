import os

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from github import Github

app = Flask(__name__)
cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/get-dibs')
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_dibs():
    try:
        github = Github(os.environ['GITHUB_TOKEN'])
        repo = github.get_repo('lib-it/lib-it.github.io')

        contents = repo.get_contents('')
        if not isinstance(contents, list):
            contents = [contents]

        files = {}
        for file_content in contents:
            files[file_content.name] = file_content.decoded_content

        return jsonify(success=True, files=files), 200
    except Exception as exception:
        return jsonify(success=False, error=str(exception))


@app.route('/call', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def deploy():
    try:
        data = request.json
        if data is None:
            return jsonify(success=False, error='No JSON data provided'), 400

        github = Github(os.environ['GITHUB_TOKEN'])
        repo = github.get_repo('lib-it/lib-it.github.io')

        for file_name, file_content in data['files'].items():
            repo.create_file(f"{data['name']}/{file_name}", 'Deploy', file_content)

        url = f"https://lib-it.github.io/{data['name']}"

        return jsonify(success=True, url=url), 200
    except Exception as exception:
        return jsonify(success=False, error=str(exception))

if __name__ == '__main__':
    app.run('0.0.0.0')
