"""
    Alan's Speakeasy

    API for Alan's Speakeasy, Version 0.1  # noqa: E501

    The version of the OpenAPI document: 0.1
    Generated by: https://openapi-generator.tech
"""

import re  # noqa: F401
import sys  # noqa: F401

from speakeasypy.openapi.client.api_client import ApiClient, Endpoint as _Endpoint
from speakeasypy.openapi.client.model.chat_message_reaction import ChatMessageReaction
from speakeasypy.openapi.client.model.chat_room_list import ChatRoomList
from speakeasypy.openapi.client.model.chat_room_state import ChatRoomState
from speakeasypy.openapi.client.model.success_status import SuccessStatus
from speakeasypy.openapi.client.model_utils import (  # noqa: F401
    check_allowed_values,
    check_validations,
    date,
    datetime,
    file_type,
    none_type,
    validate_and_convert_types
)


class ChatApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

        def __get_api_room_with_roomid_with_since(
                self,
                room_id,
                since,
                **kwargs
        ):
            """Get state and all messages for a chat room since a specified time  # noqa: E501

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.get_api_room_with_roomid_with_since(room_id, since, async_req=True)
            >>> result = thread.get()

            Args:
                room_id (str): Id of the Chatroom
                since (int): Timestamp for new messages

            Keyword Args:
                session (str): Session Token. [optional]
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (int/float/tuple): timeout setting for this request. If
                    one number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                ChatRoomState
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['room_id'] = \
                room_id
            kwargs['since'] = \
                since
            return self.call_with_http_info(**kwargs)

        self.get_api_room_with_roomid_with_since = _Endpoint(
            settings={
                'response_type': (ChatRoomState,),
                'auth': [],
                'endpoint_path': '/api/room/{roomId}/{since}',
                'operation_id': 'get_api_room_with_roomid_with_since',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'room_id',
                    'since',
                    'session',
                ],
                'required': [
                    'room_id',
                    'since',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'room_id':
                        (str,),
                    'since':
                        (int,),
                    'session':
                        (str,),
                },
                'attribute_map': {
                    'room_id': 'roomId',
                    'since': 'since',
                    'session': 'session',
                },
                'location_map': {
                    'room_id': 'path',
                    'since': 'path',
                    'session': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client,
            callable=__get_api_room_with_roomid_with_since
        )

        def __get_api_rooms(
                self,
                **kwargs
        ):
            """Lists all Chatrooms for current user  # noqa: E501

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.get_api_rooms(async_req=True)
            >>> result = thread.get()


            Keyword Args:
                session (str): Session Token. [optional]
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (int/float/tuple): timeout setting for this request. If
                    one number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                ChatRoomList
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            return self.call_with_http_info(**kwargs)

        self.get_api_rooms = _Endpoint(
            settings={
                'response_type': (ChatRoomList,),
                'auth': [],
                'endpoint_path': '/api/rooms',
                'operation_id': 'get_api_rooms',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'session',
                ],
                'required': [],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'session':
                        (str,),
                },
                'attribute_map': {
                    'session': 'session',
                },
                'location_map': {
                    'session': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client,
            callable=__get_api_rooms
        )

        def __post_api_room_with_roomid(
                self,
                room_id,
                **kwargs
        ):
            """Post a message to a Chatroom.  # noqa: E501

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.post_api_room_with_roomid(room_id, async_req=True)
            >>> result = thread.get()

            Args:
                room_id (str): Id of the Chatroom

            Keyword Args:
                session (str): Session Token. [optional]
                body (str): [optional]
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (int/float/tuple): timeout setting for this request. If
                    one number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                SuccessStatus
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['room_id'] = \
                room_id
            return self.call_with_http_info(**kwargs)

        self.post_api_room_with_roomid = _Endpoint(
            settings={
                'response_type': (SuccessStatus,),
                'auth': [],
                'endpoint_path': '/api/room/{roomId}',
                'operation_id': 'post_api_room_with_roomid',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'room_id',
                    'session',
                    'body',
                ],
                'required': [
                    'room_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'room_id':
                        (str,),
                    'session':
                        (str,),
                    'body':
                        (str,),
                },
                'attribute_map': {
                    'room_id': 'roomId',
                    'session': 'session',
                },
                'location_map': {
                    'room_id': 'path',
                    'session': 'query',
                    'body': 'body',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [
                    'text/plain'
                ]
            },
            api_client=api_client,
            callable=__post_api_room_with_roomid
        )

        def __post_api_room_with_roomid_reaction(
                self,
                room_id,
                **kwargs
        ):
            """Post a chat message reaction to a Chatroom.  # noqa: E501

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.post_api_room_with_roomid_reaction(room_id, async_req=True)
            >>> result = thread.get()

            Args:
                room_id (str): Id of the Chatroom

            Keyword Args:
                session (str): Session Token. [optional]
                chat_message_reaction (ChatMessageReaction): [optional]
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (int/float/tuple): timeout setting for this request. If
                    one number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                SuccessStatus
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['room_id'] = \
                room_id
            return self.call_with_http_info(**kwargs)

        self.post_api_room_with_roomid_reaction = _Endpoint(
            settings={
                'response_type': (SuccessStatus,),
                'auth': [],
                'endpoint_path': '/api/room/{roomId}/reaction',
                'operation_id': 'post_api_room_with_roomid_reaction',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'room_id',
                    'session',
                    'chat_message_reaction',
                ],
                'required': [
                    'room_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'room_id':
                        (str,),
                    'session':
                        (str,),
                    'chat_message_reaction':
                        (ChatMessageReaction,),
                },
                'attribute_map': {
                    'room_id': 'roomId',
                    'session': 'session',
                },
                'location_map': {
                    'room_id': 'path',
                    'session': 'query',
                    'chat_message_reaction': 'body',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client,
            callable=__post_api_room_with_roomid_reaction
        )
