"""国際化サポート - 日本語 / English / 中文."""

import locale
import os

# サポートする UI 言語コード
UI_LANGUAGES = ["ja", "en", "zh"]
DEFAULT_UI_LANGUAGE = "ja"

# UI 言語の表示名（ネイティブ表記）
UI_LANGUAGE_NAMES: dict[str, str] = {
    "ja": "🇯🇵 日本語",
    "en": "🇺🇸 English",
    "zh": "🇨🇳 中文",
}

# TTS 言語名 → SUPPORTED_LANGUAGES のインデックスはアプリ側で解決する
_TTS_LANG_MAP: dict[str, str] = {
    "ja": "Japanese",
    "en": "English",
    "zh": "Chinese",
}


def detect_ui_language() -> str:
    """システム言語を検出し、対応する UI 言語コードを返す。

    優先順位: 環境変数 (LANG / LANGUAGE / LC_ALL / LC_MESSAGES) → locale.getlocale()
    対応言語: ja / en / zh。それ以外はデフォルト（日本語）。
    """
    for env_var in ("LANG", "LANGUAGE", "LC_ALL", "LC_MESSAGES"):
        lang = os.environ.get(env_var, "").lower()
        if lang:
            if lang.startswith("ja"):
                return "ja"
            if lang.startswith("zh"):
                return "zh"
            if lang.startswith("en"):
                return "en"
    try:
        loc = (locale.getlocale()[0] or "").lower()
        if loc.startswith("ja"):
            return "ja"
        if loc.startswith("zh"):
            return "zh"
        if loc.startswith("en"):
            return "en"
    except Exception:
        pass
    return DEFAULT_UI_LANGUAGE


def get_tts_default_language(ui_lang: str) -> str:
    """UI 言語コードからデフォルトの TTS 言語名 (SUPPORTED_LANGUAGES の要素) を返す。"""
    return _TTS_LANG_MAP.get(ui_lang, _TTS_LANG_MAP[DEFAULT_UI_LANGUAGE])


# ---------------------------------------------------------------------------
# 翻訳辞書
# ---------------------------------------------------------------------------

