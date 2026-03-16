"""UI国際化（i18n）- 日本語 / English / 中文 対応."""

import locale
import os


def detect_language() -> str:
    """システム言語を検出し、'ja'、'zh'、'en' のいずれかを返す。フォールバックは 'ja'。

    環境変数 LANGUAGE / LANG / LC_ALL / LC_MESSAGES を優先して参照し、
    取得できない場合は Python の locale モジュールにフォールバックする。
    """
    for env_var in ("LANGUAGE", "LANG", "LC_ALL", "LC_MESSAGES"):
        val = os.environ.get(env_var, "")
        if val:
            # LANGUAGE は複数ロケールをコロン区切りで持つことがある。先頭を使用。
            code = val.split(":")[0].split(".")[0].lower()
            if code.startswith("ja"):
                return "ja"
            if code.startswith("zh"):
                return "zh"
            if code.startswith("en"):
                return "en"
    try:
        lang_code, _ = locale.getdefaultlocale()
        if lang_code:
            code = lang_code.lower()
            if code.startswith("ja"):
                return "ja"
            if code.startswith("zh"):
                return "zh"
            if code.startswith("en"):
                return "en"
    except Exception:
        pass
    return "ja"


# システム言語 → デフォルトのTTS出力言語インデックス
# （engine.py の SUPPORTED_LANGUAGES リストの順序に対応）
# ["Japanese", "Chinese", "English", "Korean", ...]
DEFAULT_TTS_LANGUAGE_INDEX: dict[str, int] = {
    "ja": 0,  # Japanese
    "zh": 1,  # Chinese
    "en": 2,  # English
}

