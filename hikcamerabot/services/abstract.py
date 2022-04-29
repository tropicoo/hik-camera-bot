import abc
import logging
from typing import Optional, TYPE_CHECKING

from hikcamerabot.enums import Alarm, Detection, Stream
from hikcamerabot.event_engine.queue import get_result_queue

if TYPE_CHECKING:
    from hikcamerabot.camera import HikvisionCam
    from hikcamerabot.services.alarm import AlarmService
    from hikcamerabot.services.stream.abstract import AbstractStreamService


class AbstractService(metaclass=abc.ABCMeta):
    """Base Service Class."""

    name: Optional[Detection] = None
    type: Optional[Alarm | Stream] = None

    def __init__(self, cam: 'HikvisionCam') -> None:
        self._log = logging.getLogger(self.__class__.__name__)
        self._cls_name = self.__class__.__name__
        self.cam = cam

    def __str__(self) -> str:
        return self._cls_name

    @abc.abstractmethod
    async def start(self) -> None:
        pass

    @abc.abstractmethod
    async def stop(self) -> None:
        pass

    @property
    @abc.abstractmethod
    def started(self) -> bool:
        pass

    @property
    @abc.abstractmethod
    def enabled_in_conf(self) -> bool:
        pass


ServiceTypeType = 'AbstractStreamService | AbstractService | AlarmService'


class AbstractServiceTask(abc.ABC):
    type: Optional[str] = None
    _event_manager_cls = None

    def __init__(self, service: ServiceTypeType, run_forever: bool = False) -> None:
        self._log = logging.getLogger(self.__class__.__name__)
        self._run_forever = run_forever
        self.service = service
        self._cam = service.cam
        self._bot = self._cam.bot
        self._cls_name = self.__class__.__name__
        self._result_queue = get_result_queue()

    @abc.abstractmethod
    async def run(self) -> None:
        """Main async task entry point."""
        pass
