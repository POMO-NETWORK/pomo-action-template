from core.config import settings


class StaticFileService:

    dir = settings.PROJECT_ROOT / settings.STATIC_ROOT

    @classmethod
    def write_file(cls, file_name: str, data: str):
        with open(str(cls.dir / file_name), "w") as file:
            file.write(data)
