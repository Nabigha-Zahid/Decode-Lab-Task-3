import streamlit as st
import re

from recommender import recommend_jobs


st.set_page_config(
    page_title="Tech Stack Recommender",
    page_icon="💼",
    layout="wide"
)


def get_display_skills(skill_text, user_skills, max_skills=8):

    if not isinstance(skill_text, str):
        return []

    stop_words = {
        "on", "in", "at", "of", "for", "to", "and", "or",
        "with", "the", "a", "an", "is", "are", "be",
        "experience", "knowledge", "skills", "skill",
        "working", "work", "good", "strong", "using",
        "based", "support", "development", "management"
    }

    words = re.findall(
        r"[A-Za-z][A-Za-z0-9+#.\-]*",
        skill_text
    )

    unique_words = []
    seen = set()

    for word in words:

        clean_word = word.strip()
        lower_word = clean_word.lower()

        if len(clean_word) < 3:
            continue

        if lower_word in stop_words:
            continue

        if lower_word not in seen:
            seen.add(lower_word)
            unique_words.append(clean_word)

    user_lower = [
        skill.lower()
        for skill in user_skills
    ]

    matching = []
    remaining = []

    for skill in unique_words:

        skill_lower = skill.lower()

        if any(
            user_skill in skill_lower
            or skill_lower in user_skill
            for user_skill in user_lower
        ):
            matching.append(skill)
        else:
            remaining.append(skill)

    final_skills = matching + remaining

    return final_skills[:max_skills]


# -----------------------------
# Header
# -----------------------------

st.title("Tech Stack Recommender")

st.caption(
    "Discover career roles that match your technical skills "
    "using TF-IDF and Cosine Similarity."
)

st.divider()


# -----------------------------
# User Input
# -----------------------------

st.subheader("Your Skills")

user_input = st.text_input(
    "Enter at least 3 skills separated by commas",
    placeholder="Python, Machine Learning, Data Analysis"
)

recommend_button = st.button(
    "Find Jobs",
    type="primary"
)


# -----------------------------
# Recommendations
# -----------------------------

if recommend_button:

    skills = [
        skill.strip()
        for skill in user_input.split(",")
        if skill.strip()
    ]

    if len(skills) < 3:

        st.error(
            "Please enter at least 3 skills."
        )

    else:

        with st.spinner(
            "Finding your best career matches..."
        ):

            recommendations = recommend_jobs(
                skills,
                top_n=3
            )

        st.success(
            "Recommendations generated successfully."
        )

        st.subheader(
            "Top Career Matches"
        )

        for rank, (_, row) in enumerate(
            recommendations.iterrows(),
            start=1
        ):

            score = (
                float(row["Similarity Score"])
                * 100
            )

            display_skills = get_display_skills(
                row["Key Skills"],
                skills,
                max_skills=8
            )

            with st.container(border=True):

                left, right = st.columns(
                    [4, 1]
                )

                with left:

                    st.markdown(
                        f"### {rank}. {row['Job Title']}"
                    )

                    category = str(
                        row.get("Role Category", "")
                    )

                    if category and category != "nan":
                        st.caption(category)

                with right:

                    st.metric(
                        "Match",
                        f"{score:.1f}%"
                    )

                st.progress(
                    min(
                        max(
                            float(
                                row["Similarity Score"]
                            ),
                            0.0
                        ),
                        1.0
                    )
                )

                st.markdown(
                    "**Relevant Skills**"
                )

                if display_skills:

                    skill_columns = st.columns(4)

                    for index, skill in enumerate(
                        display_skills
                    ):

                        with skill_columns[
                            index % 4
                        ]:

                            st.code(
                                skill,
                                language=None
                            )

                industry = str(
                    row.get("Industry", "")
                )

                if industry and industry != "nan":

                    st.caption(
                        f"Industry: {industry}"
                    )


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.header(
        "How it works"
    )

    st.write(
        """
        1. Enter at least three skills.
        2. Skills are converted into TF-IDF vectors.
        3. Cosine similarity compares your skills with job roles.
        4. The three highest matching roles are recommended.
        """
    )

    st.divider()

    st.markdown(
        "**Example Skills**"
    )

    st.write(
        "Python, Machine Learning, SQL"
    )

    st.write(
        "AWS, Docker, Kubernetes"
    )

    st.write(
        "Java, Spring, MySQL"
    )