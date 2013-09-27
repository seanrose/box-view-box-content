from flask import Flask, jsonify, request, redirect
import requests
import time
import settings as s


app = Flask(__name__)


@app.route('/')
def hello():

    root_folder_files = get_folder_files()

    return jsonify(root_folder_files)


@app.route('/view')
def view():

    boxcloud_link = get_boxcloud_for_file(request.args.get('file_id'))

    print boxcloud_link

    payload = {'url': boxcloud_link}

    documents_resource = '/documents'
    url = s.VIEW_API_URL + documents_resource
    auth = {'Authorization': 'Token {}'.format(s.VIEW_API_KEY)}

    api_response = requests.post(url, headers=auth, data=payload).json()
    document_id = api_response['id']
    
    # TODO(seanrose): actually check the document status instead of sleeping for an arbitrary time
    time.sleep(12)

    payload = {'document_id': document_id}
    sessions_resource = '/sessions'
    url = s.VIEW_API_URL + sessions_resource

    api_response = requests.post(url, headers=auth, data=payload).json()
    session_id = api_response['id']

    # TODO(seanrose): make the view base url in settings.py usable here
    view_base_url = 'https://view-api.box.com/view/'
    view_url = '{}{}'.format(view_base_url, session_id)

    return redirect(view_url)


def get_folder_items(folder_id=0):

    folders_resource = '/folders/{}/items'.format(folder_id)
    url = s.CONTENT_API_URL + folders_resource
    auth = {'Authorization': 'Bearer {}'.format(s.CONTENT_TOKEN)}

    api_response = requests.get(url, headers=auth).json()

    return api_response


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
    auth = {'Authorization': 'Bearer {}'.format(s.CONTENT_TOKEN)}

    api_response = requests.get(url, headers=auth, allow_redirects=False)
    boxcloud_link = api_response.headers['Location']

    return boxcloud_link

if __name__ == '__main__':
    app.debug = True
    app.run()
