from vaulboros.api_client import ApiResponse
from vaulboros.api.token import VaultToken
from vaulboros.api.base import BaseApi, VaultResponse

# логин и управление approle auth engine

class ApproleApi(BaseApi):
    
    def __init__(self, vault_url, vault_token=None, vault_approle_mount_path='approle', **kwargs):
        self.approle_mount = vault_approle_mount_path
        super().__init__(vault_url, vault_token=vault_token, **kwargs)

    def __get_login_request_params(self, role_id, secret_id) -> dict:
        return dict(
            url=f"{self.vault_url}/v1/auth/{self.approle_mount}/login",
            data={
                "role_id": role_id,
                "secret_id": secret_id
            }
        )

    def __post_process_login_response(self, response: ApiResponse, persist_token=True):
        if response.status_code == 200:
            vault_token = VaultToken.from_api_response(response)

            if vault_token:
                if persist_token:
                    self.persist_api_token(vault_token)

            return vault_token

    def login(self, role_id, secret_id, **kwargs) -> VaultResponse:
        login_response: ApiResponse = self._post(**self.__get_login_request_params(role_id, secret_id))

        return VaultResponse(login_response, self.__post_process_login_response(login_response, **kwargs))
    
    @BaseApi.async_unavailable_fallback('login')
    async def a_login(self, role_id, secret_id, **kwargs) -> VaultResponse:
        login_response: ApiResponse = await self._a_post(**self.__get_login_request_params(role_id, secret_id))

        return VaultResponse(login_response, self.__post_process_login_response(login_response, **kwargs))