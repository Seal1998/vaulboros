import json

from vaulboros.api_client import ApiResponse
from vaulboros.api.base import BaseApi, VaultResponse
from vaulboros.api.kv import KvApi, Kv2Api

class MountApi(BaseApi):

    class MountContainer:

        def __init__(self, path, type, config, description, options):
            self.path = path
            self.type = type
            self.config = config
            self.description = description
            self.options = options

            self.api: BaseApi = None

        @property
        def json(self):
            return json.dumps(self.dict)
            
        @property
        def dict(self):
            return dict(
                path=self.path,
                type=self.type,
                config=self.config,
                options=self.options,
                description=self.description,
                api=True if self.api is not None else False
            )

        def __repr__(self) -> str:
            return f"{self.path} - {self.description}"
        
        def init_api_object(self, api_type: BaseApi, from_object: BaseApi, **kwargs):
            self.api = api_type.from_api_instance(from_object, **kwargs)

        @classmethod
        def from_sys_mounts_response(cls, response: ApiResponse, derive_from_api_object: BaseApi=None):
            mounts: list[cls] = []
            for raw_mount_path, raw_mount in response.content['data'].items():
                mount = cls(
                        path = raw_mount_path[:-1], # cut '/' at the end
                        type = raw_mount['type'],
                        config = raw_mount['config'],
                        description = raw_mount['description'],
                        options = raw_mount['options']
                    )
                
                if derive_from_api_object is not None:
                    if mount.type == 'kv':
                        if mount.options['version'] == "2":
                            mount.init_api_object(Kv2Api, derive_from_api_object, vault_kv_engine_path=mount.path)

                mounts.append(mount)
            return mounts

    def __init__(self, vault_url, vault_token=None, create_api_object_for_mount=True, **kwargs):
        super().__init__(vault_url, vault_token, vault_token_required=True, **kwargs)

        self.__mounts: dict = dict()
        self.create_api_object_for_mount = create_api_object_for_mount

    def __getitem__(self, mount_key) -> MountContainer:
        if mount_key in self.__mounts.keys():
            return self.__mounts[mount_key]

    def __contains__(self, mount_key) -> bool:
        if mount_key.split('/')[0] in self.__mounts.keys():
            return True
        else:
            False

    def __get_load_existing_mounts_request_params(self) -> dict:
        return dict(
            url=f"{self.vault_url}/v1/sys/mounts"
        )

    def __post_process_load_mounts_response(self, response: ApiResponse) -> dict[str, MountContainer]:
        mounts_derive_from_api_object = self if self.create_api_object_for_mount else None
        if response.status_code == 200:
            mounts = self.MountContainer.from_sys_mounts_response(response, derive_from_api_object=mounts_derive_from_api_object)

            for mount in mounts:
                self.__mounts[mount.path.split('/')[0]] = mount

        return self.__mounts

    def load_existing_mounts(self) -> VaultResponse:
        mounts_response: ApiResponse = self._get(**self.__get_load_existing_mounts_request_params())

        return VaultResponse(mounts_response, self.__post_process_load_mounts_response(mounts_response))
    
    @BaseApi.async_unavailable_fallback('load_existing_mounts')
    async def a_load_existing_mounts(self) -> VaultResponse:
        mounts_response: ApiResponse = await self._a_get(**self.__get_load_existing_mounts_request_params())

        return VaultResponse(mounts_response, self.__post_process_load_mounts_response(mounts_response))