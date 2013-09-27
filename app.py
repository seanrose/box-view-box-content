from flask import Flask, jsonify, redirect
import requests
import time
import settings as s
import json


app = Flask(__name__)


@app.route('/')
def hello():

    try:
        root_folder_files = get_folder_files()
    except Exception as ex:
        return 'There was a problem using the Box Content API: {}'.format(ex.message), 500

    return jsonify(root_folder_files)


@app.route('/view/<file_id>')
def view(file_id):

    try:
        boxcloud_link = get_boxcloud_for_file(file_id)
    except Exception as ex:
        return 'There was a problem using the Box Content API: {}'.format(ex.message), 500

    headers = {
        'Authorization': 'Token {}'.format(s.VIEW_API_KEY),
        'Content-Type': 'application/json',
    }

    documents_resource = '/documents'
    url = s.VIEW_API_URL + documents_resource
    data = json.dumps({'url': boxcloud_link})

    api_response = requests.post(url, headers=headers, data=data)
    document_id = api_response.json()['id']
    
    for i in range(30):
        document_resource = '{}/{}'.format(documents_resource, document_id)
        url = s.VIEW_API_URL + document_resource
        api_response = requests.get(url, headers=headers)
        status = api_response.json()['status']
        if status == 'done':
            break
        elif status == 'error':
            break
        else:
            time.sleep(1)

    if status != 'done':
        return 'There was a problem generating a preview for this document', 500

    sessions_resource = '/sessions'
    url = s.VIEW_API_URL + sessions_resource
    data = json.dumps({'document_id': document_id})

    api_response = requests.post(url, headers=headers, data=data)
    session_id = api_response.json()['id']

    # TODO(seanrose): make the view base url in settings.py usable here
    view_base_url = 'https://view-api.box.com/view'
    view_url = '{}/{}'.format(view_base_url, session_id)

    return redirect(view_url)


def get_folder_items(folder_id=0):

    folders_resource = '/folders/{}/items'.format(folder_id)
    url = s.CONTENT_API_URL + folders_resource
    auth = {'Authorization': 'Bearer {}'.format(s.CONTENT_ACCESS_TOKEN)}

    api_response = requests.get(url, headers=auth)
    api_response.raise_for_status()

    return api_response.json()


def get_folder_files(folder_id=0):

    folder_items = get_folder_items(folder_id)

    folder_files = [
        item for item in folder_items['entries'] if item['type'] == 'file'
    ]

    folder_items['entries'] = folder_files
    folder_items['total_count'] = len(folder_files)

    return folder_items


def get_boxcloud_for_file(file_id):

    files_resource = '/files/{}/content'.format(file_id)
    url = s.CONTENT_API_URL + files_resource
    auth = {'Authorization': 'Bearer {}'.format(s.CONTENT_ACCESS_TOKEN)}

    api_response = requests.get(url, headers=auth, allow_redirects=False)
    api_response.raise_for_status()

    boxcloud_link = api_response.headers['Location']

    return boxcloud_link


if __name__ == '__main__':
    app.debug = True
    app.run()
