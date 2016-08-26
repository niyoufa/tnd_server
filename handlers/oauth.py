# -*- coding: utf-8 -*-

"""
    alter by: youfaNi
    alter on 2016-07-13
"""
import json,pdb
import oauth2
import oauth2.tokengenerator
import oauth2.grant
import oauth2.store.redisdb
import oauth2.store.mongodb
from oauth2.web.tornado import OAuth2Handler
import json
import time
import pymongo
import renren.libs.utils as utils
import renren.model.oauth as oauth
import renren.libs.utils as utils
import renren.authority as Authority

auth_provider = None
def init_oauth(*args,**options):
    global auth_provider
    if auth_provider :
        return auth_provider
    # Populate mock
    oauth_model = oauth.OauthModel()
    coll = oauth_model.get_coll()
    client_store = oauth2.store.mongodb.ClientStore(coll)

    # Redis for tokens storage
    token_store = oauth2.store.redisdb.TokenStore(rs=utils.Redis())

    # Generator of tokens
    token_generator = oauth2.tokengenerator.Uuid4()
    token_generator.expires_in[oauth2.grant.ClientCredentialsGrant.grant_type] = 3600 * 24

    # OAuth2 controller
    auth_provider = oauth2.Provider(
        access_token_store=token_store,
        auth_code_store=token_store,
        client_store=client_store,
        token_generator=token_generator
    )
    # auth_controller.token_path = '/oauth/token'

    default_scope = "font-api" # token默认具有的权限 默认具有前端访问权限
    scopes = ["font-api","back-api","system-api"] # token 可获得的权限
    # Add Client Credentials to OAuth2 controller
    auth_provider.add_grant(oauth2.grant.ClientCredentialsGrant(default_scope=default_scope,scopes=scopes))

    return auth_provider

handlers = [
                (r'/token', OAuth2Handler,init_oauth()),
            ]
