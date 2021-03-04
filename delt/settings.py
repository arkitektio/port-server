from delt.service.types import Service, ServiceType
from django.conf import settings



class DeltSettings:

    def __init__(self) -> None:
        self.api_version = 0.1

        self.inward = settings.DELT["INWARD"]
        self.outward = settings.DELT["OUTWARD"]
        self.type = settings.DELT["TYPE"]
        self.port = settings.DELT["PORT"]


        self.service_dict = settings.ARKITEKT_SERVICE





        
    @property
    def service(self):
        dc = self.service_dict
        return Service(types=dc["TYPES"], outward=dc["OUTWARD"], inward=dc["INWARD"], port=dc["PORT"], dependencies=dc["DEPENDENCIES"], name=dc["NAME"], version=dc["VERSION"])




ACTIVE_DELT_SETTINGS = None

def get_active_settings():
    global ACTIVE_DELT_SETTINGS
    if ACTIVE_DELT_SETTINGS is None:
        ACTIVE_DELT_SETTINGS = DeltSettings()
    return ACTIVE_DELT_SETTINGS