"""HTTP server for automated speech recognition (ASR)."""
import argparse
import io
import wave
from pathlib import Path

from flask import Flask, Response, jsonify, redirect, request
from swagger_ui import flask_api_doc  # pylint: disable=no-name-in-module

from wyoming.asr import Transcribe, Transcript
from wyoming.audio import wav_to_chunks
from wyoming.client import AsyncClient
from wyoming.info import Describe, Info

_DIR = Path(__file__).parent
CONF_PATH = _DIR / "conf" / "asr.yaml"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--uri", help="URI of Wyoming ASR service")
    parser.add_argument("--model", help="Default model name for transcription")
    parser.add_argument("--language", help="Default language for transcription")
    parser.add_argument("--samples-per-chunk", type=int, default=1024)
    args = parser.parse_args()

    app = Flask("asr")

    @app.route("/")
    def redirect_to_api():
        return redirect("/api")

    @app.route("/api/speech-to-text", methods=["POST"])
    async def api_stt() -> Response:
        uri = request.args.get("uri", args.uri)
        if not uri:
            raise ValueError("URI is required")

        model_name = request.args.get("model", args.model)
        language = request.args.get("language", args.model)

        async with AsyncClient.from_uri(uri) as client:
            await client.write_event(
                Transcribe(name=model_name, language=language).event()
            )

            with io.BytesIO(request.data) as wav_io:
                with wave.open(wav_io, "rb") as wav_file:
                    chunks = wav_to_chunks(
                        wav_file,
                        samples_per_chunk=1024,
                        start_event=True,
                        stop_event=True,
                    )
                    for chunk in chunks:
                        await client.write_event(chunk.event())

            while True:
                event = await client.read_event()
                if event is None:
                    raise RuntimeError("Client disconnected")

                if Transcript.is_type(event.type):
                    transcript = Transcript.from_event(event)
                    return jsonify(transcript.to_dict())

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
