#!/usr/bin/env python2
"""Command-line interface for the Ona API client.

Usage: cli.py (--client-args=vals) api-name api-method (--method-args=vals)

api-name:           The name of the Ona API to call.
                    E.g. forms

api-method:         The method to call on the Ona API.
                    E.g. list

--method-args:      (OPTIONAL) The arguments to pass into the Ona API method.
                    E.g. --owner=someone

--client-args:      (OPTIONAL) The arguments used to create the Ona API client.
                    If these are not set, they will be read from ~/onapierc.
                    E.g. --username=someone --password=secret
                    E.g. --api-token=123lkjoi123klj

"""
import ast
import codecs
import errno
import inspect
import json
import logging
import os
import re
import sys

from onapie.client import Client
from onapie.exceptions import ApiException


_ERR_MISSING_ARGUMENT = 1
_ERR_API_MISSING = 2
_ERR_API_UNKNOWN = 3
_ERR_METHOD_MISSING = 4
_ERR_METHOD_UNKNOWN = 5
_ERR_METHOD_BAD_ARGS = 6
_ERR_METHOD_BAD_CALL = 7

_LOG = logging.getLogger(__name__)
_LOG.addHandler(logging.StreamHandler())
_LOG.setLevel(logging.INFO)


def _default_client_config():
    """
    :rtype: dict[str,object]

    """
    return {
        'api_addr': 'https://api.ona.io',
    }


def _load_user_config(path, encoding='utf-8'):
    """
    :type path: str
    :type encoding: str
    :rtype: dict[str,object]

    """
    path = os.path.expanduser(path)
    try:
        with codecs.open(path, encoding=encoding) as config_file:
            config = json.load(config_file)
    except ValueError:
        _LOG.warning('ignoring non-json configuration file at %s', path)
        config = {}
    except IOError as exception:
        if exception.errno == errno.ENOENT:
            config = {}
        else:
            raise

    return config


def _is_option(arg):
    """
    :type arg: str
    :rtype: bool

    """
    return arg.startswith('--')


def _option_name_to_arg(option_name):
    """
    :type option_name: str
    :rtype: str

    >>> _option_name_to_arg('--foo')
    'foo'

    >>> _option_name_to_arg('--foo-bar')
    'foo_bar'

    """
    option_name = re.sub('^-*', '', option_name)
    option_name = re.sub('-', '_', option_name)
    return option_name


def _option_value_to_value(option_value):
    """
    :type option_value: str
    :rtype: object

    >>> _option_value_to_value('foo')
    'foo'

    >>> _option_value_to_value('123abc')
    '123abc'

    >>> _option_value_to_value('123')
    123

    """
    try:
        return ast.literal_eval(option_value)
    except (ValueError, SyntaxError):
        return str(option_value)


def _parse_next_option(args):
    """
    :type args: list[str]
    :rtype: (str,object) | None

    >>> args = ['--foo', 'bar', 'baz']
    >>> _parse_next_option(args)
    ('foo', 'bar')
    >>> args
    ['baz']

    >>> args = ['--foo=bar', 'baz']
    >>> _parse_next_option(args)
    ('foo', 'bar')
    >>> args
    ['baz']

    >>> args = ['--foo=123', 'baz']
    >>> _parse_next_option(args)
    ('foo', 123)
    >>> args
    ['baz']

    >>> args = ['baz']
    >>> _parse_next_option(args) is None
    True
    >>> args
    ['baz']

    """
    if len(args) < 1:
        return None

    next_option = args[0]
    if not _is_option(next_option):
        return None

    if '=' in next_option:
        option_name, option_value = args.pop(0).split('=')
    else:
        option_name = args.pop(0)
        try:
            option_value = args.pop(0)
        except IndexError:
            _LOG.error('missing value for argument %s', option_name)
            sys.exit(_ERR_MISSING_ARGUMENT)

    option_name = _option_name_to_arg(option_name)
    option_value = _option_value_to_value(option_value)
    return option_name, option_value


def _parse_options(args):
    """
    :type args: list[str]
    :rtype: dict[str,object]

    """
    options = {}
    while True:
        option = _parse_next_option(args)
        if not option:
            break

        option_name, option_value = option
        options[option_name] = option_value

    return options


