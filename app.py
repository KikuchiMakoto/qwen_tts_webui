"""Qwen3-TTS WebUI - Streamlit アプリケーション."""

import io
import tempfile
import uuid
from pathlib import Path

import numpy as np
import soundfile as sf
import streamlit as st
import streamlit.components.v1 as components
import torch

from engine import GREETINGS, SUPPORTED_LANGUAGES, TTSEngine
from i18n import (
    UI_LANGUAGE_NAMES,
    UI_LANGUAGES,
    detect_ui_language,
    get_tts_default_language,
    get_translations,
)
from voice_store import (
    export_voice,
    import_voice,
    list_voices_by_size,
    load_voice,
    remove_voice,
    save_voice,
)

st.set_page_config(
    page_title="Qwen3-TTS WebUI",
    layout="wide",
)

# --- セッション状態の初期化 ---

if "ui_lang" not in st.session_state:
    st.session_state.ui_lang = detect_ui_language()
if "engine" not in st.session_state:
    st.session_state.engine = TTSEngine()
if "tts_history" not in st.session_state:
    st.session_state.tts_history = []
if "instant_history" not in st.session_state:
    st.session_state.instant_history = []
if "is_generating" not in st.session_state:
    st.session_state.is_generating = False

# --- 言語設定と翻訳辞書（セッション状態から取得）---
T = get_translations(st.session_state.ui_lang)

# デフォルト TTS 言語 (SUPPORTED_LANGUAGES のインデックス)
_DEFAULT_TTS_LANG = get_tts_default_language(st.session_state.ui_lang)
_DEFAULT_TTS_INDEX = (
    SUPPORTED_LANGUAGES.index(_DEFAULT_TTS_LANG)
    if _DEFAULT_TTS_LANG in SUPPORTED_LANGUAGES
    else 0
)

# --- 内部モードキー ---
MODE_TRAIN = "train"
MODE_TTS = "tts"
MODE_INSTANT = "instant"
MODE_WEBAPI = "webapi"

# --- 内部ボイスソースキー ---
VOICE_SOURCE_SAVED = "saved"
VOICE_SOURCE_UPLOAD = "upload"


# --- UI 言語変更コールバック ---

# TTS 言語セレクトボックスのセッション状態キー一覧
_TTS_LANG_KEYS = ("train_lang", "import_lang", "tts_lang", "instant_ref_lang", "instant_out_lang")


def on_ui_lang_change() -> None:
    """UI 言語が変更されたとき、TTS 言語の各セレクトボックスをデフォルト値にリセットする。"""
    new_tts_default = get_tts_default_language(st.session_state.ui_lang)
    for key in _TTS_LANG_KEYS:
        if key in st.session_state:
            st.session_state[key] = new_tts_default


# --- ユーティリティ ---


def audio_to_bytes(wav: np.ndarray, sr: int) -> bytes:
    """numpy音声をWAVバイト列に変換する。"""
    buf = io.BytesIO()
    sf.write(buf, wav, sr, format="WAV")
    buf.seek(0)
    return buf.read()


def save_uploaded_audio(uploaded_file) -> str:
    """アップロードされた音声をテンポラリファイルに保存しパスを返す。"""
    suffix = Path(uploaded_file.name).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
        f.write(uploaded_file.getvalue())
        return f.name


# 音声学習に使用するリファレンス音声の長さ制約（秒）
VOICE_LEARNING_MIN_DURATION: float = 3.0
VOICE_LEARNING_MAX_DURATION: float = 15.0


def get_audio_duration(uploaded_file) -> float:
    """アップロードされた音声ファイルの長さ（秒）を返す。

    Raises:
        ValueError: 音声ファイルの読み込みに失敗した場合
    """
    data = uploaded_file.getvalue()
    try:
        with sf.SoundFile(io.BytesIO(data)) as f:
            return len(f) / f.samplerate
    except Exception as e:
        raise ValueError(str(e)) from e


def validate_audio_duration(uploaded_file) -> bool:
    """音声の長さが学習に適した範囲（3秒〜15秒）かどうかを検証する。

    範囲外または読み込み不可の場合は st.error でエラーを表示し False を返す。
    """
    try:
        duration = get_audio_duration(uploaded_file)
    except ValueError as e:
        st.error(T["audio_load_error"].format(error=str(e)))
        return False
    if duration < VOICE_LEARNING_MIN_DURATION or duration > VOICE_LEARNING_MAX_DURATION:
        st.error(
            T["audio_duration_error"].format(
                duration=duration,
                min=VOICE_LEARNING_MIN_DURATION,
                max=VOICE_LEARNING_MAX_DURATION,
            )
        )
        return False
    return True


