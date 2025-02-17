# class or fucntions
import json
import requests


def get_request(url, headers):
    get_response = requests.get(url=url, headers=headers)
    return get_response


def post_request(url, headers, payload, in_json):
    post_response = requests.post(url=url, headers=headers, data=json.dumps(payload))
    if in_json is True:
        return post_response.json()
    return post_response


def patch_requests(url, headers, payload, in_json):
    patch_response_data = requests.patch(url=url, headers=headers, data=json.dumps(payload))
    if in_json is True:
        return patch_response_data.json()
    return patch_response_data


def put_requests(url, headers, payload, in_json):
    put_response_data = requests.put(url=url, headers=headers, data=json.dumps(payload))
    if in_json is True:
        return put_response_data.json()
    return put_response_data


def delete_requests(url, headers, in_json):
    delete_response_data = requests.delete(url=url, headers=headers)
    if in_json is True:
        return delete_response_data.json()
    return delete_response_data
