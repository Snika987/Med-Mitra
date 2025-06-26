import os
from dotenv import load_dotenv
from deepgram import DeepgramClient, PrerecordedOptions

load_dotenv()
DG_API_KEY = os.getenv("DEEPGRAM_API_KEY")

def transcribe_with_deepgram(audio_path: str) -> str:
    try:
        dg_client = DeepgramClient(DG_API_KEY)

        # Options for transcription
        options = PrerecordedOptions(
            model="general",
            smart_format=True,
            language="en"
        )

        # ✅ Open file and pass as source
        with open(audio_path, "rb") as audio:
            source = {
                "buffer": audio,
                "mimetype": "audio/wav"
            }

            # ✅ CORRECT: pass source explicitly
            response = dg_client.listen.prerecorded.v("1").transcribe_file(
                source=source,
                options=options
            )

        return response["results"]["channels"][0]["alternatives"][0]["transcript"]

    except Exception as e:
        return f"Transcription failed: {str(e)}"