def show_completion_notification(message: str | None = None):
    """完了通知を表示する（Toast + 音声）."""
    if message is None:
        message = T["completion_default"]
    st.toast(message, icon="✅")
    components.html(
        """
        <script>
        const audio = new Audio('/static/notify.ogg');
        audio.load();
        audio.play().catch(() => {
            console.log('音声再生がブロックされました');
        });
        </script>
        """,
        height=0,
    )


# --- サイドバー ---

with st.sidebar:
    st.title("Qwen3-TTS WebUI")
    st.caption(
        T["device_label"].format(device=st.session_state.engine.get_device_info())
    )

    st.selectbox(
        T["ui_lang_selector"],
        UI_LANGUAGES,
        format_func=lambda x: UI_LANGUAGE_NAMES[x],
        key="ui_lang",
        on_change=on_ui_lang_change,
        disabled=st.session_state.is_generating,
    )

    st.divider()

    model_size = st.selectbox(
        T["model_size"],
        ["1.7B", "0.6B"],
        index=0,
        help=T["model_size_help"],
        disabled=st.session_state.is_generating,
    )

    st.divider()

    _mode_labels = {
        MODE_TRAIN: T["mode_train"],
        MODE_TTS: T["mode_tts"],
        MODE_INSTANT: T["mode_instant"],
        MODE_WEBAPI: T["mode_webapi"],
    }
    mode = st.radio(
        T["mode_select"],
        [MODE_TRAIN, MODE_TTS, MODE_INSTANT, MODE_WEBAPI],
        format_func=lambda x: _mode_labels[x],
        index=0,
        disabled=st.session_state.is_generating,
    )

    st.divider()

    # 生成パラメータ設定（音声合成モードで使用）
    with st.expander(T["gen_params"], expanded=False):
        gen_temperature = st.slider(
            T["temperature"],
            min_value=0.30,
            max_value=1.30,
            value=0.65,
            step=0.05,
            key="gen_temperature",
            help=T["temperature_help"],
            disabled=st.session_state.is_generating,
        )
        gen_top_p = st.slider(
            T["top_p"],
            min_value=0.80,
            max_value=1.00,
            value=0.90,
            step=0.05,
            key="gen_top_p",
            help=T["top_p_help"],
            disabled=st.session_state.is_generating,
        )
        gen_top_k = st.slider(
            T["top_k"],
            min_value=10,
            max_value=50,
            value=50,
            step=1,
            key="gen_top_k",
            help=T["top_k_help"],
            disabled=st.session_state.is_generating,
        )
        gen_repetition_penalty = st.slider(
            T["repetition_penalty"],
            min_value=1.00,
            max_value=1.50,
            value=1.15,
            step=0.05,
            key="gen_repetition_penalty",
            help=T["repetition_penalty_help"],
            disabled=st.session_state.is_generating,
        )

    st.divider()

    # モードに応じた履歴クリアボタン
    if mode == MODE_TTS and st.session_state.tts_history:
        if st.button(
            T["clear_history"], key="clear_tts", disabled=st.session_state.is_generating
        ):
            st.session_state.tts_history = []
            st.rerun()
    elif mode == MODE_INSTANT and st.session_state.instant_history:
        if st.button(
            T["clear_history"],
            key="clear_instant",
            disabled=st.session_state.is_generating,
        ):
            st.session_state.instant_history = []
            st.rerun()


