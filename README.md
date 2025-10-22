# Emmet

> "Wait a minute, Doc. Are you telling me you built a voice assistant... for Home Assistant?"

**Emmett** is a self-hosted voice assistant, written in Python, designed to integrate directly with [Home Assistant](https://www.home-assistant.io/).

It uses the custom wake-word **"Hey Doc!"** to activate and then listens for your commands. It's built to be lightweight, privacy-focused, and thematic.

The goal of this project is to provide a flexible alternative to cloud services (like Alexa or Google) by using an offline wake-word engine and processing commands locally or via APIs...

## Main Features

* **Offline Wake-Word:** Uses [Picovoice Porcupine](https://picovoice.ai/platform/porcupine/) to detect the wake-word "Hey Doc!" efficiently and entirely offline.
* **HA Integration:** Designed to send commands, trigger scripts, or start automations on your Home Assistant instance.
* **Flexible:** Written in Python, easy to modify and extend.
* **Private:** Your voice does not leave your local network (except for command transcription if you choose to use a cloud API such as Google Speech-to-Text).

## Requirements

* Python 3
* A Home Assistant instance
* A microphone
* A Picovoice AccessKey (free for personal use)

## Installation


## License

The source code of **Emmett** is released under the [MIT License](LICENSE).

Please note that this project depends on Picovoice Porcupine, which is governed by the [Apache 2.0 License](https://github.com/Picovoice/porcupine/blob/master/LICENSE). Wake-word models ...
