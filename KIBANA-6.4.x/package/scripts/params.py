# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Kibana Params configurations
"""

from resource_management.libraries.functions.version import format_hdp_stack_version, compare_versions
from resource_management import *
import status_params
import os

config = Script.get_config()

java64_home = config['hostLevelParams']['java_home']
hostname = config['hostname']


# kibana env
kibana_user = config['configurations']['kibana-env']['kibana.user']
kibana_group = config['configurations']['kibana-env']['kibana.group']
kibana_base_dir = config['configurations']['kibana-env']['kibana.base.dir']
kibana_download_url = config['configurations']['kibana-env']['kibana.download.url']


# kibana config
server_host = config['configurations']['kibana-config']['server.host']
server_port = config['configurations']['kibana-config']['server.port']
server_name = config['configurations']['kibana-config']['server.name']
server_basePath = config['configurations']['kibana-config']['server.basePath']
if server_basePath == 'none' or not server_basePath:
    server_basePath = '#server.basePath: ' + server_basePath
else:
    server_basePath = 'server.basePath: ' + server_basePath

server_rewriteBasePath = config['configurations']['kibana-config']['server.rewriteBasePath']
if server_rewriteBasePath is True:
    server_rewriteBasePath = 'true'
else:
    server_rewriteBasePath = 'false'
server_maxPayloadBytes = config['configurations']['kibana-config']['server.maxPayloadBytes']
elasticsearch_url = config['configurations']['kibana-config']['elasticsearch.url']
elasticsearch_preserveHost = config['configurations']['kibana-config']['elasticsearch.preserveHost']
if elasticsearch_preserveHost is True or elasticsearch_preserveHost is True:
    elasticsearch_preserveHost = 'true'
else:
    elasticsearch_preserveHost = 'false'
kibana_index = config['configurations']['kibana-config']['kibana.index']
kibana_defaultAppId = config['configurations']['kibana-config']['kibana.defaultAppId']
elasticsearch_username = config['configurations']['kibana-config']['elasticsearch.username']
elasticsearch_password = config['configurations']['kibana-config']['elasticsearch.password']
server_ssl_enabled = config['configurations']['kibana-config']['server.ssl.enabled']

if server_ssl_enabled is True:
    server_ssl_enabled = 'true'
    server_ssl_certificate = 'server.ssl.certificate: ' + config['configurations']['kibana-config']['server.ssl.certificate']
    server_ssl_key = 'server.ssl.key: ' + config['configurations']['kibana-config']['server.ssl.key']
else:
    server_ssl_enabled = 'false'
    server_ssl_certificate = '#server.ssl.certificate: ' + config['configurations']['kibana-config']['server.ssl.certificate']
    server_ssl_key = '#server.ssl.key: ' + config['configurations']['kibana-config']['server.ssl.key']

elasticsearch_ssl_certificate = config['configurations']['kibana-config']['elasticsearch.ssl.certificate']
if elasticsearch_ssl_certificate == 'none' or not elasticsearch_ssl_certificate:
    elasticsearch_ssl_certificate = '#elasticsearch.ssl.certificate: ' + elasticsearch_ssl_certificate
else:
    elasticsearch_ssl_certificate = 'elasticsearch.ssl.certificate: ' + elasticsearch_ssl_certificate

elasticsearch_ssl_key = config['configurations']['kibana-config']['elasticsearch.ssl.key']
if elasticsearch_ssl_key == 'none' or not elasticsearch_ssl_key:
    elasticsearch_ssl_key = '#elasticsearch.ssl.key: ' + elasticsearch_ssl_key
else:
    elasticsearch_ssl_key = 'elasticsearch.ssl.key: ' + elasticsearch_ssl_key

elasticsearch_ssl_certificateAuthorities = config['configurations']['kibana-config']['elasticsearch.ssl.certificateAuthorities']
if elasticsearch_ssl_certificateAuthorities == 'none' or not elasticsearch_ssl_certificateAuthorities or elasticsearch_ssl_certificateAuthorities == '[]':
    elasticsearch_ssl_certificateAuthorities = '#elasticsearch.ssl.certificateAuthorities: ' + elasticsearch_ssl_certificateAuthorities
else:
    elasticsearch_ssl_certificateAuthorities = 'elasticsearch.ssl.certificateAuthorities: ' + elasticsearch_ssl_certificateAuthorities

elasticsearch_ssl_verificationMode = config['configurations']['kibana-config']['elasticsearch.ssl.verificationMode']
elasticsearch_pingTimeout = config['configurations']['kibana-config']['elasticsearch.pingTimeout']
elasticsearch_requestTimeout = config['configurations']['kibana-config']['elasticsearch.requestTimeout']
elasticsearch_requestHeadersWhitelist = config['configurations']['kibana-config']['elasticsearch.requestHeadersWhitelist'] #list
elasticsearch_customHeaders = config['configurations']['kibana-config']['elasticsearch.customHeaders']
elasticsearch_shardTimeout = config['configurations']['kibana-config']['elasticsearch.shardTimeout']
elasticsearch_startupTimeout = config['configurations']['kibana-config']['elasticsearch.startupTimeout']
elasticsearch_logQueries = config['configurations']['kibana-config']['elasticsearch.logQueries']
if elasticsearch_logQueries is True:
    elasticsearch_logQueries = 'true'
else:
    elasticsearch_logQueries = 'false'
pid_file_dir = config['configurations']['kibana-env']['pid.file.dir']
pid_file = pid_file_dir + '/kibana.pid'
logging_dest_dir = config['configurations']['kibana-config']['logging.dest.dir']
logging_dest = logging_dest_dir + '/kibana.log'
logging_silent = config['configurations']['kibana-config']['logging.silent']
if logging_silent is True:
    logging_silent = 'true'
else:
    logging_silent = 'false'
logging_quiet = config['configurations']['kibana-config']['logging.quiet']
if logging_quiet is True:
    logging_quiet = 'true'
else:
    logging_quiet = 'false'
logging_verbose = config['configurations']['kibana-config']['logging.verbose']
if logging_verbose is True:
    logging_verbose = 'true'
else:
    logging_verbose = 'false'
ops_interval = config['configurations']['kibana-config']['ops.interval']
i18n_defaultLocale = config['configurations']['kibana-config']['i18n.defaultLocale']