# =============================================================================
# モード1: オリジナルボイスモデル学習
# =============================================================================
if mode == MODE_TRAIN:
    st.header(T["train_header"])
    st.markdown(T["train_desc"])

    col_create, col_saved = st.columns([3, 2])

    with col_create:
        st.subheader(T["train_new_model"])

        audio_file = st.file_uploader(
            T["train_audio_file"],
            type=["wav", "mp3", "flac", "ogg", "m4a"],
            key="train_audio",
            help=T["train_audio_help"],
        )

        ref_text = st.text_area(
            T["train_ref_text"],
            placeholder=T["train_ref_text_placeholder"],
            key="train_text",
        )

        ref_lang = st.selectbox(
            T["train_ref_lang"],
            SUPPORTED_LANGUAGES,
            index=_DEFAULT_TTS_INDEX,
            key="train_lang",
        )

        nickname = st.text_input(
            T["train_nickname"],
            placeholder=T["train_nickname_placeholder"],
            key="train_nickname",
        )

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            create_clicked = st.button(
                T["train_create_btn"], type="primary", use_container_width=True
            )

        with col_btn2:
            preview_clicked = st.button(
                T["train_preview_btn"], use_container_width=True
            )

        if create_clicked:
            if not audio_file or not ref_text or not nickname:
                st.error(T["train_error_missing"])
            elif not validate_audio_duration(audio_file):
                pass
            else:
                audio_path = save_uploaded_audio(audio_file)
                st.session_state.is_generating = True
                try:
                    with st.spinner(T["train_spinner"]):
                        prompt_items = st.session_state.engine.create_voice_prompt(
                            ref_audio=audio_path,
                            ref_text=ref_text,
                            model_size=model_size,
                        )
                        save_voice(nickname, prompt_items, ref_lang, model_size)
                    st.success(T["train_success"].format(nickname=nickname))
                    show_completion_notification(T["train_notify"])
                finally:
                    st.session_state.is_generating = False
                st.rerun()

        if preview_clicked:
            if not audio_file or not ref_text:
                st.error(T["train_preview_error"])
            elif not validate_audio_duration(audio_file):
                pass
            else:
                audio_path = save_uploaded_audio(audio_file)
                greeting = GREETINGS.get(ref_lang, GREETINGS["English"])
                st.session_state.is_generating = True
                try:
                    with st.spinner(T["train_preview_spinner"].format(lang=ref_lang)):
                        prompt_items = st.session_state.engine.create_voice_prompt(
                            ref_audio=audio_path,
                            ref_text=ref_text,
                            model_size=model_size,
                        )
                        wav, sr = st.session_state.engine.generate_speech(
                            text=greeting,
                            language=ref_lang,
                            voice_clone_prompt=prompt_items,
                            model_size=model_size,
                        )
                    st.info(T["train_preview_info"].format(greeting=greeting))
                    show_completion_notification(T["train_preview_notify"])
                    st.audio(audio_to_bytes(wav, sr), format="audio/wav")
                finally:
                    st.session_state.is_generating = False

    with col_saved:
        st.subheader(T["train_saved_models"])
        voices = list_voices_by_size(model_size)

        if not voices:
            st.info(T["train_no_models"].format(size=model_size))

        for voice in voices:
            with st.container(border=True):
                st.markdown(f"**{voice['nickname']}**")
                st.caption(
                    T["train_caption"].format(
                        lang=voice["language"],
                        size=voice["model_size"],
                        date=voice["created_at"][:10],
                    )
                )

                c1, c2 = st.columns(2)
                with c1:
                    data, filename = export_voice(
                        voice["nickname"], voice["model_size"]
                    )
                    st.download_button(
                        T["train_export_btn"],
                        data=data,
                        file_name=filename,
                        mime="application/octet-stream",
                        use_container_width=True,
                        key=f"export_{voice['nickname']}",
                    )
                with c2:
                    if st.button(
                        T["train_delete_btn"],
                        key=f"del_{voice['nickname']}",
                        use_container_width=True,
                    ):
                        remove_voice(voice["nickname"], voice["model_size"])
                        st.rerun()

        st.divider()
        st.subheader(T["train_import_section"])

        import_file = st.file_uploader(
            T["train_import_file"].format(size=model_size),
            type=["pt"],
            key="import_file",
        )
        import_nickname = st.text_input(T["train_import_name"], key="import_nickname")
        import_lang = st.selectbox(
            T["train_import_lang"],
            SUPPORTED_LANGUAGES,
            index=_DEFAULT_TTS_INDEX,
            key="import_lang",
        )

        if st.button(T["train_import_btn"], use_container_width=True):
            if import_file and import_nickname:
                try:
                    import_voice(
                        import_nickname, import_file.read(), import_lang, model_size
                    )
                    st.success(T["train_import_success"].format(name=import_nickname))
                    st.rerun()
                except ValueError as e:
                    st.error(T["train_import_fail"].format(error=e))
            else:
                st.error(T["train_import_error_missing"])


