from typing import Annotated

from pydantic import AfterValidator

from hikcamerabot.config.schemas._validators import (
    int_min_0,
    int_min_1,
    int_min_minus_1,
    validate_ffmpeg_loglevel,
    validate_python_log_level,
)

IntMin1 = Annotated[int, AfterValidator(int_min_1)]
IntMin0 = Annotated[int, AfterValidator(int_min_0)]
IntMinus1 = Annotated[int, AfterValidator(int_min_minus_1)]

FfmpegLogLevel = Annotated[str, AfterValidator(validate_ffmpeg_loglevel)]
PythonLogLevel = Annotated[str, AfterValidator(validate_python_log_level)]
