import streamlit as st

from src.review_intelligence import analyze_review


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Hotel Review Intelligence",
    page_icon="🏨",
    layout="wide"
)


# ---------------------------------------------------------
# MULTILINGUAL INTERFACE
# ---------------------------------------------------------

TRANSLATIONS = {

    "English": {
        "title": "Hotel Review Intelligence",
        "subtitle": "AI-powered guest sentiment and complaint intelligence for hotel management.",
        "language": "Interface Language",
        "model_note": (
            "The current sentiment model was trained on English hotel reviews. "
            "For reliable predictions, enter the guest review in English."
        ),
        "review_label": "Enter Guest Review",
        "placeholder": (
            "Example: The bathroom was dirty and the staff were very rude..."
        ),
        "analyze": "Analyze Review",
        "results": "Analysis Results",
        "sentiment": "Sentiment",
        "confidence": "Confidence",
        "category": "Complaint Category",
        "department": "Responsible Department",
        "priority": "Priority",
        "action": "Recommended Management Action",
        "empty": "Please enter a guest review before analyzing."
    },

    "Français": {
        "title": "Intelligence des Avis Hôteliers",
        "subtitle": "Analyse intelligente du sentiment et des plaintes clients pour la gestion hôtelière.",
        "language": "Langue de l’interface",
        "model_note": (
            "Le modèle actuel a été entraîné sur des avis hôteliers en anglais. "
            "Pour une prédiction fiable, saisissez l’avis du client en anglais."
        ),
        "review_label": "Saisir l'avis du client",
        "placeholder": (
            "Exemple : The bathroom was dirty and the staff were very rude..."
        ),
        "analyze": "Analyser l'avis",
        "results": "Résultats de l'analyse",
        "sentiment": "Sentiment",
        "confidence": "Confiance",
        "category": "Catégorie de plainte",
        "department": "Département responsable",
        "priority": "Priorité",
        "action": "Action recommandée",
        "empty": "Veuillez saisir un avis avant de lancer l'analyse."
    },

    "Türkçe": {
        "title": "Otel Yorum Zekâsı",
        "subtitle": "Otel yönetimi için yapay zekâ destekli misafir duygu ve şikâyet analizi.",
        "language": "Arayüz Dili",
        "model_note": (
            "Mevcut duygu analizi modeli İngilizce otel yorumlarıyla eğitilmiştir. "
            "Güvenilir sonuçlar için yorumu İngilizce girin."
        ),
        "review_label": "Misafir Yorumunu Girin",
        "placeholder": (
            "Örnek: The bathroom was dirty and the staff were very rude..."
        ),
        "analyze": "Yorumu Analiz Et",
        "results": "Analiz Sonuçları",
        "sentiment": "Duygu",
        "confidence": "Güven",
        "category": "Şikâyet Kategorisi",
        "department": "Sorumlu Departman",
        "priority": "Öncelik",
        "action": "Önerilen Yönetim Aksiyonu",
        "empty": "Analiz etmeden önce bir misafir yorumu girin."
    },

    "Русский": {
        "title": "Аналитика Отзывов Отеля",
        "subtitle": "Интеллектуальный анализ отзывов, настроений и жалоб гостей для управления отелем.",
        "language": "Язык интерфейса",
        "model_note": (
            "Текущая модель обучена на англоязычных отзывах об отелях. "
            "Для надежного результата вводите отзыв на английском языке."
        ),
        "review_label": "Введите отзыв гостя",
        "placeholder": (
            "Пример: The bathroom was dirty and the staff were very rude..."
        ),
        "analyze": "Анализировать отзыв",
        "results": "Результаты анализа",
        "sentiment": "Тональность",
        "confidence": "Уверенность",
        "category": "Категория жалобы",
        "department": "Ответственный отдел",
        "priority": "Приоритет",
        "action": "Рекомендуемое действие",
        "empty": "Введите отзыв гостя перед анализом."
    }
}


# ---------------------------------------------------------
# TRANSLATE MODEL OUTPUT VALUES
# ---------------------------------------------------------

SENTIMENT_TRANSLATIONS = {

    "English": {
        "Positive": "Positive",
        "Neutral": "Neutral",
        "Negative": "Negative"
    },

    "Français": {
        "Positive": "Positif",
        "Neutral": "Neutre",
        "Negative": "Négatif"
    },

    "Türkçe": {
        "Positive": "Olumlu",
        "Neutral": "Nötr",
        "Negative": "Olumsuz"
    },

    "Русский": {
        "Positive": "Положительный",
        "Neutral": "Нейтральный",
        "Negative": "Отрицательный"
    }
}


PRIORITY_TRANSLATIONS = {

    "English": {
        "High": "High",
        "Medium": "Medium",
        "Low": "Low"
    },

    "Français": {
        "High": "Élevée",
        "Medium": "Moyenne",
        "Low": "Faible"
    },

    "Türkçe": {
        "High": "Yüksek",
        "Medium": "Orta",
        "Low": "Düşük"
    },

    "Русский": {
        "High": "Высокий",
        "Medium": "Средний",
        "Low": "Низкий"
    }
}


# ---------------------------------------------------------
# SIMPLE PROFESSIONAL STYLING
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        opacity: 0.75;
        margin-bottom: 25px;
    }

    .result-box {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-top: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# LANGUAGE SELECTION
# ---------------------------------------------------------

language = st.selectbox(
    "Language / Langue / Dil / Язык",
    ["English", "Français", "Türkçe", "Русский"]
)

t = TRANSLATIONS[language]


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    f'<div class="main-title">🏨 {t["title"]}</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="subtitle">{t["subtitle"]}</div>',
    unsafe_allow_html=True
)

st.info(t["model_note"])


# ---------------------------------------------------------
# REVIEW INPUT
# ---------------------------------------------------------

review = st.text_area(
    t["review_label"],
    placeholder=t["placeholder"],
    height=180
)


# ---------------------------------------------------------
# ANALYSIS BUTTON
# ---------------------------------------------------------

if st.button(
    t["analyze"],
    type="primary",
    use_container_width=True
):

    if not review.strip():

        st.warning(t["empty"])

    else:

        with st.spinner("Analyzing..."):

            result = analyze_review(review)


        # -------------------------------------------------
        # RESULTS
        # -------------------------------------------------

        st.subheader(t["results"])

        col1, col2, col3 = st.columns(3)

        sentiment_display = SENTIMENT_TRANSLATIONS[
            language
        ].get(
            result["sentiment"],
            result["sentiment"]
        )

        priority_display = PRIORITY_TRANSLATIONS[
            language
        ].get(
            result["priority"],
            result["priority"]
        )


        with col1:

            st.metric(
                t["sentiment"],
                sentiment_display
            )


        with col2:

            st.metric(
                t["confidence"],
                f'{result["confidence"]}%'
            )


        with col3:

            st.metric(
                t["priority"],
                priority_display
            )


        st.divider()


        col4, col5 = st.columns(2)


        with col4:

            st.markdown(
                f"### {t['category']}"
            )

            st.write(
                result["complaint_category"]
            )


        with col5:

            st.markdown(
                f"### {t['department']}"
            )

            st.write(
                result["department"]
            )


        st.markdown(
            f"### {t['action']}"
        )

        st.success(
            result["recommended_action"]
        )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "Hotel Review Intelligence | "
    "Python • NLP • TF-IDF • Logistic Regression • Streamlit"
)
