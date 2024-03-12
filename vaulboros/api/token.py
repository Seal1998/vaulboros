from vaulboros.api_client import ApiResponse
from vaulboros.api.base import BaseApi, VaultToken
    
class TokenApi(BaseApi):

    def __init__(self, vault_url, vault_token: VaultToken=None, **kwargs):
        super().__init__(vault_url=vault_url, vault_token=vault_token, vault_token_required=True)