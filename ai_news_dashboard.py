import streamlit as st
import feedparser
from datetime import datetime
from urllib.parse import quote

# ページ設定
st.set_page_config(
    page_title="ガンバ大阪ニュースダッシュボード",
    page_icon="⚽",
    layout="wide"
)

# ガンバ大阪公式サイト風カスタムCSS（クール＆モダン）
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap');
    
    * {
        font-family: 'Noto Sans JP', sans-serif;
    }
    
    .main {
        background: #0a0a0a;
    }
    
    .stApp {
        background: #0a0a0a;
    }
    
    /* サイドバースタイル */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
        border-right: 1px solid #21262d;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #c9d1d9;
    }
    
    /* ニュースカード - クリック可能なリンク */
    .news-card-link {
        display: block;
        text-decoration: none;
        color: inherit;
        transition: all 0.3s ease;
    }
    
    .news-card {
        background: #161b22;
        border-radius: 8px;
        padding: 24px;
        margin: 12px 0;
        border: 1px solid #21262d;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
    }
    
    .news-card-link:hover .news-card {
        background: #1c2128;
        border-color: #0066cc;
        transform: translateX(4px);
    }
    
    .news-card-link:hover .news-title {
        color: #58a6ff;
    }
    
    .news-title {
        color: #ffffff;
        font-size: 1.1em;
        font-weight: 700;
        margin-bottom: 10px;
        line-height: 1.5;
        transition: color 0.3s ease;
    }
    
    .news-date {
        color: #8b949e;
        font-size: 0.8em;
        margin-bottom: 12px;
        font-weight: 500;
    }
    
    .news-summary {
        color: #c9d1d9;
        font-size: 0.9em;
        line-height: 1.6;
        margin-bottom: 14px;
    }
    
    .read-indicator {
        color: #0066cc;
        font-size: 0.85em;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .news-card-link:hover .read-indicator {
        color: #58a6ff;
        transform: translateX(4px);
    }
    
    /* ソースバッジ */
    .source-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 4px;
        font-size: 0.7em;
        font-weight: 600;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .source-google {
        background: #0066cc;
        color: #ffffff;
    }
    
    .source-x {
        background: #21262d;
        color: #ffffff;
        border: 1px solid #30363d;
    }
    
    /* ヘッダー */
    .header-container {
        text-align: center;
        padding: 48px 20px 32px;
        margin-bottom: 16px;
        background: linear-gradient(180deg, #0d1117 0%, #0a0a0a 100%);
        border-bottom: 1px solid #21262d;
    }
    
    .main-title {
        color: #ffffff;
        font-size: 2em;
        font-weight: 900;
        margin-bottom: 8px;
        letter-spacing: 0.02em;
    }
    
    .title-blue {
        color: #0066cc;
    }
    
    .title-icon {
        color: #D4AF37;
        margin-right: 8px;
        text-shadow: 0 0 20px rgba(212, 175, 55, 0.5);
    }
    
    .subtitle {
        color: #8b949e;
        font-size: 0.9em;
        font-weight: 400;
    }
    
    /* ニュース件数 */
    .news-count {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 6px;
        padding: 12px 20px;
        margin: 16px 0 24px 0;
        color: #c9d1d9;
        font-weight: 500;
        text-align: center;
        font-size: 0.9em;
    }
    
    .news-count strong {
        color: #0066cc;
    }
    
    /* スクロールバー */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0d1117;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #30363d;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #484f58;
    }
    
    /* サイドバーのスタイル調整 */
    .sidebar-title {
        color: #ffffff;
        font-size: 0.85em;
        font-weight: 700;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .sidebar-info {
        background: #21262d;
        border-radius: 6px;
        padding: 14px;
        color: #8b949e;
        font-size: 0.8em;
        line-height: 1.6;
    }
    
    /* ボタンスタイル */
    .stButton > button {
        background: #0066cc;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85em;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #0077ee;
        transform: translateY(-1px);
    }
    
    /* セクションヘッダー */
    .section-header {
        color: #ffffff;
        font-size: 0.9em;
        font-weight: 700;
        margin: 32px 0 16px 0;
        padding: 12px 16px;
        background: #161b22;
        border-left: 3px solid #0066cc;
        border-radius: 0 6px 6px 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* メイン検索ボックス */
    .main-search-container {
        max-width: 500px;
        margin: 0 auto 8px auto;
    }
    
    .main-search-container input {
        background: #0d1117 !important;
        border: 1px solid #30363d !important;
        border-radius: 6px !important;
        padding: 12px 16px !important;
        color: #c9d1d9 !important;
        font-size: 1em !important;
    }
    
    .main-search-container input:focus {
        border-color: #0066cc !important;
        box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.2) !important;
    }
    
    .main-search-container input::placeholder {
        color: #6e7681 !important;
    }
    
    /* 検索ラベル */
    .search-label {
        text-align: center;
        margin-bottom: 12px;
    }
    
    .search-label-text {
        color: #8b949e;
        font-size: 0.9em;
        font-weight: 500;
    }
    
    .search-icon {
        color: #D4AF37;
        font-size: 1.2em;
        margin-right: 8px;
    }
    
    /* チェックボックススタイル */
    .stCheckbox label {
        color: #c9d1d9 !important;
    }
</style>
""", unsafe_allow_html=True)

def fetch_google_news(query):
    """Google NewsのRSSフィードからニュースを取得"""
    encoded_query = quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    feed = feedparser.parse(rss_url)
    return feed.entries

def fetch_x_posts(query):
    """X（Twitter）の投稿を検索（Google News経由）- ガンバ関連のみ"""
    # ガンバ大阪関連キーワードを含む検索
    gamba_keywords = ["ガンバ", "gamba", "G大阪", "パナスタ", "吹田スタジアム"]
    search_query = f'"{query}" (site:twitter.com OR site:x.com)'
    encoded_query = quote(search_query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    feed = feedparser.parse(rss_url)
    
    # ガンバ関連のエントリーのみをフィルタリング
    filtered_entries = []
    for entry in feed.entries:
        title = entry.get('title', '').lower()
        summary = entry.get('summary', '').lower()
        content = title + summary
        # ガンバ関連キーワードが含まれているかチェック
        if any(keyword.lower() in content for keyword in gamba_keywords):
            filtered_entries.append(entry)
    
    return filtered_entries

def format_date(date_string):
    """日付を日本語形式にフォーマット"""
    try:
        dt = datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %Z")
        return dt.strftime("%Y.%m.%d %H:%M")
    except:
        return date_string

def main():
    # ヘッダー
    st.markdown("""
    <div class="header-container">
        <h1 class="main-title">
            <span class="title-icon">★</span>
            <span class="title-blue">GAMBA OSAKA</span> NEWS
        </h1>
        <p class="subtitle">ガンバ大阪の最新情報をリアルタイムでお届け</p>
    </div>
    """, unsafe_allow_html=True)
    
    # メイン検索ボックス
    st.markdown("""
    <div class="search-label">
        <span class="search-icon">🔍</span>
        <span class="search-label-text">検索する文字を入力してください</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="main-search-container">', unsafe_allow_html=True)
    search_query = st.text_input(
        "検索キーワード",
        value="ガンバ大阪",
        help="検索したいキーワードを入力してください",
        label_visibility="collapsed",
        placeholder="例: ガンバ大阪、宇佐美貴史、パナスタ...",
        key="main_search"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # サイドバー
    with st.sidebar:
        # ソース選択
        st.markdown('<div class="sidebar-title">📰 NEWS SOURCE</div>', unsafe_allow_html=True)
        show_google = st.checkbox("Google News", value=True)
        show_x = st.checkbox("X（Twitter）", value=True)
        
        st.markdown("---")
        
        if st.button("🔄 更新", use_container_width=True):
            st.rerun()
        
        st.markdown("---")
        
        st.markdown("""
        <div class="sidebar-info">
            <strong>GUIDE</strong><br><br>
            検索ボックスにキーワードを入力すると、関連ニュースを自動取得します。<br><br>
            カードをクリックで元記事へ移動。
        </div>
        """, unsafe_allow_html=True)
    
    # ニュース取得
    google_entries = []
    x_entries = []
    
    with st.spinner("Loading..."):
        if show_google:
            google_entries = fetch_google_news(search_query)
        if show_x:
            x_entries = fetch_x_posts(search_query)
    
    total_count = len(google_entries) + len(x_entries)
    
    # ニュース件数表示
    st.markdown(f"""
    <div class="news-count">
        <strong>{total_count}</strong> 件のニュースを取得
        （Google News: {len(google_entries)} / X: {len(x_entries)}）
    </div>
    """, unsafe_allow_html=True)
    
    import re
    
    # 2カラムレイアウトで横並び表示
    col1, col2 = st.columns(2)
    
    # 左カラム: Google News
    with col1:
        if show_google:
            st.markdown('<div class="section-header">📰 GOOGLE NEWS</div>', unsafe_allow_html=True)
            if google_entries:
                for entry in google_entries[:10]:
                    title = entry.get('title', 'タイトルなし')
                    link = entry.get('link', '#')
                    published = entry.get('published', '日付不明')
                    summary = entry.get('summary', '要約がありません')
                    summary_clean = re.sub('<[^<]+?>', '', summary)
                    
                    st.markdown(f"""
                    <a href="{link}" target="_blank" class="news-card-link">
                        <div class="news-card">
                            <span class="source-badge source-google">Google News</span>
                            <div class="news-title">{title}</div>
                            <div class="news-date">{format_date(published)}</div>
                            <div class="news-summary">{summary_clean[:120]}...</div>
                            <div class="read-indicator">続きを読む →</div>
                        </div>
                    </a>
                    """, unsafe_allow_html=True)
            else:
                st.info("ニュースが見つかりませんでした")
    
    # 右カラム: X（Twitter）
    with col2:
        if show_x:
            st.markdown('<div class="section-header">𝕏 X / TWITTER</div>', unsafe_allow_html=True)
            if x_entries:
                for entry in x_entries[:10]:
                    title = entry.get('title', 'タイトルなし')
                    link = entry.get('link', '#')
                    published = entry.get('published', '日付不明')
                    summary = entry.get('summary', '要約がありません')
                    summary_clean = re.sub('<[^<]+?>', '', summary)
                    
                    st.markdown(f"""
                    <a href="{link}" target="_blank" class="news-card-link">
                        <div class="news-card">
                            <span class="source-badge source-x">𝕏</span>
                            <div class="news-title">{title}</div>
                            <div class="news-date">{format_date(published)}</div>
                            <div class="news-summary">{summary_clean[:120]}...</div>
                            <div class="read-indicator">投稿を見る →</div>
                        </div>
                    </a>
                    """, unsafe_allow_html=True)
            else:
                st.info("投稿が見つかりませんでした")
    
    if total_count == 0:
        st.warning("ニュースが見つかりませんでした。別のキーワードをお試しください。")

if __name__ == "__main__":
    main()
