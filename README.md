# Wyoming Protocol

A peer-to-peer protocol for voice assistants (basically [JSONL](https://jsonlines.org/) + PCM audio)

``` text
{ "type": "...", "data": { ... }, "data_length": ..., "payload_length": ... }\n
<data_length bytes (optional)>
<payload_length bytes (optional)>
```

Used in [Rhasspy](https://github.com/rhasspy/rhasspy3/) and the [Home Assistant](https://www.home-assistant.io/integrations/wyoming) for communication with voice services.

## Wyoming Projects

* Voice satellites
    * [Satellite](https://github.com/rhasspy/wyoming-satellite) for Home Assistant 
* Audio input/output
    * [mic-external](https://github.com/rhasspy/wyoming-mic-external)
    * [snd-external](https://github.com/rhasspy/wyoming-snd-external)
    * [SDL2](https://github.com/rhasspy/wyoming-sdl2)
* Wake word detection
    * [openWakeWord](https://github.com/rhasspy/wyoming-openwakeword)
    * [porcupine1](https://github.com/rhasspy/wyoming-porcupine1)
    * [snowboy](https://github.com/rhasspy/wyoming-snowboy)
* Speech-to-text
    * [Faster Whisper](https://github.com/rhasspy/wyoming-faster-whisper)
    * [Vosk](https://github.com/rhasspy/wyoming-vosk)
* Text-to-speech
    * [Piper](https://github.com/rhasspy/wyoming-piper)
* Intent handling
    * [handle-external](https://github.com/rhasspy/wyoming-handle-external)

## Format

1. A JSON object header as a single line with `\n` (UTF-8, required)
    * `type` - event type (string, required)
    * `data` - event data (object, optional)
    * `data_length` - bytes of additional data (int, optional)
    * `payload_length` - bytes of binary payload (int, optional)
2. Additional data (UTF-8, optional)
    * JSON object with additional event-specific data
    * Merged on top of header `data`
    * Exactly `data_length` bytes long
    * Immediately follows header `\n`
3. Payload
    * Typically PCM audio but can be any binary data
    * Exactly `payload_length` bytes long
    * Immediately follows additional data or header `\n` if no additional data


## Events Types

Available events with `type` and fields.

### Audio

Send raw audio and indicate begin/end of audio streams.

* `audio-chunk` - chunk of raw PCM audio
    * `rate` - sample rate in hertz (int, required)
    * `width` - sample width in bytes (int, required)
    * `channels` - number of channels (int, required)
    * `timestamp` - timestamp of audio chunk in milliseconds (int, optional)
    * Payload is raw PCM audio samples
* `audio-start` - start of an audio stream
    * `rate` - sample rate in hertz (int, required)
    * `width` - sample width in bytes (int, required)
    * `channels` - number of channels (int, required)
    * `timestamp` - timestamp in milliseconds (int, optional)
* `audio-stop` - end of an audio stream
    * `timestamp` - timestamp in milliseconds (int, optional)
    
    
### Info

Describe available services.

* `describe` - request for available voice services
* `info` - response describing available voice services
    * `asr` - list speech recognition services (optional)
        * `models` - list of available models (required)
            * `name` - unique name (required)
            * `languages` - supported languages by model (list of string, required)
            * `attribution` (required)
                * `name` - name of creator (required)
                * `url` - URL of creator (required)
            * `installed` - true if currently installed (bool, required)
            * `description` - human-readable description (string, optional)
            * `version` - version of the model (string, optional)
    * `tts` - list text to speech services (optional)
        * `models` - list of available models
            * `name` - unique name (required)
            * `languages` - supported languages by model (list of string, required)
            * `speakers` - list of speakers (optional)
                * `name` - unique name of speaker (required)
            * `attribution` (required)
                * `name` - name of creator (required)
                * `url` - URL of creator (required)
            * `installed` - true if currently installed (bool, required)
            * `description` - human-readable description (string, optional)
            * `version` - version of the model (string, optional)
    * `wake` - list wake word detection services( optional )
        * `models` - list of available models (required)
            * `name` - unique name (required)
            * `languages` - supported languages by model (list of string, required)
            * `attribution` (required)
                * `name` - name of creator (required)
                * `url` - URL of creator (required)
            * `installed` - true if currently installed (bool, required)
            * `description` - human-readable description (string, optional)
            * `version` - version of the model (string, optional)
    * `handle` - list intent handling services (optional)
        * `models` - list of available models (required)
            * `name` - unique name (required)
            * `languages` - supported languages by model (list of string, required)
            * `attribution` (required)
                * `name` - name of creator (required)
                * `url` - URL of creator (required)
            * `installed` - true if currently installed (bool, required)
            * `description` - human-readable description (string, optional)
            * `version` - version of the model (string, optional)
    * `intent` - list intent recognition services (optional)
        * `models` - list of available models (required)
            * `name` - unique name (required)
            * `languages` - supported languages by model (list of string, required)
            * `attribution` (required)
                * `name` - name of creator (required)
                * `url` - URL of creator (required)
            * `installed` - true if currently installed (bool, required)
            * `description` - human-readable description (string, optional)
            * `version` - version of the model (string, optional)
    * `satellite` - information about voice satellite (optional)
        * `area` - name of area where satellite is located (string, optional)
        * `snd_format` - optimal audio output format of satellite (optional)
            * `rate` - sample rate in hertz (int, required)
            * `width` - sample width in bytes (int, required)
            * `channels` - number of channels (int, required)
    
### Speech Recognition

Transcribe audio into text.

* `transcribe` - request to transcribe an audio stream
    * `name` - name of model to use (string, optional)
    * `language` - language of spoken audio (string, optional)
    * `context` - context from previous interactions (object, optional)
* `transcript` - response with transcription
    * `text` - text transcription of spoken audio (string, required)
    * `context` - context for next interaction (object, optional)

### Text to Speech

Synthesize audio from text.

* `synthesize` - request to generate audio from text
    * `text` - text to speak (string, required)
    * `voice` - use a specific voice (optional)
        * `name` - name of voice (string, optional)
        * `language` - language of voice (string, optional)
        * `speaker` - speaker of voice (string, optional)
    
### Wake Word

Detect wake words in an audio stream.

* `detect` - request detection of specific wake word(s)
    * `names` - wake word names to detect (list of string, optional)
* `detection` - response when detection occurs
    * `name` - name of wake word that was detected (int, optional)
    * `timestamp` - timestamp of audio chunk in milliseconds when detection occurred (int optional)
* `not-detected` - response when audio stream ends without a detection

### Voice Activity Detection

Detects speech and silence in an audio stream.

* `voice-started` - user has started speaking
    * `timestamp` - timestamp of audio chunk when speaking started in milliseconds (int, optional)
* `voice-stopped` - user has stopped speaking
    * `timestamp` - timestamp of audio chunk when speaking stopped in milliseconds (int, optional)
    
### Intent Recognition

Recognizes intents from text.

* `recognize` - request to recognize an intent from text
    * `text` - text to recognize (string, required)
    * `context` - context from previous interactions (object, optional)
* `intent` - response with recognized intent
    * `name` - name of intent (string, required)
    * `entities` - list of entities (optional)
        * `name` - name of entity (string, required)
        * `value` - value of entity (any, optional)
    * `text` - response for user (string, optional)
    * `context` - context for next interactions (object, optional)
* `not-recognized` - response indicating no intent was recognized
    * `text` - response for user (string, optional)
    * `context` - context for next interactions (object, optional)

### Intent Handling

Handle structured intents or text directly.

* `handled` - response when intent was successfully handled
    * `text` - response for user (string, optional)
    * `context` - context for next interactions (object, optional)
* `not-handled` - response when intent was not handled
    * `text` - response for user (string, optional)
    * `context` - context for next interactions (object, optional)

### Audio Output

Play audio stream.

* `played` - response when audio finishes playing

### Voice Satellite

Control of one or more remote voice satellites connected to a central server.

* `run-satellite` - informs satellite that server is ready to run pipelines
* `pause-satellite` - informs satellite that server is not ready anymore to run pipelines
* `satellite-connected` - satellite has connected to the server
* `satellite-disconnected` - satellite has been disconnected from the server
* `streaming-started` - satellite has started streaming audio to the server
* `streaming-stopped` - satellite has stopped streaming audio to the server


## Event Flow

* &rarr; is an event from client to server
* &larr; is an event from server to client


### Service Description

1. &rarr; `describe` (required) 
2. &larr; `info` (required)


### Speech to Text

1. &rarr; `transcribe` event with `name` of model to use or `language` (optional)
2. &rarr; `audio-start` (required)
3. &rarr; `audio-chunk` (required)
    * Send audio chunks until silence is detected
4. &rarr; `audio-stop` (required)
5. &larr; `transcript`
    * Contains text transcription of spoken audio

### Text to Speech

1. &rarr; `synthesize` event with `text` (required)
2. &larr; `audio-start`
3. &larr; `audio-chunk`
    * One or more audio chunks
4. &larr; `audio-stop`

### Wake Word Detection

1. &rarr; `detect` event with `names` of wake words to detect (optional)
2. &rarr; `audio-start` (required)
3. &rarr; `audio-chunk` (required)
    * Keep sending audio chunks until a `detection` is received
4. &larr; `detection`
    * Sent for each wake word detection 
5. &rarr; `audio-stop` (optional)
    * Manually end audio stream
6. &larr; `not-detected`
    * Sent after `audio-stop` if no detections occurred
    
### Voice Activity Detection

1. &rarr; `audio-chunk` (required)
    * Send audio chunks until silence is detected
2. &larr; `voice-started`
    * When speech starts
3. &larr; `voice-stopped`
    * When speech stops
    
### Intent Recognition

1. &rarr; `recognize` (required)
2. &larr; `intent` if successful
3. &larr; `not-recognized` if not successful

### Intent Handling

For structured intents:

1. &rarr; `intent` (required)
2. &larr; `handled` if successful
3. &larr; `not-handled` if not successful

For text only:

1. &rarr; `transcript` with `text` to handle (required)
2. &larr; `handled` if successful
3. &larr; `not-handled` if not successful
    
### Audio Output

1. &rarr; `audio-start` (required)
2. &rarr; `audio-chunk` (required)
    * One or more audio chunks
3. &rarr; `audio-stop` (required)
4. &larr; `played`
