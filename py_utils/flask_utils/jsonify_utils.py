from flask import jsonify


def jsonify_response(data_tuple: tuple):
    data = data_tuple[0]
    message = data_tuple[-1]
    if data:
        return success_with_msg_response(message=message, data=data)
    return error_response(message, data)


def error_response(message: str, data=None, code=404):
    return jsonify({'status': False, 'message': message, 'data': data}), code


def unauthorized_response(message: str = ''):
    return jsonify({'status': False, 'message': message, }), 401


def success_with_msg_response(message: str, data):
    return jsonify({'status': True, 'message': message, 'data': data}), 200


def success_response(data):
    return jsonify({'status': True, 'message': '', 'data': data}), 200
