import streamlit as st
import subprocess
import platform
import re

# --- ページ設定 ---
st.set_page_config(page_title="ネットワーク経路調査ツール", layout="centered")

# --- カスタムCSS ---
st.markdown("""
    <style>
    .credit { text-align: right; font-size: 14px; color: #666; margin-bottom: -20px; }
    .stTextInput label { font-size: 20px !important; color: #1E90FF !important; font-weight: bold !important; }
    .console-box {
        background-color: #000;
        color: #0f0;
        padding: 15px;
        border-radius: 5px;
        font-family: 'Courier New', Courier, monospace;
        white-space: pre-wrap;
        min-height: 200px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="credit">開発/制作：緒方</p>', unsafe_allow_html=True)
st.title("🌐 ネットワーク経路調査 (Traceroute)")
st.write("指定したホストへの通信経路を確認します。")
st.markdown("---")

# --- 入力セクション ---
target_host = st.text_input("調査対象のホスト名またはIPアドレス", value="google.com", help="例: google.com や 8.8.8.8")

# --- 実行ボタン ---
if st.button("トレース実行", use_container_width=True):
    if not target_host:
        st.error("ホスト名を入力してください。")
    else:
        # OSを判定してコマンドを使い分け
        os_type = platform.system()
        # Windowsは「tracert」、Linux/Macは「traceroute」
        command = ["tracert", "-d", target_host] if os_type == "Windows" else ["traceroute", "-n", target_host]
        
        st.info(f"経路を調査中... (完了まで時間がかかる場合があります)")
        
        # 実行中の出力をリアルタイムに表示するためのプレースホルダー
        output_area = st.empty()
        full_output = ""

        try:
            # サブプロセスを実行
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                shell=(os_type == "Windows")
            )

            # 出力を1行ずつ読み取って表示を更新
            for line in process.stdout:
                full_output += line
                output_area.markdown(f'<div class="console-box">{full_output}</div>', unsafe_allow_html=True)
            
            process.wait()
            st.success("調査が完了しました。")

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

st.markdown("---")
st.caption("💡 ヒント: `-d` (Windows) または `-n` (Linux) オプションを使用し、逆引きを行わずに速度を優先しています。")

# --- 画面下部中央に「戻る」ボタンを配置 ---
st.markdown("---")  # 区切り線
col1, col2, col3 = st.columns([1, 1, 1])

with col2:  # 中央の列を使用
    # 水色のアイコン（🏠）と「戻る」を表示するボタン
    if st.link_button("🏠\n\n戻る", "https://menue3-pkwzfkwnoxnnuljkqg7mdt.streamlit.app/", use_container_width=True):
        pass

# ボタンの色（水色）を調整するカスタム設定
st.markdown("""
    <style>
    div.stLinkButton > a {
        background-color: #00BFFF !important; /* 水色（DeepSkyBlue） */
        color: white !important;
        border-radius: 10px;
        text-align: center;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)