TRANSLATIONS: dict[str, dict[str, str]] = {
    # ------------------------------------------------------------------ 日本語
    "ja": {
        # 表示言語セレクタ
        "ui_lang_selector": "表示言語",
        # デバイス
        "device_label": "デバイス: {device}",
        # サイドバー
        "model_size": "モデルサイズ",
        "model_size_help": "1.7B（デフォルト）は高品質、0.6B は軽量版です。",
        "mode_select": "モード選択",
        "mode_train": "ボイスモデル学習",
        "mode_tts": "音声合成",
        "mode_instant": "即時音声合成",
        "mode_webapi": "音声合成 WebAPI",
        "gen_params": "生成パラメータ設定",
        "temperature": "温度（感情値）",
        "temperature_help": (
            "感情の豊かさを制御します。"
            "高いほど表現豊かでランダムな発音、低いほど落ち着いた安定した発音になります。"
        ),
        "top_p": "Top-p（核サンプリング）",
        "top_p_help": (
            "累積確率が上位 p 以内のトークンのみからサンプリングします。"
            "低いほど安定した出力になります。"
        ),
        "top_k": "Top-k",
        "top_k_help": (
            "確率の高い上位 k 件のトークンのみからサンプリングします。"
            "低いほど安定した出力になります。"
        ),
        "repetition_penalty": "繰り返し抑制（Repetition Penalty）",
        "repetition_penalty_help": (
            "同じ音やフレーズの繰り返しを抑制します。高いほど繰り返しが起きにくくなります。"
        ),
        "clear_history": "チャット履歴クリア",
        # モード 1: ボイスモデル学習
        "train_header": "ボイスモデル学習",
        "train_desc": "リファレンス音声からオリジナルボイスモデルを作成します。",
        "train_new_model": "新規モデル作成",
        "train_audio_file": "リファレンス音声ファイル",
        "train_audio_help": "6〜15 秒のクリアな音声（WAV 推奨）をご用意ください。",
        "train_ref_text": "音声の文字起こし",
        "train_ref_text_placeholder": "アップロードした音声の内容をテキストで入力してください",
        "train_ref_lang": "リファレンス音声の言語",
        "train_nickname": "ニックネーム",
        "train_nickname_placeholder": "ボイスモデルの名前を入力",
        "train_create_btn": "モデル作成",
        "train_preview_btn": "挨拶プレビュー",
        "train_error_missing": "音声ファイル、文字起こし、ニックネームをすべて入力してください。",
        "train_spinner": "ボイスモデルを作成中...",
        "train_success": "ボイスモデル '{nickname}' を作成しました。",
        "train_notify": "ボイスモデル作成完了",
        "train_preview_error": "音声ファイルと文字起こしを入力してください。",
        "train_preview_spinner": "挨拶音声を生成中（{lang}）...",
        "train_preview_info": "挨拶: {greeting}",
        "train_preview_notify": "プレビュー完了",
        "train_saved_models": "保存済みモデル",
        "train_no_models": "保存されたボイスモデルはありません（{size}）。",
        "train_caption": "言語: {lang} | サイズ: {size} | 作成日: {date}",
        "train_export_btn": "エクスポート",
        "train_delete_btn": "削除",
        "train_import_section": "モデルインポート",
        "train_import_file": "ボイスモデルファイル (.pt) - {size} 向けのみ",
        "train_import_name": "インポート名",
        "train_import_lang": "言語",
        "train_import_btn": "インポート",
        "train_import_success": "'{name}' をインポートしました。",
        "train_import_fail": "インポート失敗: {error}",
        "train_import_error_missing": "ファイルとインポート名を入力してください。",
        # モード 2: 音声合成
        "tts_header": "音声合成",
        "tts_voice_source": "ボイスモデルソース",
        "tts_source_saved": "保存済みモデル",
        "tts_source_upload": "ファイルアップロード",
        "tts_output_lang": "出力言語",
        "tts_voice_model": "ボイスモデル",
        "tts_no_models": (
            "保存されたボイスモデルがありません（{size}）。"
            "「ボイスモデル学習」モードで先にモデルを作成してください。"
        ),
        "tts_upload_model": "ボイスモデルファイル (.pt)",
        "tts_chat_input": "合成するテキストを入力してください",
        "tts_no_voice": "ボイスモデルを選択またはアップロードしてください。",
        "tts_spinner": "音声を生成中...",
        "tts_generated": "音声を生成しました",
        "tts_notify": "音声合成完了",
        # モード 3: 即時合成
        "instant_header": "即時音声合成",
        "instant_desc": "リファレンス音声から直接音声合成を行います。ボイスモデルはキャッシュされません。",
        "instant_ref_section": "リファレンス設定",
        "instant_out_section": "出力設定",
        "instant_audio": "リファレンス音声",
        "instant_audio_help": "6〜15 秒のクリアな音声（WAV 推奨）をご用意ください。",
        "instant_ref_text": "文字起こし",
        "instant_ref_text_placeholder": "リファレンス音声の内容",
        "instant_ref_lang": "リファレンス言語",
        "instant_out_lang": "出力言語",
        "instant_chat_input": "合成するテキストを入力",
        "instant_error_missing": "リファレンス音声と文字起こしを入力してください。",
        "instant_spinner": "リファレンス音声を解析して音声を生成中...",
        "instant_generated": "音声を生成しました",
        # モード 4: WebAPI
        "webapi_header": "音声合成 WebAPI",
        "webapi_desc": (
            "VOICEVOX 互換の HTTP API サーバーとして利用できます。\n"
            "以下のコマンドで API サーバーを起動し、他のアプリケーションから音声合成を呼び出せます。"
        ),
        "webapi_start_cmd": "サーバー起動コマンド",
        "webapi_default_caption": "デフォルト: host=127.0.0.1, port=50021",
        "webapi_network_caption": "ネットワーク公開の例",
        "webapi_model_info": (
            "モデルは常に **1.7B** を使用します。"
            "ボイスモデルはこの WebUI で学習・保存済みのものを使用します。"
        ),
        "webapi_endpoints": "主要 API エンドポイント（VOICEVOX 互換）",
        "webapi_version": "GET /version - バージョン取得",
        "webapi_speakers": "GET /speakers - 話者（ボイスモデル）一覧",
        "webapi_speakers_caption": (
            "保存済みボイスモデルが話者として返されます。"
            "speaker_id は /voice_models で確認できます。"
        ),
        "webapi_synthesis": "POST /audio_query + POST /synthesis - 音声合成（2 ステップ）",
        "webapi_step1": "**ステップ 1: AudioQuery を作成**",
        "webapi_step2": "**ステップ 2: 音声合成**",
        "webapi_ext_endpoints": "拡張 API エンドポイント",
        "webapi_voice_models": "GET /voice_models - ボイスモデル一覧（拡張）",
        "webapi_api_docs": "API ドキュメント",
        "webapi_api_docs_desc": (
            "サーバー起動後、以下の URL でインタラクティブな API ドキュメントを参照できます:\n\n"
            "- **Swagger UI**: http://127.0.0.1:50021/docs\n"
            "- **ReDoc**: http://127.0.0.1:50021/redoc"
        ),
        "webapi_python_sample": "Python サンプルコード",
        # ユーティリティ
        "audio_load_error": "音声ファイルの読み込みに失敗しました: {error}",
        "audio_duration_error": (
            "音声の長さが {duration:.1f} 秒です。"
            "音声学習には {min:.0f} 秒〜{max:.0f} 秒の音声を使用してください。"
        ),
        "completion_default": "完了しました！",
    },
    # ------------------------------------------------------------------ English
    "en": {
        # UI language selector
        "ui_lang_selector": "Display Language",
        # Device
        "device_label": "Device: {device}",
        # Sidebar
        "model_size": "Model Size",
        "model_size_help": "1.7B (default) is high quality; 0.6B is a lightweight version.",
        "mode_select": "Mode",
        "mode_train": "Voice Model Training",
        "mode_tts": "Text-to-Speech",
        "mode_instant": "Instant Voice Synthesis",
        "mode_webapi": "TTS Web API",
        "gen_params": "Generation Parameters",
        "temperature": "Temperature (Emotion)",
        "temperature_help": (
            "Controls expressiveness. "
            "Higher values produce more expressive and varied speech; "
            "lower values produce calmer, more stable output."
        ),
        "top_p": "Top-p (Nucleus Sampling)",
        "top_p_help": (
            "Samples only from tokens within the top-p cumulative probability. "
            "Lower values produce more stable output."
        ),
        "top_k": "Top-k",
        "top_k_help": (
            "Samples only from the top-k most probable tokens. "
            "Lower values produce more stable output."
        ),
        "repetition_penalty": "Repetition Penalty",
        "repetition_penalty_help": (
            "Suppresses repeated sounds or phrases. Higher values reduce repetition."
        ),
        "clear_history": "Clear Chat History",
        # Mode 1: Voice Model Training
        "train_header": "Voice Model Training",
        "train_desc": "Create an original voice model from a reference audio.",
        "train_new_model": "Create New Model",
        "train_audio_file": "Reference Audio File",
        "train_audio_help": "Recommend 6–15 seconds of clear audio (WAV preferred).",
        "train_ref_text": "Transcription",
        "train_ref_text_placeholder": "Enter the text content of the uploaded audio",
        "train_ref_lang": "Reference Audio Language",
        "train_nickname": "Nickname",
        "train_nickname_placeholder": "Enter a name for the voice model",
        "train_create_btn": "Create Model",
        "train_preview_btn": "Greeting Preview",
        "train_error_missing": "Please provide the audio file, transcription, and nickname.",
        "train_spinner": "Creating voice model...",
        "train_success": "Voice model '{nickname}' created.",
        "train_notify": "Voice model creation complete",
        "train_preview_error": "Please provide the audio file and transcription.",
        "train_preview_spinner": "Generating greeting audio ({lang})...",
        "train_preview_info": "Greeting: {greeting}",
        "train_preview_notify": "Preview complete",
        "train_saved_models": "Saved Models",
        "train_no_models": "No saved voice models ({size}).",
        "train_caption": "Language: {lang} | Size: {size} | Created: {date}",
        "train_export_btn": "Export",
        "train_delete_btn": "Delete",
        "train_import_section": "Import Model",
        "train_import_file": "Voice Model File (.pt) - {size} only",
        "train_import_name": "Import Name",
        "train_import_lang": "Language",
        "train_import_btn": "Import",
        "train_import_success": "'{name}' imported successfully.",
        "train_import_fail": "Import failed: {error}",
        "train_import_error_missing": "Please provide the file and import name.",
        # Mode 2: TTS
        "tts_header": "Text-to-Speech",
        "tts_voice_source": "Voice Model Source",
        "tts_source_saved": "Saved Models",
        "tts_source_upload": "File Upload",
        "tts_output_lang": "Output Language",
        "tts_voice_model": "Voice Model",
        "tts_no_models": (
            "No saved voice models ({size}). "
            "Please create a model in 'Voice Model Training' mode first."
        ),
        "tts_upload_model": "Voice Model File (.pt)",
        "tts_chat_input": "Enter text to synthesize",
        "tts_no_voice": "Please select or upload a voice model.",
        "tts_spinner": "Generating audio...",
        "tts_generated": "Audio generated",
        "tts_notify": "Speech synthesis complete",
        # Mode 3: Instant
        "instant_header": "Instant Voice Synthesis",
        "instant_desc": (
            "Synthesize speech directly from reference audio. "
            "Voice model is not cached."
        ),
        "instant_ref_section": "Reference Settings",
        "instant_out_section": "Output Settings",
        "instant_audio": "Reference Audio",
        "instant_audio_help": "Recommend 6–15 seconds of clear audio (WAV preferred).",
        "instant_ref_text": "Transcription",
        "instant_ref_text_placeholder": "Content of the reference audio",
        "instant_ref_lang": "Reference Language",
        "instant_out_lang": "Output Language",
        "instant_chat_input": "Enter text to synthesize",
        "instant_error_missing": "Please provide the reference audio and transcription.",
        "instant_spinner": "Analyzing reference audio and generating speech...",
        "instant_generated": "Audio generated",
        # Mode 4: WebAPI
        "webapi_header": "TTS Web API",
        "webapi_desc": (
            "Available as a VOICEVOX-compatible HTTP API server.\n"
            "Start the API server with the command below to call speech synthesis "
            "from other applications."
        ),
        "webapi_start_cmd": "Server Start Command",
        "webapi_default_caption": "Default: host=127.0.0.1, port=50021",
        "webapi_network_caption": "Example for network access",
        "webapi_model_info": (
            "Always uses the **1.7B** model. "
            "Voice models trained and saved in this WebUI are used."
        ),
        "webapi_endpoints": "Main API Endpoints (VOICEVOX-compatible)",
        "webapi_version": "GET /version - Get version",
        "webapi_speakers": "GET /speakers - Speaker (voice model) list",
        "webapi_speakers_caption": (
            "Saved voice models are returned as speakers. "
            "Check speaker_id at /voice_models."
        ),
        "webapi_synthesis": "POST /audio_query + POST /synthesis - Speech synthesis (2 steps)",
        "webapi_step1": "**Step 1: Create AudioQuery**",
        "webapi_step2": "**Step 2: Speech synthesis**",
        "webapi_ext_endpoints": "Extended API Endpoints",
        "webapi_voice_models": "GET /voice_models - Voice model list (extended)",
        "webapi_api_docs": "API Documentation",
        "webapi_api_docs_desc": (
            "After starting the server, refer to the interactive API documentation at:\n\n"
            "- **Swagger UI**: http://127.0.0.1:50021/docs\n"
            "- **ReDoc**: http://127.0.0.1:50021/redoc"
        ),
        "webapi_python_sample": "Python Sample Code",
        # Utility
        "audio_load_error": "Failed to load audio file: {error}",
        "audio_duration_error": (
            "Audio duration is {duration:.1f}s. "
            "Please use audio between {min:.0f}s and {max:.0f}s for voice training."
        ),
        "completion_default": "Done!",
    },
    # ------------------------------------------------------------------ 中文
    "zh": {
        # 界面语言选择器
        "ui_lang_selector": "界面语言",
        # 设备
        "device_label": "设备: {device}",
        # 侧边栏
        "model_size": "模型大小",
        "model_size_help": "1.7B（默认）为高质量版本，0.6B 为轻量版本。",
        "mode_select": "模式选择",
        "mode_train": "语音模型训练",
        "mode_tts": "语音合成",
        "mode_instant": "即时语音合成",
        "mode_webapi": "语音合成 Web API",
        "gen_params": "生成参数设置",
        "temperature": "温度（情感值）",
        "temperature_help": (
            "控制表现力。值越高，语音越有表现力且随机；值越低，语音越平稳。"
        ),
        "top_p": "Top-p（核采样）",
        "top_p_help": "仅从累积概率在前 p 以内的词元中采样。值越低，输出越稳定。",
        "top_k": "Top-k",
        "top_k_help": "仅从概率最高的前 k 个词元中采样。值越低，输出越稳定。",
        "repetition_penalty": "重复抑制（Repetition Penalty）",
        "repetition_penalty_help": "抑制相同音节或短语的重复。值越高，重复越少。",
        "clear_history": "清除聊天记录",
        # 模式 1: 声音模型训练
        "train_header": "语音模型训练",
        "train_desc": "从参考音频创建原创声音模型。",
        "train_new_model": "创建新模型",
        "train_audio_file": "参考音频文件",
        "train_audio_help": "建议使用 6～15 秒的清晰音频（推荐 WAV 格式）。",
        "train_ref_text": "音频转录文本",
        "train_ref_text_placeholder": "请输入上传音频的文本内容",
        "train_ref_lang": "参考音频语言",
        "train_nickname": "昵称",
        "train_nickname_placeholder": "输入声音模型的名称",
        "train_create_btn": "创建模型",
        "train_preview_btn": "问候预览",
        "train_error_missing": "请提供音频文件、转录文本和昵称。",
        "train_spinner": "正在创建声音模型...",
        "train_success": "声音模型 '{nickname}' 已创建。",
        "train_notify": "声音模型创建完成",
        "train_preview_error": "请提供音频文件和转录文本。",
        "train_preview_spinner": "正在生成问候音频（{lang}）...",
        "train_preview_info": "问候语: {greeting}",
        "train_preview_notify": "预览完成",
        "train_saved_models": "已保存的模型",
        "train_no_models": "没有已保存的声音模型（{size}）。",
        "train_caption": "语言: {lang} | 大小: {size} | 创建日期: {date}",
        "train_export_btn": "导出",
        "train_delete_btn": "删除",
        "train_import_section": "导入模型",
        "train_import_file": "声音模型文件 (.pt) - 仅限 {size}",
        "train_import_name": "导入名称",
        "train_import_lang": "语言",
        "train_import_btn": "导入",
        "train_import_success": "'{name}' 已成功导入。",
        "train_import_fail": "导入失败: {error}",
        "train_import_error_missing": "请提供文件和导入名称。",
        # 模式 2: 语音合成
        "tts_header": "语音合成",
        "tts_voice_source": "声音模型来源",
        "tts_source_saved": "已保存的模型",
        "tts_source_upload": "文件上传",
        "tts_output_lang": "输出语言",
        "tts_voice_model": "声音模型",
        "tts_no_models": (
            "没有已保存的声音模型（{size}）。请先在『语音模型训练』模式中创建模型。"
        ),
        "tts_upload_model": "声音模型文件 (.pt)",
        "tts_chat_input": "请输入要合成的文本",
        "tts_no_voice": "请选择或上传声音模型。",
        "tts_spinner": "正在生成音频...",
        "tts_generated": "音频已生成",
        "tts_notify": "语音合成完成",
        # 模式 3: 即时合成
        "instant_header": "即时语音合成",
        "instant_desc": "直接从参考音频进行语音合成。声音模型不会被缓存。",
        "instant_ref_section": "参考设置",
        "instant_out_section": "输出设置",
        "instant_audio": "参考音频",
        "instant_audio_help": "建议使用 6～15 秒的清晰音频（推荐 WAV 格式）。",
        "instant_ref_text": "转录文本",
        "instant_ref_text_placeholder": "参考音频的内容",
        "instant_ref_lang": "参考语言",
        "instant_out_lang": "输出语言",
        "instant_chat_input": "请输入要合成的文本",
        "instant_error_missing": "请提供参考音频和转录文本。",
        "instant_spinner": "正在分析参考音频并生成语音...",
        "instant_generated": "音频已生成",
        # 模式 4: WebAPI
        "webapi_header": "语音合成 Web API",
        "webapi_desc": (
            "可作为 VOICEVOX 兼容的 HTTP API 服务器使用。\n"
            "使用以下命令启动 API 服务器，从其他应用程序调用语音合成。"
        ),
        "webapi_start_cmd": "服务器启动命令",
        "webapi_default_caption": "默认: host=127.0.0.1, port=50021",
        "webapi_network_caption": "网络访问示例",
        "webapi_model_info": (
            "始终使用 **1.7B** 模型。使用在此 WebUI 中训练和保存的声音模型。"
        ),
        "webapi_endpoints": "主要 API 端点（VOICEVOX 兼容）",
        "webapi_version": "GET /version - 获取版本",
        "webapi_speakers": "GET /speakers - 说话人（声音模型）列表",
        "webapi_speakers_caption": (
            "已保存的声音模型将作为说话人返回。可在 /voice_models 查看 speaker_id。"
        ),
        "webapi_synthesis": "POST /audio_query + POST /synthesis - 语音合成（2 步骤）",
        "webapi_step1": "**步骤 1: 创建 AudioQuery**",
        "webapi_step2": "**步骤 2: 语音合成**",
        "webapi_ext_endpoints": "扩展 API 端点",
        "webapi_voice_models": "GET /voice_models - 声音模型列表（扩展）",
        "webapi_api_docs": "API 文档",
        "webapi_api_docs_desc": (
            "启动服务器后，可在以下 URL 查看交互式 API 文档:\n\n"
            "- **Swagger UI**: http://127.0.0.1:50021/docs\n"
            "- **ReDoc**: http://127.0.0.1:50021/redoc"
        ),
        "webapi_python_sample": "Python 示例代码",
        # 工具
        "audio_load_error": "音频文件加载失败: {error}",
        "audio_duration_error": (
            "音频时长为 {duration:.1f} 秒。"
            "声音训练请使用 {min:.0f} 秒至 {max:.0f} 秒的音频。"
        ),
        "completion_default": "完成！",
    },
}


def get_translations(ui_lang: str) -> dict[str, str]:
    """指定された UI 言語の翻訳辞書を返す。未対応言語はデフォルト（日本語）を返す。"""
    return TRANSLATIONS.get(ui_lang, TRANSLATIONS[DEFAULT_UI_LANGUAGE])
