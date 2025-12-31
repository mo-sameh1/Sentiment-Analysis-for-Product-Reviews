"""
Reusable chart components for the dashboard.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional


def render_score_distribution(df: pd.DataFrame, title: str = "Score Distribution"):
    if "Score" not in df.columns:
        st.warning("No 'Score' column found in data.")
        return
    
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = sns.color_palette("RdYlGn", 5)
    sns.countplot(x="Score", data=df, ax=ax, palette=colors, hue="Score", legend=False)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel("Rating Score", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', fontsize=10)
    
    st.pyplot(fig)
    plt.close(fig)


def render_sentiment_pie(df: pd.DataFrame):
    if "Score" not in df.columns:
        return
    
    sentiment_counts = df["Score"].apply(
        lambda x: "Positive" if x >= 4 else ("Negative" if x <= 2 else "Neutral")
    ).value_counts()
    
    fig, ax = plt.subplots(figsize=(8, 8))
    colors = {"Positive": "#2ecc71", "Negative": "#e74c3c", "Neutral": "#f39c12"}
    pie_colors = [colors.get(label, "#95a5a6") for label in sentiment_counts.index]
    
    wedges, texts, autotexts = ax.pie(
        sentiment_counts.values,
        labels=sentiment_counts.index,
        autopct='%1.1f%%',
        colors=pie_colors,
        explode=[0.02] * len(sentiment_counts),
        shadow=True,
        startangle=90
    )
    
    for autotext in autotexts:
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')
    
    ax.set_title("Sentiment Distribution", fontsize=14, fontweight="bold")
    st.pyplot(fig)
    plt.close(fig)


def render_wordcloud(df: pd.DataFrame, column: str = "Text", max_words: int = 100):
    from wordcloud import WordCloud
    
    if column not in df.columns:
        st.warning(f"Column '{column}' not found.")
        return
    
    text = " ".join(df[column].dropna().astype(str))
    
    if not text.strip():
        st.warning("No text data available for word cloud.")
        return
    
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white",
        max_words=max_words,
        colormap="viridis",
        contour_width=2,
        contour_color="steelblue"
    ).generate(text)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    ax.set_title("Most Frequent Words", fontsize=14, fontweight="bold", pad=20)
    st.pyplot(fig)
    plt.close(fig)


def render_review_length_distribution(df: pd.DataFrame, column: str = "Text"):
    if column not in df.columns:
        return
    
    df_copy = df.copy()
    df_copy["text_length"] = df_copy[column].astype(str).apply(len)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df_copy["text_length"], bins=50, ax=ax, color="steelblue", edgecolor="white")
    ax.set_title("Review Length Distribution", fontsize=14, fontweight="bold")
    ax.set_xlabel("Character Count", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    st.pyplot(fig)
    plt.close(fig)


def render_helpfulness_analysis(df: pd.DataFrame):
    if "HelpfulnessNumerator" not in df.columns or "HelpfulnessDenominator" not in df.columns:
        return
    
    df_copy = df.copy()
    df_copy = df_copy[df_copy["HelpfulnessDenominator"] > 0].copy()
    df_copy["helpfulness_ratio"] = df_copy["HelpfulnessNumerator"] / df_copy["HelpfulnessDenominator"]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(x="Score", y="helpfulness_ratio", data=df_copy, ax=ax, palette="RdYlGn", hue="Score", legend=False)
    ax.set_title("Helpfulness Ratio by Score", fontsize=14, fontweight="bold")
    ax.set_xlabel("Rating Score", fontsize=12)
    ax.set_ylabel("Helpfulness Ratio", fontsize=12)
    st.pyplot(fig)
    plt.close(fig)