# =============================================================================
# モード2: 音声合成
# =============================================================================
elif mode == MODE_TTS:
    st.header(T["tts_header"])

    # 設定エリア
    col_s1, col_s2 = st.columns(2)

    with col_s1:
        _vs_labels = {
            VOICE_SOURCE_SAVED: T["tts_source_saved"],
            VOICE_SOURCE_UPLOAD: T["tts_source_upload"],
        }
        voice_source = st.radio(
            T["tts_voice_source"],
            [VOICE_SOURCE_SAVED, VOICE_SOURCE_UPLOAD],
            format_func=lambda x: _vs_labels[x],
            horizontal=True,
            key="tts_source",
        )

    with col_s2:
        output_lang = st.selectbox(
            T["tts_output_lang"],
            SUPPORTED_LANGUAGES,
            index=_DEFAULT_TTS_INDEX,
            key="tts_lang",
        )

    # ボイスモデルの読み込み
    voice_prompt = None

    if voice_source == VOICE_SOURCE_SAVED:
        voices = list_voices_by_size(model_size)
        voice_options = [v["nickname"] for v in voices]
        if voice_options:
            selected_voice = st.selectbox(
                T["tts_voice_model"], voice_options, key="tts_voice"
            )
            if selected_voice:
                voice_prompt = load_voice(selected_voice, model_size)
        else:
            st.warning(T["tts_no_models"].format(size=model_size))
    else:
        uploaded_model = st.file_uploader(
            T["tts_upload_model"],
            type=["pt"],
            key="tts_upload_model",
        )
        if uploaded_model:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pt") as f:
                f.write(uploaded_model.read())
                voice_prompt = torch.load(f.name, weights_only=False)

    st.divider()

    # チャットインターフェース
    for msg in st.session_state.tts_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "audio" in msg:
                st.audio(msg["audio"], format="audio/wav")

    if text_input := st.chat_input(T["tts_chat_input"]):
        if voice_prompt is None:
            st.error(T["tts_no_voice"])
        else:
            # ユーザーメッセージ
            user_msg = {
                "role": "user",
                "content": text_input,
                "id": str(uuid.uuid4()),
            }
            st.session_state.tts_history.append(user_msg)

            with st.chat_message("user"):
                st.markdown(text_input)

            # 音声生成
            with st.chat_message("assistant"):
                st.session_state.is_generating = True
                try:
                    with st.spinner(T["tts_spinner"]):
                        wav, sr = st.session_state.engine.generate_speech(
                            text=text_input,
                            language=output_lang,
                            voice_clone_prompt=voice_prompt,
                            model_size=model_size,
                            temperature=gen_temperature,
                            repetition_penalty=gen_repetition_penalty,
                            top_p=gen_top_p,
                            top_k=gen_top_k,
                        )
                    audio_bytes = audio_to_bytes(wav, sr)
                    msg_id = str(uuid.uuid4())
                    st.markdown(T["tts_generated"])
                    show_completion_notification(T["tts_notify"])
                    st.audio(audio_bytes, format="audio/wav")
                    st.session_state.tts_history.append(
                        {
                            "role": "assistant",
                            "content": T["tts_generated"],
                            "audio": audio_bytes,
                            "id": msg_id,
                        }
                    )
                finally:
                    st.session_state.is_generating = False


