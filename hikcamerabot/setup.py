import logging
from collections import defaultdict
from typing import Callable, Union

from pyrogram import filters
from pyrogram.handlers import MessageHandler

from hikcamerabot.camera import HikvisionCam
from hikcamerabot.camerabot import CameraBot
from hikcamerabot.commands import setup_commands
from hikcamerabot.config.config import get_main_config
from hikcamerabot.registry import CameraRegistry
from hikcamerabot.utils.utils import build_command_presentation


class BotSetup:
    """Setup everything before bot start."""

    def __init__(self) -> None:
        self._log = logging.getLogger(self.__class__.__name__)
        self._conf = get_main_config()
        self._bot = CameraBot()
        cam_registry = self._create_and_setup_cameras()
        self._bot.add_cam_registry(cam_registry)

    def _create_and_setup_cameras(self) -> CameraRegistry:
        """Create cameras and setup for the dispatcher.

        Iterate trough the config, create event queues per camera,
        setup camera registry and command callbacks (handlers).

        Hidden (undesirable) cameras will be excluded from the setup.
        """
        cam_registry = CameraRegistry()
        tpl_cmds, global_cmds = setup_commands()

        for cam_id, cam_conf in self._conf.camera_list.items():
            if cam_conf.hidden:
                # Ignore/skip camera and its settings.
                continue

            cam_cmds = defaultdict(list)
            for description, group in tpl_cmds.items():
                for cmd, callback in group['commands'].items():
                    cmd = cmd.format(cam_id)
                    cam_cmds[description].append(cmd)
                    self._setup_message_handler(callback, cmd)

            cam = HikvisionCam(id=cam_id, conf=cam_conf, bot=self._bot)
            cam_registry.add(
                cam=cam,
                commands=cam_cmds,
                commands_presentation=build_command_presentation(cam_cmds, cam),
            )

        self._setup_global_cmds(global_cmds)
        self._log.debug('Camera Meta Registry: %r', cam_registry)
        return cam_registry

    def _setup_message_handler(
        self, callback: Callable, cmd: Union[str, list[str]]
    ) -> None:
        self._bot.add_handler(
            MessageHandler(
                callback,
                filters=filters.user(self._bot.chat_users) & filters.command(cmd),
            )
        )

    def _setup_global_cmds(self, global_cmds: dict) -> None:
        """Set up global bot command callbacks (handlers) in place."""
        for cmd, callback in global_cmds.items():
            self._setup_message_handler(callback, cmd)

    def get_bot(self) -> CameraBot:
        return self._bot
