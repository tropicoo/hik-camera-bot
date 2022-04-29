# Hikvision Telegram Camera Bot
Telegram Bot which sends snapshots from your Hikvision cameras.

Version: 1.4. [Release details](releases/release_1.4.md).

## Features
1. Send full/resized snapshots on request
2. Auto-send snapshots on **Motion**, **Line Crossing** and **Intrusion (Field) Detection**
3. Send so-called Telegram video-gifs on request and alert events from paragraph #2
4. YouTube, Telegram and Icecast direct or re-encoded livestreams
5. DVR to local storage with upload to Telegram group
6. SRS re-stream server


![frames](img/screenshot-1.png)

# Installation
To install Hikvision Telegram Camera Bot, simply `clone` the repo.

```shell script
git clone https://github.com/tropicoo/hikvision-camera-bot.git
cd hikvision-camera-bot
```

# Configuration
Configuration files are stored in JSON format and can be found in `configs` directory.

## Quick Setup
1. [Create and start Telegram Bot](https://core.telegram.org/bots#6-botfather)
 and get its API token
2. [Get your own Telegram API key](https://my.telegram.org/apps) (`api_id` and `api_hash`)
3. Copy 3 default configuration files with predefined templates in `configs` directory:
    
    ```bash
    cd configs
    cp config-template.json config.json
    cp encoding_templates-template.json encoding_templates.json
    cp livestream_templates-template.json livestream_templates.json
    ```
4. Edit **config.json**:
    1. Put the obtained `api_id` and `api_hash` strings to same keys
    2. Put the obtained bot API token string to `token` key
    3. [Find](https://stackoverflow.com/a/32777943) your Telegram user id
    and put it to `chat_users`, `alert_users` and `startup_message_users` lists as 
    integer value. Multiple ids can be used, just separate them with a comma.
    4. Hikvision camera settings are placed inside the `camera_list` section. Template
    comes with two cameras

        **Camera names should start with `cam_` prefix and end with 
        digit suffix**: `cam_1`, `cam_2`, `cam_<digit>` with any description.

    5. Write authentication credentials in `user` and `password` keys for every camera
    6. Same for `host`, which should include protocol, e.g. `http://192.168.1.1`
    7. In `alert` section you can enable sending picture on alert (Motion, 
    Line Crossing and Intrusion (Field) Detection). Configure `delay` setting 
    in seconds between pushing alert pictures. To send resized picture change 
    `fullpic` to `false`

### Example `config.json` with dummy values
```json
{
  "telegram": {
    "api_id": 11111111,
    "api_hash": "1a1a1a1a1a1a1a1a",
    "lang_code": "en",
    "token": "1b1b1b1b1b1b1b1b",
    "chat_users": [
      1010101010,
      2020202020
    ],
    "alert_users": [
      1010101010,
      2020202020
    ],
    "startup_message_users": [
      1010101010,
      2020202020
    ]
  },
  "log_level": "DEBUG",
  "camera_list": {
    "cam_1": {
      "hidden": false,
      "description": "Kitchen",
      "hashtag": "kitchen",
      "group": "Test group",
      "api": {
        "host": "http://192.168.1.1",
        "auth": {
          "user": "dummy-user",
          "password": "dummy-password"
        },
        "stream_timeout": 10
      },
      "rtsp_port": 554,
      "video_gif": {
        "on_demand": {
          "channel": 101,
          "record_time": 10,
          "rewind_time": 10,
          "tmp_storage": "/tmp",
          "loglevel": "error",
          "rtsp_transport_type": "tcp"
        },
        "on_alert": {
          "channel": 101,
          "record_time": 10,
          "rewind_time": 10,
          "rewind": true,
          "tmp_storage": "/tmp",
          "loglevel": "error",
          "rtsp_transport_type": "tcp"
        }
      },
      "alert": {
        "delay": 15,
        "motion_detection": {
          "enabled": false,
          "sendpic": true,
          "fullpic": false,
          "send_videogif": true
        },
        "line_crossing_detection": {
          "enabled": false,
          "sendpic": true,
          "fullpic": false,
          "send_videogif": true
        },
        "intrusion_detection": {
          "enabled": false,
          "sendpic": true,
          "fullpic": false,
          "send_videogif": true
        }
      },
      "livestream": {
        "youtube": {
          "enabled": false,
          "livestream_template": "tpl_kitchen",
          "encoding_template": "direct.kitchen_youtube"
        },
        "telegram": {
          "enabled": false,
          "livestream_template": "tpl_kitchen",
          "encoding_template": "direct.kitchen_telegram"
        },
        "srs": {
          "enabled": true,
          "livestream_template": "tpl_kitchen",
          "encoding_template": "direct.kitchen_srs"
        },
        "dvr": {
          "enabled": false,
          "local_storage_path": "/data/dvr",
          "livestream_template": "tpl_kitchen",
          "encoding_template": "direct.kitchen_dvr",
          "upload": {
            "delete_after_upload": true,
            "storage": {
              "telegram": {
                "enabled": false,
                "group_id": -10000000
              }
            }
          }
        },
        "icecast": {
          "enabled": false,
          "livestream_template": "tpl_kitchen",
          "encoding_template": "vp9.kitchen"
        }
      },
      "command_sections_visibility": {
        "general": true,
        "infrared": true,
        "motion_detection": true,
        "line_detection": true,
        "intrusion_detection": true,
        "alert_service": true,
        "stream_youtube": true,
        "stream_telegram": true,
        "stream_icecast": true
      }
    }
  }
}
```

# Usage
## Launch by using Docker and Docker Compose
1. Set your timezone by editing `.env` file (`TZ=Europe/Kiev`).
Currently, there is Ukrainian timezone because I live there.
Look for your timezone here [http://www.timezoneconverter.com/cgi-bin/zoneinfo](http://www.timezoneconverter.com/cgi-bin/zoneinfo).
If you want to use default UTC time format, set Greenwich Mean Time timezone `TZ=GMT`

2. Build an image and run a container in a detached mode
    ```bash
    sudo docker-compose build && sudo docker-compose up -d && sudo docker-compose logs -f --tail=1000
    ```

# Commands
| Command | Description |
|---|---|
| `/start` | Start the bot (one-time action during first start) and show help |
| `/help` | Show help message |
| `/list_cams` | List all your cameras |
| `/cmds_cam_*` | List commands for particular camera |
| `/getpic_cam_*` | Get resized picture from your Hikvision camera  |
| `/getfullpic_cam_*` | Get full-sized picture from your Hikvision camera |
| `/ir_on_cam_*` | Turn on Infrared mode |
| `/ir_off_cam_*` | Turn off Infrared mode |
| `/ir_auto_cam_*` | Turn on Infrared auto mode |
| `/md_on_cam_*` | Enable Motion Detection |
| `/md_off_cam_*` | Disable Motion Detection |
| `/ld_on_cam_*` | Enable Line Crossing Detection |
| `/ld_off_cam_*` | Disable Line Crossing Detection |
| `/intr_on_cam_*` | Enable Intrusion (Field) Detection |
| `/intr_off_cam_*` | Disable Intrusion (Field) Detection |
| `/alert_on_cam_*` | Enable Alert (Alarm) mode. It means it will send respective alert to your account in Telegram |
| `/alert_off_cam_*` | Disable Alert (Alarm) mode, no alerts will be sent when something detected |
| `/yt_on_cam_*` | Enable YouTube stream |
| `/yt_off_cam_*` | Disable YouTube stream |
| `/icecast_on_cam_*` | Enable Icecast stream |
| `/icecast_off_cam_*` | Disable Icecast stream |

`*` - camera digit id, e.g. `cam_1`.

#  Advanced Configuration
## SRS
[SRS](https://github.com/ossrs/srs/tree/4.0release) (Simple Realtime Server) is a re-stream server which takes a stream from your camera and re-streams it
to any destination without touching native camera stream multiple times.
SRS release version used in the bot is `4.0`.

SRS decreases CPU time and network load on the camera when you enable something like DVR,
 YouTube Livestream or try to get Video GIF at the same time. Pictures are taken
directly from the camera stream, not from the SRS.

How it works - if you have two cameras with enabled SRS for both, there will be two
running 24/7 bot tasks taking streams from the cameras to the SRS server. Eventually, when you
request Video Gif, or it's triggered by some alert, video will be taken from SRS server.

You can also connect to SRS server with any video player like VLC and watch the stream
without any interruptions. URL looks like this: `rtmp://192.168.1.100/live/livestream_101_cam_2`,
where:
1. `192.168.1.100` is an IP address or a host of your server.
2. `101` is camera's configured stream channel.
3. `cam_2` is ID of your second configured camera.

SRS runs in a separate docker container. SRS config and `Dockerfile` placed
in `srs_prod` directory. Service name is `hikvision-srs-server` in `docker-compose.yml`.



If `docker-compose.yml` is a list of forwarded and open SRS ports to the world:
```yaml
# If you don't plan to use anything from this, just comment out the whole section.
ports:
  - "1935:1935"   # SRS RTMP port, if you comment this out, you won't be able to connect with video player
  - "1985:1985"   # SRS API port, can be commented out since not used
  - "8080:8080"   # SRS WebUI port
```

## DVR
You can record your videos from the camera to a local storage mounted as volume in
volumes section of `hikvision-camera-bot` service in `docker-compose.yml`.

DVR configuration is per camera in `config.json` with livestream template name from `livestream_templates.json`.

It's very simple:
1. Use `enabled` key to turn on/off this feature.
2. `local_storage_path` is a path inside the container to which videos will be recorded. 
Don't change this default value (`/data/dvr`) since it's written in the volumes mapping section.
If you need to change it for some reason - you need to change both here and in the volumes mapping.
3. `livestream_template` has a template name located inside the `livestream_templates.json` 
file with DVR stream settings:
    ```json
    "dvr": {
      "tpl_kitchen": {
        "channel": 101,
        "sub_channel": 102,
        "restart_period": -1,
        "restart_pause": 0,
        "segment_time": 1800,
      }
    }
    ```
    a) `segment_time` is time in seconds when DVR record file will be split to a new one. 

    b) `1800` seconds mean every file will have 30 minutes of video recording.

    c) File is named as `cam_1_101_1800_2022-04-15_21-19-32.mp4` with cam ID, channel name, segment time, and record start datetime.

4. Configuration part from the `config.json`:
    ```json
    "dvr": {
      "enabled": true,
      "local_storage_path": "/data/dvr",
      "livestream_template": "tpl_kitchen",
      "encoding_template": "direct.kitchen_dvr",
      "upload": {
        "delete_after_upload": true,
        "storage": {
          "telegram": {
            "enabled": true,
            "group_id": -1001631507769
          }
        }
      }
    }
    ```
    Recorded files can be uploaded to Telegram group. Right now upload will work only
    if `delete_after_upload` is set to `true` meaning uploaded file will be deleted 
    from the local storage. You need to make sure your file size will be up to 2GB since
    Telegram rejects larger ones. Just experiment with segment time.
5. Local storage (the real one, not in the container) by default is `/data/dvr` in volumes mapping (the first path string, not the last).
   Change it to any location you need, e.g. to `- D:\Videos:/data/dvr` if you're on Windows.
    ```yaml
    volumes:
      - "/data/dvr:/data/dvr"
    ```
6. Watch logs for any errors.


## YouTube Livestream
To enable YouTube Live Stream enable it in the `youtube` key.

| Parameter | Value | Description |
|---|---|---|
| `"enabled"` | `false` | set `true` to start stream during bot start |
| `"livestream_template"` | `"tpl_kitchen"` | stream template, read below |
| `"encoding_template"` | `"x264.kitchen"` | stream template, read below |

**Livestream templates**

To start particular livestream, user needs to set both *livestream* and
*encoding* templates with stream settings and encoding type/arguments.

Encoding templates

`direct` means that video stream will not be re-encoded (transcoded) and will
be sent to YouTube/Icecast servers "as is", only audio can be disabled.

`x264` or `vp9` means that video stream will be re-encoded on your machine/server
where bot is running using respective encoding codecs.

User can create its own templates in file named `livestream_templates.json` 
and `encoding_templates.json`.

Default dummy template file is named `livestream_templates_template.json` 
(not very funny name but anyway) which should be copied or renamed to 
`livestream_templates.json`.

Same for `encoding_templates-template.json` -> `encoding_templates.json`

<details>
  <summary>livestream_templates-template.json</summary>

  ```json
  {
    "youtube": {
      "tpl_kitchen": {
        "channel": 101,
        "restart_period": 39600,
        "restart_pause": 10,
        "url": "rtmp://a.rtmp.youtube.com/live2",
        "key": "xxxx-xxxx-xxxx-xxxx"
      },
      "tpl_basement": {
        "channel": 101,
        "restart_period": 39600,
        "restart_pause": 10,
        "url": "rtmp://a.rtmp.youtube.com/live2",
        "key": "xxxx-xxxx-xxxx-xxxx"
      }
    },
    "icecast": {
      "tpl_kitchen": {
        "channel": 101,
        "restart_period": 39600,
        "restart_pause": 10,
        "ice_stream": {
          "ice_genre": "333Default",
          "ice_name": "222Default",
          "ice_description": "111Default",
          "ice_public": 0,
          "url": "icecast://source@192.168.10.1:8000/video.webm",
          "password": "hackme",
          "content_type": "video/webm"
        }
      },
      "tpl_basement": {
        "channel": 101,
        "restart_period": 39600,
        "restart_pause": 10,
        "ice_stream": {
          "ice_genre": "333Default",
          "ice_name": "222Default",
          "ice_description": "111Default",
          "ice_public": 0,
          "url": "icecast://source@192.168.10.2:8000/video.webm",
          "password": "hackme",
          "content_type": "video/webm"
        }
      }
    }
  }
  ```
</details>

Where:

| Parameter | Value | Description |
|---|---|---|
| `channel` | `101` | camera channel. 101 is main stream, 102 is substream. |
| `restart_period` | `39600` | stream restart period in seconds |
| `restart_pause` | `10` | stream pause before starting on restart |
| `url` | `"rtmp://a.rtmp.youtube.com/live2"` | YouTube rtmp server |
| `key` | `"aaaa-bbbb-cccc-dddd"` | YouTube Live Streams key. |
| `ice_genre` | `"Default"` | Icecast stream genre |
| `ice_name` | `"Default"` | Icecast stream name |
| `ice_description` | `"Default"` | Icecast stream description |
| `ice_public` | `0` | Icecast public switch, default 0 |
| `url` | `"icecast://source@x.x.x.x:8000/video.webm"` | Icecast server URL, Port and media mount point |
| `password` | `"xxxx"` | Icecast authentication password |
| `content_type` | `"video/webm"` | FFMPEG content-type for Icecast stream |

<details>
  <summary>encoding_templates-template.json</summary>

  ```json
  {
    "x264": {
      "kitchen": {
        "null_audio": false,
        "loglevel": "error",
        "vcodec": "libx264",
        "acodec": "aac",
        "format": "flv",
        "rtsp_transport_type": "tcp",
        "pix_fmt": "yuv420p",
        "pass_mode": 1,
        "framerate": 25,
        "preset": "superfast",
        "average_bitrate": "1000K",
        "maxrate": "3000k",
        "bufsize": "6000k",
        "tune": "zerolatency",
        "scale": {
          "enabled": true,
          "width": 640,
          "height": -1,
          "format": "yuv420p"
        }
      },
      "basement": {
        "null_audio": false,
        "loglevel": "error",
        "vcodec": "libx264",
        "acodec": "aac",
        "format": "flv",
        "rtsp_transport_type": "tcp",
        "pix_fmt": "yuv420p",
        "pass_mode": 1,
        "framerate": 25,
        "preset": "superfast",
        "average_bitrate": "1000K",
        "maxrate": "3000k",
        "bufsize": "6000k",
        "tune": "zerolatency",
        "scale": {
          "enabled": true,
          "width": 640,
          "height": -1,
          "format": "yuv420p"
        }
      }
    },
    "vp9": {
      "kitchen": {
        "null_audio": false,
        "loglevel": "info",
        "vcodec": "libvpx-vp9",
        "acodec": "libopus",
        "format": "webm",
        "rtsp_transport_type": "tcp",
        "pix_fmt": "yuv420p",
        "pass_mode": 1,
        "framerate": 10,
        "average_bitrate": "1000K",
        "maxrate": "2000k",
        "bufsize": "4000k",
        "deadline": "realtime",
        "speed": 5,
        "scale": {
          "enabled": true,
          "width": 640,
          "height": -1,
          "format": "yuv420p"
        }
      },
      "basement": {
        "null_audio": false,
        "loglevel": "info",
        "vcodec": "libvpx-vp9",
        "acodec": "libopus",
        "format": "webm",
        "rtsp_transport_type": "tcp",
        "pix_fmt": "yuv420p",
        "pass_mode": 1,
        "framerate": 10,
        "average_bitrate": "1000K",
        "maxrate": "2000k",
        "bufsize": "4000k",
        "deadline": "realtime",
        "speed": 5,
        "scale": {
          "enabled": true,
          "width": 640,
          "height": -1,
          "format": "yuv420p"
        }
      }
    },
    "direct": {
      "kitchen": {
        "null_audio": false,
        "loglevel": "error",
        "vcodec": "copy",
        "acodec": "aac",
        "format": "flv",
        "rtsp_transport_type": "tcp"
      },
      "basement": {
        "null_audio": false,
        "loglevel": "error",
        "vcodec": "copy",
        "acodec": "aac",
        "format": "flv",
        "rtsp_transport_type": "tcp"
      }
    }
  }
  ```
</details>

Where:

| Parameter | Value | Description |
|---|---|---|
| `null_audio` | `false` | enable fake silent audio (for cameras without mics) |
| `url` | `"rtmp://a.rtmp.youtube.com/live2"` | YouTube rtmp server |
| `key` | `"aaaa-bbbb-cccc-dddd"` | YouTube Live Streams key |
| `loglevel` | `"quiet"` | ffmpeg log levels, default "quiet" |
| `pix_fmt` | `"yuv420p"` | pixel format, Hikvision streams in yuvj420p |
| `framerate` | `25` | encode framerate, YouTube will re-encode any to 30 anyway |
| `preset` | `"superfast"` | libx264 predefined presets, more here https://trac.ffmpeg.org/wiki/Encode/H.264 |
| `maxrate` | `"3000k"` | max variable bitrate |
| `bufsize` | `"2000k"` | rate control buffer |
| `tune` | `"zerolatency"` | tune for zero latency |
| `scale` | \<key\> | re-scale video size |
| `enabled` | `true` | false to disable and re-encode with source width and height |
| `width` | `640` | width |
| `height` | `-1` | height, -1 means will be automatically determined |
| `format` | `"yuv420p"` | pixel format |

> YouTube Live Streams server/key is available at https://www.youtube.com/live_dashboard.
