"""HTTP server for text to speech (TTS)."""
import argparse
import io
import wave
from pathlib import Path
from typing import Optional

from flask import Flask, Response, jsonify, redirect, request
from swagger_ui import flask_api_doc  # pylint: disable=no-name-in-module

from wyoming.audio import AudioChunk, AudioStart, AudioStop
from wyoming.client import AsyncClient
from wyoming.info import Describe, Info
from wyoming.tts import Synthesize, SynthesizeVoice

_DIR = Path(__file__).parent
CONF_PATH = _DIR / "conf" / "tts.yaml"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--uri", help="URI of Wyoming ASR service")
    parser.add_argument("--voice", help="Default voice for synthesis")
    parser.add_argument("--speaker", help="Default voice speaker for synthesis")
    args = parser.parse_args()

    app = Flask("tts")

    @app.route("/")
    def redirect_to_api():
        return redirect("/api")

    @app.route("/api/text-to-speech", methods=["POST", "GET"])
    async def api_stt() -> Response:
        uri = request.args.get("uri", args.uri)
        if not uri:
            raise ValueError("URI is required")

        if request.method == "POST":
            text = request.data.decode()
        else:
            text = request.args.get("text", "")

        if not text:
            raise ValueError("Text is required")

        voice: Optional[SynthesizeVoice] = None
        voice_name = request.args.get("voice", args.voice)
        if voice_name:
            voice = SynthesizeVoice(
                name=voice_name, speaker=request.args.get("speaker", args.speaker)
            )

        async with AsyncClient.from_uri(uri) as client:
            wav_io = io.BytesIO()
            wav_file = wave.open(wav_io, "wb")
            await client.write_event(Synthesize(text=text, voice=voice).event())

            while True:
                event = await client.read_event()
                if event is None:
                    raise RuntimeError("Client disconnected")

                if AudioStart.is_type(event.type):
                    audio_start = AudioStart.from_event(event)
                    wav_file.setframerate(audio_start.rate)
                    wav_file.setsampwidth(audio_start.width)
                    wav_file.setnchannels(audio_start.channels)
                elif AudioChunk.is_type(event.type):
                    audio_chunk = AudioChunk.from_event(event)
                    wav_file.writeframes(audio_chunk.audio)
                elif AudioStop.is_type(event.type):
                    wav_file.close()
                    wav_io.seek(0)
                    return Response(
                        wav_io.getvalue(), headers={"Content-Type": "audio/wav"}
                    )

    @app.route("/api/info", methods=["GET"])
    async def api_info():
        uri = request.args.get("uri", args.uri)
        if not uri:
            raise ValueError("URI is required")

        async with AsyncClient.from_uri(uri) as client:
            await client.write_event(Describe().event())

            while True:
                event = await client.read_event()
                if event is None:
                    raise RuntimeError("Client disconnected")

                if Info.is_type(event.type):
                    info = Info.from_event(event)
                    return jsonify(info.to_dict())

    flask_api_doc(app, config_path=str(CONF_PATH), url_prefix="/api", title="API doc")
    app.run(args.host, args.port)


if __name__ == "__main__":
    main()
