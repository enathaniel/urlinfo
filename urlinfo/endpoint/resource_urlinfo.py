from flask import Flask, Blueprint, current_app, jsonify, request
import urllib
from ..model import UrlInfoParams, UrlInfo, UrlInfoRepository, db

bp = Blueprint('resource_urlinfo', __name__)

@bp.route('/urlinfo/1/<host_and_port>/')
@bp.route('/urlinfo/1/<host_and_port>/<path:original_path_query_string>')
def get(host_and_port, original_path_query_string=None):
    url_info_param = UrlInfoParams(request.path, request.full_path, host_and_port, original_path_query_string)
    current_app.logger.info("urlinfoparam: " + str(url_info_param))
    url_info = url_info_param.to_urlinfo()
    current_app.logger.info("urlinfo: " + str(url_info))
    print(current_app.config['HASHRING'][url_info.url])
    db.choose_tenant(current_app.config['HASHRING'][url_info.url])
    repository = UrlInfoRepository(db.session)
    found = repository.get(url_info)
    current_app.logger.info("found: " + str(found))
    return jsonify({'malware': found.malware})