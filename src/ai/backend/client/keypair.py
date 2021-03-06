from typing import Iterable, Sequence, Union

from .base import api_function
from .request import Request

__all__ = (
    'KeyPair',
)


class KeyPair:
    '''
    Provides interactions with keypairs.
    '''

    session = None
    '''The client session instance that this function class is bound to.'''

    @api_function
    @classmethod
    async def create(cls, user_id: Union[int, str],
                     is_active: bool = True,
                     is_admin: bool = False,
                     resource_policy: str = None,
                     rate_limit: int = None,
                     concurrency_limit: int = None,
                     fields: Iterable[str] = None) -> dict:
        '''
        Creates a new keypair with the given options.
        You need an admin privilege for this operation.
        '''
        if fields is None:
            fields = ('access_key', 'secret_key')
        uid_type = 'Int!' if isinstance(user_id, int) else 'String!'
        q = 'mutation($user_id: {0}, $input: KeyPairInput!) {{'.format(uid_type) + \
            '  create_keypair(user_id: $user_id, props: $input) {' \
            '    ok msg keypair { $fields }' \
            '  }' \
            '}'
        q = q.replace('$fields', ' '.join(fields))
        variables = {
            'user_id': user_id,
            'input': {
                'is_active': is_active,
                'is_admin': is_admin,
                'resource_policy': resource_policy,
                'rate_limit': rate_limit,
                'concurrency_limit': concurrency_limit,
            },
        }
        rqst = Request(cls.session, 'POST', '/admin/graphql')
        rqst.set_json({
            'query': q,
            'variables': variables,
        })
        async with rqst.fetch() as resp:
            data = await resp.json()
            return data['create_keypair']

    @api_function
    @classmethod
    async def list(cls, user_id: Union[int, str] = None,
                   is_active: bool = None,
                   fields: Iterable[str] = None) -> Sequence[dict]:
        '''
        Lists the keypairs.
        You need an admin privilege for this operation.
        '''
        if fields is None:
            fields = (
                'access_key', 'secret_key',
                'is_active', 'is_admin',
            )
        if user_id is None:
            q = 'query($is_active: Boolean) {' \
                '  keypairs(is_active: $is_active) {' \
                '    $fields' \
                '  }' \
                '}'
        else:
            uid_type = 'Int!' if isinstance(user_id, int) else 'String!'
            q = 'query($user_id: {0}, $is_active: Boolean) {{'.format(uid_type) + \
                '  keypairs(user_id: $user_id, is_active: $is_active) {' \
                '    $fields' \
                '  }' \
                '}'
        q = q.replace('$fields', ' '.join(fields))
        variables = {
            'is_active': is_active,
        }
        if user_id is not None:
            variables['user_id'] = user_id
        rqst = Request(cls.session, 'POST', '/admin/graphql')
        rqst.set_json({
            'query': q,
            'variables': variables,
        })
        async with rqst.fetch() as resp:
            data = await resp.json()
            return data['keypairs']

    def __init__(self, access_key: str):
        self.access_key = access_key

    @api_function
    async def info(self, fields: Iterable[str] = None) -> dict:
        '''
        Returns the keypair's information such as resource limits.

        :param fields: Additional per-agent query fields to fetch.

        .. versionadded:: 18.12
        '''
        if fields is None:
            fields = (
                'access_key', 'secret_key',
                'is_active', 'is_admin',
            )
        q = 'query {' \
            '  keypair {' \
            '    $fields' \
            '  }' \
            '}'
        q = q.replace('$fields', ' '.join(fields))
        rqst = Request(self.session, 'POST', '/admin/graphql')
        rqst.set_json({
            'query': q,
        })
        async with rqst.fetch() as resp:
            data = await resp.json()
            return data['keypair']

    @api_function
    async def activate(self):
        '''
        Activates this keypair.
        You need an admin privilege for this operation.
        '''
        raise NotImplementedError

    @api_function
    async def deactivate(self):
        '''
        Deactivates this keypair.
        Deactivated keypairs cannot make any API requests
        unless activated again by an administrator.
        You need an admin privilege for this operation.
        '''
        raise NotImplementedError
