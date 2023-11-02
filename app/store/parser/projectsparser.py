from abc import ABCMeta, abstractmethod


class ProjectsParser(metaclass=ABCMeta):
    @abstractmethod
    async def get_new_projects(self):
        raise NotImplementedError