def _parse_attr(obj, args, missing, unknown, available_getter):
    """
    :type obj: T
    :type args: list[str]
    :type missing: (str,int)
    :type unknown: (str,int)
    :type available_getter: T -> list[str]
    :rtype: object

    """
    try:
        action = args.pop(0)
    except IndexError:
        message, error = missing
        _LOG.error(message)
        sys.exit(error)

    try:
        action = getattr(obj, action)
    except AttributeError:
        message, error = unknown
        _LOG.error(message, action)
        _LOG.info('available are %s', _join(available_getter(obj), 'and'))
        sys.exit(error)

    return action


def _parse_attribute(obj, args, missing, unknown):
    """
    :type obj: object
    :type args: list[str]
    :type missing: (str,int)
    :type unknown: (str,int)
    :rtype: object

    """
    try:
        action = args.pop(0)
    except IndexError:
        message, error = missing
        _LOG.error(message)
        sys.exit(error)

    try:
        action = getattr(obj, action)
    except AttributeError:
        message, error = unknown
        _LOG.error(message, action)
        _LOG.info('available are %s', _join(dir(obj), 'and'))
        sys.exit(error)

    return action


def _get_method_arguments(method):
    """
    :type method: typing.FunctionType
    :rtype: list[str]

    >>> def foo(a, b=1): pass
    >>> _get_method_arguments(foo)
    ['a', 'b']

    >>> def foo(): pass
    >>> _get_method_arguments(foo)
    []

    """
    signature = inspect.getargspec(method)
    args = set()
    args.update(signature.args or [])
    args.update(signature.keywords or [])
    args.discard('self')
    return sorted(args)


def _join(items, separator):
    """
    :type items: list[str]
    :type separator: str
    :rtype: str

    >>> _join(['foo'], 'and')
    'foo'

    >>> _join(['foo', 'bar'], 'and')
    'foo and bar'

    >>> _join(['foo', 'bar', 'baz'], 'or')
    'foo, bar or baz'

    """
    if len(items) == 1:
        return items[0]

    return '%s %s %s' % (', '.join(items[:-1]), separator, items[-1])


def _public_methods(obj):
    """
    :type obj: object
    :rtype: list[str]

    """
    return sorted(method for method in dir(obj) if not method.startswith('_'))


def create_client(args, user_config_path):
    """
    :type args: list[str]
    :type user_config_path: str
    :rtype: onapie.client.Client

    """
    client_config = _default_client_config()
    client_config.update(_load_user_config(path=user_config_path))
    client_config.update(_parse_options(args))
    return Client(**client_config)


def get_api(args, client):
    """
    :type client: onapie.client.Client
    :type args: list[str]
    :rtype: object

    """
    def available_apis(obj):
        # todo: keep in sync with Client.fetch_catalog
        return ['forms', 'data', 'stats']

    missing = ('must specify an api to call on the client', _ERR_API_MISSING)
    unknown = ('api %s does not exist on the client', _ERR_API_UNKNOWN)
    return _parse_attr(client, args, missing, unknown, available_apis)


def get_method(args, api):
    """
    :type api: object
    :type args: list[str]
    :rtype: typing.FunctionType

    """
    missing = ('must specify a method to call on the api', _ERR_METHOD_MISSING)
    unknown = ('method %s does not exist on the api', _ERR_METHOD_UNKNOWN)
    return _parse_attr(api, args, missing, unknown, _public_methods)


def execute_action(args, method):
    """
    :type method: typing.FunctionType
    :type args: list[str]
    :rtype: object

    """
    provided_args = _parse_options(args)
    supported_args = _get_method_arguments(method)

    ignored_args = sorted(set(provided_args) - set(supported_args))
    if ignored_args:
        _LOG.info('ignoring extra argument(s): %s', _join(ignored_args, 'and'))
        for arg in ignored_args:
            provided_args.pop(arg)

    try:
        value = method(**provided_args)
    except ApiException as exception:
        _LOG.error(exception.msg)
        sys.exit(_ERR_METHOD_BAD_CALL)
    except TypeError as exception:
        _LOG.error(exception.message)
        _LOG.info('valid argument(s) are %s', _join(supported_args, 'or'))
        sys.exit(_ERR_METHOD_BAD_ARGS)

    return value


def print_help(args):
    """
    :type args: list[str]

    """
    if '-h' in args or '--help' in args:
        print(__doc__)
        sys.exit(0)


def display_result(value):
    # todo: implement pretty printing, e.g. lists as tables
    print(value)


def _main():
    args = sys.argv[1:]
    print_help(args)

    client = create_client(args, user_config_path='~/.onapierc')
    api = get_api(args, client)
    method = get_method(args, api)
    value = execute_action(args, method)
    display_result(value)


if __name__ == '__main__':
    _main()
