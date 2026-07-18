import streamlit as st
import networkx as nx
from skill_graph import skill_graph, generate_roadmap, list_all_goals, draw_roadmap_graph, skill_resources

st.set_page_config(page_title="Student Roadmap Generator", page_icon="🎯", layout="centered")

st.title("🎯 Student Roadmap Generator")
st.write("Pick a career goal, tell us what you already know, and get a personalized learning roadmap.")

# --- Get all possible goals dynamically ---
all_goals = list_all_goals(skill_graph)

# --- Get all possible skills (for the "known skills" checklist) ---
all_skills = sorted(skill_graph.keys())

# --- Sidebar / main inputs ---
goal = st.selectbox("What do you want to become?", all_goals)

known_skills = st.multiselect(
    "Select the skills you already know:",
    options=all_skills,
    default=[]
)

# --- Generate roadmap on button click ---
if st.button("Generate Roadmap 🚀"):
    try:
        timeline = generate_roadmap(skill_graph, goal, known_skills)

        if not timeline:
            st.success("You already know everything needed for this goal! 🎉")
        else:
            total_weeks = timeline[-1]["cumulative_weeks"]
            st.subheader(f"Your roadmap to becoming a {goal}:")
            st.info(f"📅 Estimated total time: **{total_weeks} weeks** (~{round(total_weeks/4.3, 1)} months) at 5–8 hrs/week")

            for i, step in enumerate(timeline, 1):
                link = skill_resources.get(step['skill'])
                link_text = f" — [📚 Resource]({link})" if link else ""
                st.markdown(
                    f"**{i}. {step['skill']}** — {step['weeks']} week(s) "
                    f"&nbsp;·&nbsp; *by week {step['cumulative_weeks']}*{link_text}"
                )

            st.divider()
            st.caption(f"{len(timeline)} skills to go.")

            st.subheader("Visual Roadmap")
            fig = draw_roadmap_graph(skill_graph, timeline)
            st.pyplot(fig)

    except ValueError as e:
        st.error(str(e))

# --- Optional: show the graph visually ---
with st.expander("See full skill graph (advanced)"):
    st.write("This shows every skill and its prerequisites in the system.")
    for skill, prereqs in skill_graph.items():
        if prereqs:
            st.write(f"**{skill}** ← needs: {', '.join(prereqs)}")
        else:
            st.write(f"**{skill}** (no prerequisites)")