# =============================================================================
# モード3: オリジナル音声即時合成
# =============================================================================
elif mode == MODE_INSTANT:
    st.header(T["instant_header"])
    st.markdown(T["instant_desc"])

    col_ref, col_out = st.columns(2)

    with col_ref:
        st.subheader(T["instant_ref_section"])
        instant_audio = st.file_uploader(
            T["instant_audio"],
            type=["wav", "mp3", "flac", "ogg", "m4a"],
            key="instant_audio",
            help=T["instant_audio_help"],
        )
        instant_ref_text = st.text_area(
            T["instant_ref_text"],
            placeholder=T["instant_ref_text_placeholder"],
            key="instant_ref_text",
        )
        instant_ref_lang = st.selectbox(
            T["instant_ref_lang"],
            SUPPORTED_LANGUAGES,
            index=_DEFAULT_TTS_INDEX,
            key="instant_ref_lang",
        )

    with col_out:
        st.subheader(T["instant_out_section"])
        instant_out_lang = st.selectbox(
            T["instant_out_lang"],
            SUPPORTED_LANGUAGES,
            index=_DEFAULT_TTS_INDEX,
            key="instant_out_lang",
        )

    st.divider()

    # チャットインターフェース
    for msg in st.session_state.instant_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "audio" in msg:
                st.audio(msg["audio"], format="audio/wav")

    if text_input := st.chat_input(T["instant_chat_input"]):
        if not instant_audio or not instant_ref_text:
            st.error(T["instant_error_missing"])
        elif not validate_audio_duration(instant_audio):
            pass
        else:
            # ユーザーメッセージ
            user_msg = {
                "role": "user",
                "content": text_input,
                "id": str(uuid.uuid4()),
            }
            st.session_state.instant_history.append(user_msg)

            with st.chat_message("user"):
                st.markdown(text_input)

            # 音声生成
            with st.chat_message("assistant"):
                audio_path = save_uploaded_audio(instant_audio)
                st.session_state.is_generating = True
                try:
                    with st.spinner(T["instant_spinner"]):
                        wav, sr = st.session_state.engine.generate_speech_direct(
                            text=text_input,
                            language=instant_out_lang,
                            ref_audio=audio_path,
                            ref_text=instant_ref_text,
                            model_size=model_size,
                            temperature=gen_temperature,
                            repetition_penalty=gen_repetition_penalty,
                            top_p=gen_top_p,
                            top_k=gen_top_k,
                        )
                    audio_bytes = audio_to_bytes(wav, sr)
                    msg_id = str(uuid.uuid4())
                    st.markdown(T["instant_generated"])
                    st.audio(audio_bytes, format="audio/wav")
                    st.session_state.instant_history.append(
                        {
                            "role": "assistant",
                            "content": T["instant_generated"],
                            "audio": audio_bytes,
                            "id": msg_id,
                        }
                    )
                finally:
                    st.session_state.is_generating = False


# =============================================================================
# モード4: 音声合成WebAPI
# =============================================================================
elif mode == MODE_WEBAPI:
    st.header(T["webapi_header"])
    st.markdown(T["webapi_desc"])

    st.subheader(T["webapi_start_cmd"])

    col_cmd1, col_cmd2 = st.columns(2)
    with col_cmd1:
        st.code("uv run python api_server.py", language="bash")
        st.caption(T["webapi_default_caption"])

    with col_cmd2:
        st.code(
            "uv run python api_server.py --host 0.0.0.0 --port 50021",
            language="bash",
        )
        st.caption(T["webapi_network_caption"])

    st.info(T["webapi_model_info"])

    st.divider()

    st.subheader(T["webapi_endpoints"])

    with st.expander(T["webapi_version"], expanded=False):
        st.code("curl http://127.0.0.1:50021/version", language="bash")

    with st.expander(T["webapi_speakers"], expanded=False):
        st.code("curl http://127.0.0.1:50021/speakers", language="bash")
        st.caption(T["webapi_speakers_caption"])

    with st.expander(T["webapi_synthesis"], expanded=True):
        st.markdown(T["webapi_step1"])
        st.code(
            'curl -X POST "http://127.0.0.1:50021/audio_query?text=こんにちは&speaker=0"'
            " > query.json",
            language="bash",
        )
        st.markdown(T["webapi_step2"])
        st.code(
            'curl -X POST "http://127.0.0.1:50021/synthesis?speaker=0"'
            " -H 'Content-Type: application/json'"
            " -d @query.json"
            " --output output.wav",
            language="bash",
        )

    st.divider()

    st.subheader(T["webapi_ext_endpoints"])

    with st.expander(T["webapi_voice_models"], expanded=False):
        st.code("curl http://127.0.0.1:50021/voice_models", language="bash")

    st.divider()

    st.subheader(T["webapi_api_docs"])
    st.markdown(T["webapi_api_docs_desc"])

    st.divider()

    st.subheader(T["webapi_python_sample"])
    st.code(
        """import requests

BASE_URL = "http://127.0.0.1:50021"

# Step 1: Create AudioQuery
response = requests.post(
    f"{BASE_URL}/audio_query",
    params={"text": "こんにちは", "speaker": 0},
)
query = response.json()

# Step 2: Speech synthesis
response = requests.post(
    f"{BASE_URL}/synthesis",
    params={"speaker": 0},
    json=query,
)

# Save as WAV file
with open("output.wav", "wb") as f:
    f.write(response.content)
""",
        language="python",
    )