TRANSLATIONS: dict[str, dict[str, str]] = {
    # =========================================================================
    # 日本語
    # =========================================================================
    "ja": {
        # サイドバー
        "device_label": "デバイス: {info}",
        "model_size_label": "モデルサイズ",
        "model_size_help": "1.7B（デフォルト）は高品質、0.6Bは軽量版です。",
        "select_mode": "モード選択",
        "mode_voice_learning": "オリジナルボイスモデル学習",
        "mode_tts": "音声合成",
        "mode_instant_tts": "オリジナル音声即時合成",
        "mode_web_api": "音声合成WebAPI",
        "gen_params": "生成パラメータ設定",
        "temperature": "温度（感情値）",
        "temperature_help": "感情の豊かさを制御します。高いほど表現豊かでランダムな発音、低いほど落ち着いた安定した発音になります。",
        "top_p": "Top-p（核サンプリング）",
        "top_p_help": "累積確率が上位p以内のトークンのみからサンプリングします。低いほど安定した出力になります。",
        "top_k": "Top-k",
        "top_k_help": "確率の高い上位k件のトークンのみからサンプリングします。低いほど安定した出力になります。",
        "repetition_penalty": "繰り返し抑制（Repetition Penalty）",
        "repetition_penalty_help": "同じ音やフレーズの繰り返しを抑制します。高いほど繰り返しが起きにくくなります。",
        "clear_chat": "チャット履歴クリア",
        # 音声バリデーション
        "err_audio_load": "音声ファイルの読み込みに失敗しました: {e}",
        "err_duration": (
            "音声の長さが {duration:.1f} 秒です。"
            "音声学習には {min:.0f}秒〜{max:.0f}秒の音声を使用してください。"
        ),
        # 完了通知
        "done": "完了しました！",
        # モード1: ボイスモデル学習
        "mode1_header": "オリジナルボイスモデル学習",
        "mode1_desc": "リファレンス音声からオリジナルボイスモデルを作成します。",
        "new_model": "新規モデル作成",
        "ref_audio_file": "リファレンス音声ファイル",
        "ref_audio_help": "3秒以上の音声ファイルを推奨します。",
        "ref_transcript": "音声の文字起こし",
        "ref_transcript_placeholder": "アップロードした音声の内容をテキストで入力してください",
        "ref_lang": "リファレンス音声の言語",
        "nickname": "ニックネーム",
        "nickname_placeholder": "ボイスモデルの名前を入力",
        "create_model": "モデル作成",
        "greeting_preview": "挨拶プレビュー",
        "err_fill_all": "音声ファイル、文字起こし、ニックネームをすべて入力してください。",
        "creating_model": "ボイスモデルを作成中...",
        "model_created": "ボイスモデル '{nickname}' を作成しました。",
        "model_created_toast": "ボイスモデル作成完了",
        "err_fill_audio_text": "音声ファイルと文字起こしを入力してください。",
        "generating_greeting": "挨拶音声を生成中（{lang}）...",
        "greeting_label": "挨拶: {greeting}",
        "preview_done": "プレビュー完了",
        "saved_models": "保存済みモデル",
        "no_saved_models": "保存されたボイスモデルはありません（{model_size}）。",
        "voice_caption": "言語: {lang} | サイズ: {size} | 作成日: {date}",
        "export": "エクスポート",
        "delete": "削除",
        "model_import": "モデルインポート",
        "import_file_label": "ボイスモデルファイル (.pt) - {model_size}向けのみ",
        "import_name": "インポート名",
        "import_lang": "言語",
        "import_btn": "インポート",
        "import_success": "'{nickname}' をインポートしました。",
        "import_fail": "インポート失敗: {err}",
        "err_fill_file_name": "ファイルとインポート名を入力してください。",
        # モード2: 音声合成
        "mode2_header": "音声合成",
        "voice_source": "ボイスモデルソース",
        "saved_model_option": "保存済みモデル",
        "file_upload_option": "ファイルアップロード",
        "output_lang": "出力言語",
        "voice_model": "ボイスモデル",
        "no_saved_model_warning": (
            "保存されたボイスモデルがありません（{model_size}）。"
            "「{mode}」モードで先にモデルを作成してください。"
        ),
        "upload_model_file": "ボイスモデルファイル (.pt)",
        "chat_input_tts": "合成するテキストを入力してください",
        "err_select_model": "ボイスモデルを選択またはアップロードしてください。",
        "generating_audio": "音声を生成中...",
        "audio_generated": "音声を生成しました",
        "audio_generated_toast": "音声合成完了",
        # モード3: 即時合成
        "mode3_header": "オリジナル音声即時合成",
        "mode3_desc": "リファレンス音声から直接音声合成を行います。ボイスモデルはキャッシュされません。",
        "ref_settings": "リファレンス設定",
        "ref_audio": "リファレンス音声",
        "transcript": "文字起こし",
        "transcript_placeholder": "リファレンス音声の内容",
        "ref_lang_label": "リファレンス言語",
        "output_settings": "出力設定",
        "chat_input_instant": "合成するテキストを入力",
        "err_fill_ref": "リファレンス音声と文字起こしを入力してください。",
        "generating_with_ref": "リファレンス音声を解析して音声を生成中...",
        # モード4: WebAPI
        "mode4_header": "音声合成WebAPI",
        "mode4_desc": (
            "VOICEVOX互換のHTTP APIサーバーとして利用できます。\n"
            "以下のコマンドでAPIサーバーを起動し、他のアプリケーションから音声合成を呼び出せます。"
        ),
        "start_cmd": "サーバー起動コマンド",
        "default_host": "デフォルト: host=127.0.0.1, port=50021",
        "network_example": "ネットワーク公開の例",
        "model_info": "モデルは常に **1.7B** を使用します。ボイスモデルはこのWebUIで学習・保存済みのものを使用します。",
        "main_endpoints": "主要APIエンドポイント（VOICEVOX互換）",
        "version_endpoint": "GET /version - バージョン取得",
        "speakers_endpoint": "GET /speakers - 話者（ボイスモデル）一覧",
        "speakers_caption": (
            "保存済みボイスモデルが話者として返されます。"
            "speaker_id は /voice_models で確認できます。"
        ),
        "synthesis_endpoint": "POST /audio_query + POST /synthesis - 音声合成（2ステップ）",
        "step1": "**ステップ1: AudioQueryを作成**",
        "step2": "**ステップ2: 音声合成**",
        "ext_endpoints": "拡張APIエンドポイント",
        "voice_models_endpoint": "GET /voice_models - ボイスモデル一覧（拡張）",
        "api_docs": "APIドキュメント",
        "api_docs_desc": (
            "サーバー起動後、以下のURLでインタラクティブなAPIドキュメントを参照できます:\n\n"
            "- **Swagger UI**: http://127.0.0.1:50021/docs\n"
            "- **ReDoc**: http://127.0.0.1:50021/redoc"
        ),
        "python_sample": "Pythonサンプルコード",
        "py_step1_comment": "# ステップ1: AudioQueryを作成",
        "py_step2_comment": "# ステップ2: 音声合成",
        "py_save_comment": "# WAVファイルとして保存",
    },
    # =========================================================================
    # English
    # =========================================================================
    "en": {
        # Sidebar
        "device_label": "Device: {info}",
        "model_size_label": "Model Size",
        "model_size_help": "1.7B (default) is high quality; 0.6B is a lightweight version.",
        "select_mode": "Select Mode",
        "mode_voice_learning": "Voice Model Training",
        "mode_tts": "Voice Synthesis",
        "mode_instant_tts": "Instant Voice Synthesis",
        "mode_web_api": "Voice Synthesis Web API",
        "gen_params": "Generation Parameters",
        "temperature": "Temperature (Emotion)",
        "temperature_help": (
            "Controls expressiveness. Higher values produce more expressive and varied speech; "
            "lower values produce calm and stable speech."
        ),
        "top_p": "Top-p (Nucleus Sampling)",
        "top_p_help": (
            "Samples only from tokens within the top-p cumulative probability. "
            "Lower values produce more stable output."
        ),
        "top_k": "Top-k",
        "top_k_help": (
            "Samples only from the top-k highest-probability tokens. "
            "Lower values produce more stable output."
        ),
        "repetition_penalty": "Repetition Penalty",
        "repetition_penalty_help": (
            "Suppresses repetition of the same sounds or phrases. "
            "Higher values reduce repetition."
        ),
        "clear_chat": "Clear Chat History",
        # Audio validation
        "err_audio_load": "Failed to load audio file: {e}",
        "err_duration": (
            "Audio length is {duration:.1f} seconds. "
            "Please use audio between {min:.0f} and {max:.0f} seconds for training."
        ),
        # Completion notification
        "done": "Done!",
        # Mode 1: Voice model training
        "mode1_header": "Voice Model Training",
        "mode1_desc": "Create an original voice model from a reference audio.",
        "new_model": "Create New Model",
        "ref_audio_file": "Reference Audio File",
        "ref_audio_help": "An audio file of 3 seconds or more is recommended.",
        "ref_transcript": "Audio Transcript",
        "ref_transcript_placeholder": "Enter the content of the uploaded audio as text",
        "ref_lang": "Reference Audio Language",
        "nickname": "Nickname",
        "nickname_placeholder": "Enter voice model name",
        "create_model": "Create Model",
        "greeting_preview": "Greeting Preview",
        "err_fill_all": "Please fill in the audio file, transcript, and nickname.",
        "creating_model": "Creating voice model...",
        "model_created": "Voice model '{nickname}' has been created.",
        "model_created_toast": "Voice model created",
        "err_fill_audio_text": "Please provide the audio file and transcript.",
        "generating_greeting": "Generating greeting audio ({lang})...",
        "greeting_label": "Greeting: {greeting}",
        "preview_done": "Preview complete",
        "saved_models": "Saved Models",
        "no_saved_models": "No saved voice models ({model_size}).",
        "voice_caption": "Language: {lang} | Size: {size} | Created: {date}",
        "export": "Export",
        "delete": "Delete",
        "model_import": "Import Model",
        "import_file_label": "Voice model file (.pt) - for {model_size} only",
        "import_name": "Import Name",
        "import_lang": "Language",
        "import_btn": "Import",
        "import_success": "'{nickname}' imported successfully.",
        "import_fail": "Import failed: {err}",
        "err_fill_file_name": "Please provide the file and import name.",
        # Mode 2: Voice synthesis
        "mode2_header": "Voice Synthesis",
        "voice_source": "Voice Model Source",
        "saved_model_option": "Saved Model",
        "file_upload_option": "File Upload",
        "output_lang": "Output Language",
        "voice_model": "Voice Model",
        "no_saved_model_warning": (
            "No saved voice models ({model_size}). "
            "Please create a model first in '{mode}' mode."
        ),
        "upload_model_file": "Voice model file (.pt)",
        "chat_input_tts": "Enter text to synthesize",
        "err_select_model": "Please select or upload a voice model.",
        "generating_audio": "Generating audio...",
        "audio_generated": "Audio generated",
        "audio_generated_toast": "Audio synthesis complete",
        # Mode 3: Instant synthesis
        "mode3_header": "Instant Voice Synthesis",
        "mode3_desc": (
            "Synthesize audio directly from reference audio. "
            "The voice model will not be cached."
        ),
        "ref_settings": "Reference Settings",
        "ref_audio": "Reference Audio",
        "transcript": "Transcript",
        "transcript_placeholder": "Content of reference audio",
        "ref_lang_label": "Reference Language",
        "output_settings": "Output Settings",
        "chat_input_instant": "Enter text to synthesize",
        "err_fill_ref": "Please provide reference audio and transcript.",
        "generating_with_ref": "Analyzing reference audio and generating speech...",
        # Mode 4: Web API
        "mode4_header": "Voice Synthesis Web API",
        "mode4_desc": (
            "Can be used as a VOICEVOX-compatible HTTP API server.\n"
            "Start the API server with the command below to call voice synthesis "
            "from other applications."
        ),
        "start_cmd": "Server Start Command",
        "default_host": "Default: host=127.0.0.1, port=50021",
        "network_example": "Example for network exposure",
        "model_info": (
            "The model always uses **1.7B**. "
            "Voice models use those trained and saved in this WebUI."
        ),
        "main_endpoints": "Main API Endpoints (VOICEVOX Compatible)",
        "version_endpoint": "GET /version - Get Version",
        "speakers_endpoint": "GET /speakers - Speaker (Voice Model) List",
        "speakers_caption": (
            "Saved voice models are returned as speakers. "
            "Check speaker_id at /voice_models."
        ),
        "synthesis_endpoint": (
            "POST /audio_query + POST /synthesis - Voice Synthesis (2 steps)"
        ),
        "step1": "**Step 1: Create AudioQuery**",
        "step2": "**Step 2: Voice Synthesis**",
        "ext_endpoints": "Extended API Endpoints",
        "voice_models_endpoint": "GET /voice_models - Voice Model List (Extended)",
        "api_docs": "API Documentation",
        "api_docs_desc": (
            "After starting the server, you can view interactive API documentation at:\n\n"
            "- **Swagger UI**: http://127.0.0.1:50021/docs\n"
            "- **ReDoc**: http://127.0.0.1:50021/redoc"
        ),
        "python_sample": "Python Sample Code",
        "py_step1_comment": "# Step 1: Create AudioQuery",
        "py_step2_comment": "# Step 2: Voice Synthesis",
        "py_save_comment": "# Save as WAV file",
    },
    # =========================================================================
    # 中文
    # =========================================================================
    "zh": {
        # 侧边栏
        "device_label": "设备：{info}",
        "model_size_label": "模型大小",
        "model_size_help": "1.7B（默认）为高质量版本，0.6B为轻量版本。",
        "select_mode": "选择模式",
        "mode_voice_learning": "声音模型训练",
        "mode_tts": "语音合成",
        "mode_instant_tts": "即时语音合成",
        "mode_web_api": "语音合成WebAPI",
        "gen_params": "生成参数设置",
        "temperature": "温度（情感值）",
        "temperature_help": "控制情感丰富度。值越高，语音越富有表现力且随机；值越低，语音越平稳安定。",
        "top_p": "Top-p（核采样）",
        "top_p_help": "仅从累积概率在前p以内的标记中采样。值越低，输出越稳定。",
        "top_k": "Top-k",
        "top_k_help": "仅从概率最高的前k个标记中采样。值越低，输出越稳定。",
        "repetition_penalty": "重复惩罚（Repetition Penalty）",
        "repetition_penalty_help": "抑制相同音节或短语的重复。值越高，重复越少。",
        "clear_chat": "清除聊天记录",
        # 音频验证
        "err_audio_load": "音频文件加载失败：{e}",
        "err_duration": (
            "音频长度为 {duration:.1f} 秒。"
            "请使用 {min:.0f} 秒至 {max:.0f} 秒的音频进行训练。"
        ),
        # 完成通知
        "done": "完成！",
        # 模式1：声音模型训练
        "mode1_header": "声音模型训练",
        "mode1_desc": "从参考音频创建原创声音模型。",
        "new_model": "创建新模型",
        "ref_audio_file": "参考音频文件",
        "ref_audio_help": "建议使用3秒以上的音频文件。",
        "ref_transcript": "音频转写",
        "ref_transcript_placeholder": "请输入上传音频的文字内容",
        "ref_lang": "参考音频语言",
        "nickname": "昵称",
        "nickname_placeholder": "输入声音模型名称",
        "create_model": "创建模型",
        "greeting_preview": "问候预览",
        "err_fill_all": "请填写音频文件、转写文本和昵称。",
        "creating_model": "正在创建声音模型...",
        "model_created": "声音模型 '{nickname}' 已创建。",
        "model_created_toast": "声音模型创建完成",
        "err_fill_audio_text": "请提供音频文件和转写文本。",
        "generating_greeting": "正在生成问候音频（{lang}）...",
        "greeting_label": "问候语：{greeting}",
        "preview_done": "预览完成",
        "saved_models": "已保存模型",
        "no_saved_models": "没有已保存的声音模型（{model_size}）。",
        "voice_caption": "语言：{lang} | 大小：{size} | 创建日期：{date}",
        "export": "导出",
        "delete": "删除",
        "model_import": "导入模型",
        "import_file_label": "声音模型文件 (.pt) - 仅适用于 {model_size}",
        "import_name": "导入名称",
        "import_lang": "语言",
        "import_btn": "导入",
        "import_success": "'{nickname}' 已成功导入。",
        "import_fail": "导入失败：{err}",
        "err_fill_file_name": "请提供文件和导入名称。",
        # 模式2：语音合成
        "mode2_header": "语音合成",
        "voice_source": "声音模型来源",
        "saved_model_option": "已保存模型",
        "file_upload_option": "文件上传",
        "output_lang": "输出语言",
        "voice_model": "声音模型",
        "no_saved_model_warning": (
            "没有已保存的声音模型（{model_size}）。"
            "请先在"{mode}"模式中创建模型。"
        ),
        "upload_model_file": "声音模型文件 (.pt)",
        "chat_input_tts": "请输入要合成的文字",
        "err_select_model": "请选择或上传声音模型。",
        "generating_audio": "正在生成音频...",
        "audio_generated": "音频已生成",
        "audio_generated_toast": "语音合成完成",
        # 模式3：即时合成
        "mode3_header": "即时语音合成",
        "mode3_desc": "直接从参考音频合成语音。声音模型不会被缓存。",
        "ref_settings": "参考设置",
        "ref_audio": "参考音频",
        "transcript": "转写文本",
        "transcript_placeholder": "参考音频的内容",
        "ref_lang_label": "参考语言",
        "output_settings": "输出设置",
        "chat_input_instant": "请输入要合成的文字",
        "err_fill_ref": "请提供参考音频和转写文本。",
        "generating_with_ref": "正在分析参考音频并生成语音...",
        # 模式4：WebAPI
        "mode4_header": "语音合成WebAPI",
        "mode4_desc": (
            "可作为VOICEVOX兼容的HTTP API服务器使用。\n"
            "使用以下命令启动API服务器，从其他应用程序调用语音合成。"
        ),
        "start_cmd": "服务器启动命令",
        "default_host": "默认：host=127.0.0.1, port=50021",
        "network_example": "网络公开示例",
        "model_info": "模型始终使用 **1.7B**。声音模型使用此WebUI中训练并保存的模型。",
        "main_endpoints": "主要API端点（VOICEVOX兼容）",
        "version_endpoint": "GET /version - 获取版本",
        "speakers_endpoint": "GET /speakers - 话者（声音模型）列表",
        "speakers_caption": (
            "已保存的声音模型将作为话者返回。"
            "可在 /voice_models 查看 speaker_id。"
        ),
        "synthesis_endpoint": "POST /audio_query + POST /synthesis - 语音合成（2步骤）",
        "step1": "**步骤1：创建 AudioQuery**",
        "step2": "**步骤2：语音合成**",
        "ext_endpoints": "扩展API端点",
        "voice_models_endpoint": "GET /voice_models - 声音模型列表（扩展）",
        "api_docs": "API文档",
        "api_docs_desc": (
            "服务器启动后，可通过以下URL查看交互式API文档：\n\n"
            "- **Swagger UI**: http://127.0.0.1:50021/docs\n"
            "- **ReDoc**: http://127.0.0.1:50021/redoc"
        ),
        "python_sample": "Python示例代码",
        "py_step1_comment": "# 步骤1：创建 AudioQuery",
        "py_step2_comment": "# 步骤2：语音合成",
        "py_save_comment": "# 保存为WAV文件",
    },
}
