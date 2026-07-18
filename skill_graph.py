import textwrap
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ---------------------------------------------------------------------------
# DATASET: skill -> { prereqs: [...], weeks: N }
# ---------------------------------------------------------------------------
skill_graph = {
    # --- Foundations (shared across all paths) ---
    "Programming Fundamentals": {"prereqs": [], "weeks": 3},
    "Git & GitHub": {"prereqs": [], "weeks": 1},
    "Command Line Basics": {"prereqs": [], "weeks": 1},
    "Data Structures & Algorithms": {"prereqs": ["Programming Fundamentals"], "weeks": 6},
    "OOP Concepts": {"prereqs": ["Programming Fundamentals"], "weeks": 2},

    # --- Python-specific / Data Science track ---
    "Python Basics": {"prereqs": ["Programming Fundamentals"], "weeks": 2},
    "Pandas & Numpy": {"prereqs": ["Python Basics"], "weeks": 2},
    "Statistics": {"prereqs": ["Python Basics"], "weeks": 3},
    "SQL": {"prereqs": ["Python Basics"], "weeks": 2},
    "Data Visualization": {"prereqs": ["Pandas & Numpy"], "weeks": 1},
    "Machine Learning Basics": {"prereqs": ["Pandas & Numpy", "Statistics"], "weeks": 4},
    "Deep Learning": {"prereqs": ["Machine Learning Basics"], "weeks": 5},
    "NLP Basics": {"prereqs": ["Machine Learning Basics"], "weeks": 3},
    "Computer Vision Basics": {"prereqs": ["Deep Learning"], "weeks": 3},
    "Model Deployment": {"prereqs": ["Machine Learning Basics", "Git & GitHub"], "weeks": 2},
    "MLOps": {"prereqs": ["Model Deployment", "Command Line Basics"], "weeks": 3},
    "Data Engineering Basics": {"prereqs": ["SQL", "Python Basics"], "weeks": 3},
    "Big Data Tools (Spark/Hadoop)": {"prereqs": ["Data Engineering Basics"], "weeks": 4},
    "Data Warehousing": {"prereqs": ["Data Engineering Basics"], "weeks": 2},
    "Data Scientist": {"prereqs": ["Machine Learning Basics", "SQL", "Data Visualization"], "weeks": 1},
    "ML Engineer": {"prereqs": ["Deep Learning", "Model Deployment"], "weeks": 1},
    "AI Research Engineer": {"prereqs": ["Deep Learning", "NLP Basics", "Computer Vision Basics"], "weeks": 1},
    "Data Engineer": {"prereqs": ["Big Data Tools (Spark/Hadoop)", "Data Warehousing"], "weeks": 1},

    # --- Web track ---
    "HTML/CSS": {"prereqs": [], "weeks": 2},
    "JavaScript Basics": {"prereqs": ["HTML/CSS"], "weeks": 3},
    "React Basics": {"prereqs": ["JavaScript Basics"], "weeks": 3},
    "State Management (Redux/Context)": {"prereqs": ["React Basics"], "weeks": 2},
    "TypeScript": {"prereqs": ["JavaScript Basics"], "weeks": 2},
    "Node.js & Express": {"prereqs": ["JavaScript Basics"], "weeks": 3},
    "REST APIs": {"prereqs": ["Node.js & Express"], "weeks": 2},
    "GraphQL": {"prereqs": ["REST APIs"], "weeks": 2},
    "Databases (SQL/NoSQL)": {"prereqs": ["Node.js & Express"], "weeks": 2},
    "Authentication & Security Basics": {"prereqs": ["REST APIs"], "weeks": 2},
    "Frontend Developer": {"prereqs": ["React Basics", "State Management (Redux/Context)", "Git & GitHub"], "weeks": 1},
    "Backend Developer": {"prereqs": ["REST APIs", "Databases (SQL/NoSQL)", "Authentication & Security Basics"], "weeks": 1},
    "Full Stack Developer": {"prereqs": ["Frontend Developer", "Backend Developer"], "weeks": 1},

    # --- UI/UX track ---
    "Design Principles": {"prereqs": [], "weeks": 2},
    "Wireframing & Prototyping (Figma)": {"prereqs": ["Design Principles"], "weeks": 2},
    "User Research Basics": {"prereqs": ["Design Principles"], "weeks": 2},
    "UI/UX Designer": {"prereqs": ["Wireframing & Prototyping (Figma)", "User Research Basics"], "weeks": 1},

    # --- Mobile track ---
    "Kotlin Basics": {"prereqs": ["OOP Concepts"], "weeks": 2},
    "Android UI (XML/Jetpack Compose)": {"prereqs": ["Kotlin Basics"], "weeks": 3},
    "Android App Architecture": {"prereqs": ["Android UI (XML/Jetpack Compose)"], "weeks": 2},
    "Android Developer": {"prereqs": ["Android App Architecture", "Git & GitHub"], "weeks": 1},

    "Swift Basics": {"prereqs": ["OOP Concepts"], "weeks": 2},
    "iOS UI (SwiftUI/UIKit)": {"prereqs": ["Swift Basics"], "weeks": 3},
    "iOS App Architecture": {"prereqs": ["iOS UI (SwiftUI/UIKit)"], "weeks": 2},
    "iOS Developer": {"prereqs": ["iOS App Architecture", "Git & GitHub"], "weeks": 1},

    "React Native Basics": {"prereqs": ["React Basics"], "weeks": 3},
    "Cross-Platform Mobile Developer": {"prereqs": ["React Native Basics", "Git & GitHub"], "weeks": 1},

    # --- DevOps / Cloud track ---
    "Linux Basics": {"prereqs": ["Command Line Basics"], "weeks": 2},
    "Networking Basics": {"prereqs": [], "weeks": 2},
    "Docker": {"prereqs": ["Linux Basics"], "weeks": 2},
    "Kubernetes": {"prereqs": ["Docker"], "weeks": 3},
    "CI/CD Pipelines": {"prereqs": ["Docker", "Git & GitHub"], "weeks": 2},
    "Cloud Basics (AWS/GCP/Azure)": {"prereqs": ["Linux Basics", "Networking Basics"], "weeks": 3},
    "Infrastructure as Code (Terraform)": {"prereqs": ["Cloud Basics (AWS/GCP/Azure)"], "weeks": 2},
    "Monitoring & Logging": {"prereqs": ["Cloud Basics (AWS/GCP/Azure)"], "weeks": 1},
    "DevOps Engineer": {"prereqs": ["Kubernetes", "CI/CD Pipelines", "Cloud Basics (AWS/GCP/Azure)"], "weeks": 1},
    "Cloud Architect": {"prereqs": ["Infrastructure as Code (Terraform)", "Monitoring & Logging"], "weeks": 1},

    # --- Cybersecurity track ---
    "Networking Fundamentals": {"prereqs": ["Networking Basics"], "weeks": 2},
    "Operating System Security": {"prereqs": ["Linux Basics"], "weeks": 2},
    "Cryptography Basics": {"prereqs": ["Networking Fundamentals"], "weeks": 2},
    "Ethical Hacking Basics": {"prereqs": ["Networking Fundamentals", "Operating System Security"], "weeks": 3},
    "Security Tools (Wireshark, Nmap, Burp Suite)": {"prereqs": ["Ethical Hacking Basics"], "weeks": 2},
    "Cybersecurity Analyst": {"prereqs": ["Cryptography Basics", "Security Tools (Wireshark, Nmap, Burp Suite)"], "weeks": 1},

    # --- QA / Testing track ---
    "Manual Testing Basics": {"prereqs": [], "weeks": 2},
    "Test Automation (Selenium/Playwright)": {"prereqs": ["Manual Testing Basics", "Programming Fundamentals"], "weeks": 3},
    "API Testing": {"prereqs": ["Manual Testing Basics"], "weeks": 2},
    "QA Engineer": {"prereqs": ["Test Automation (Selenium/Playwright)", "API Testing"], "weeks": 1},

    # --- Game Dev track ---
    "C# Basics": {"prereqs": ["OOP Concepts"], "weeks": 2},
    "Unity Engine Basics": {"prereqs": ["C# Basics"], "weeks": 3},
    "Game Design Principles": {"prereqs": [], "weeks": 2},
    "Game Developer": {"prereqs": ["Unity Engine Basics", "Game Design Principles"], "weeks": 1},

    # --- Blockchain track ---
    "Blockchain Fundamentals": {"prereqs": ["Programming Fundamentals"], "weeks": 2},
    "Solidity Basics": {"prereqs": ["Blockchain Fundamentals"], "weeks": 3},
    "Smart Contract Development": {"prereqs": ["Solidity Basics"], "weeks": 3},
    "Blockchain Developer": {"prereqs": ["Smart Contract Development"], "weeks": 1},

    # --- Product Management track ---
    "Product Thinking Basics": {"prereqs": [], "weeks": 2},
    "Market & User Research": {"prereqs": ["Product Thinking Basics"], "weeks": 2},
    "Roadmapping & Prioritization": {"prereqs": ["Product Thinking Basics"], "weeks": 2},
    "Product Manager": {"prereqs": ["Market & User Research", "Roadmapping & Prioritization"], "weeks": 1},
}

# ---------------------------------------------------------------------------
# LEARNING RESOURCES (free/well-known links per skill)
# ---------------------------------------------------------------------------
skill_resources = {
    "Programming Fundamentals": "https://www.freecodecamp.org/",
    "Git & GitHub": "https://docs.github.com/en/get-started",
    "Command Line Basics": "https://www.freecodecamp.org/news/command-line-for-beginners/",
    "Data Structures & Algorithms": "https://www.geeksforgeeks.org/data-structures/",
    "OOP Concepts": "https://realpython.com/python3-object-oriented-programming/",
    "Python Basics": "https://docs.python.org/3/tutorial/",
    "Pandas & Numpy": "https://pandas.pydata.org/docs/getting_started/index.html",
    "Statistics": "https://www.khanacademy.org/math/statistics-probability",
    "SQL": "https://www.w3schools.com/sql/",
    "Data Visualization": "https://matplotlib.org/stable/tutorials/index.html",
    "Machine Learning Basics": "https://www.coursera.org/learn/machine-learning",
    "Deep Learning": "https://www.deeplearning.ai/",
    "NLP Basics": "https://huggingface.co/learn/nlp-course",
    "Computer Vision Basics": "https://opencv.org/university/",
    "Model Deployment": "https://fastapi.tiangolo.com/",
    "MLOps": "https://ml-ops.org/",
    "Data Engineering Basics": "https://www.coursera.org/specializations/data-engineering",
    "Big Data Tools (Spark/Hadoop)": "https://spark.apache.org/docs/latest/",
    "Data Warehousing": "https://cloud.google.com/learn/what-is-a-data-warehouse",
    "HTML/CSS": "https://developer.mozilla.org/en-US/docs/Learn/HTML",
    "JavaScript Basics": "https://javascript.info/",
    "React Basics": "https://react.dev/learn",
    "State Management (Redux/Context)": "https://redux.js.org/introduction/getting-started",
    "TypeScript": "https://www.typescriptlang.org/docs/handbook/intro.html",
    "Node.js & Express": "https://expressjs.com/en/starter/installing.html",
    "REST APIs": "https://restfulapi.net/",
    "GraphQL": "https://graphql.org/learn/",
    "Databases (SQL/NoSQL)": "https://www.mongodb.com/nosql-explained",
    "Authentication & Security Basics": "https://auth0.com/docs/get-started",
    "Design Principles": "https://lawsofux.com/",
    "Wireframing & Prototyping (Figma)": "https://help.figma.com/hc/en-us",
    "User Research Basics": "https://www.nngroup.com/articles/",
    "Kotlin Basics": "https://kotlinlang.org/docs/getting-started.html",
    "Android UI (XML/Jetpack Compose)": "https://developer.android.com/jetpack/compose",
    "Android App Architecture": "https://developer.android.com/topic/architecture",
    "Swift Basics": "https://developer.apple.com/swift/",
    "iOS UI (SwiftUI/UIKit)": "https://developer.apple.com/tutorials/swiftui",
    "iOS App Architecture": "https://developer.apple.com/documentation/",
    "React Native Basics": "https://reactnative.dev/docs/getting-started",
    "Linux Basics": "https://linuxjourney.com/",
    "Networking Basics": "https://www.cloudflare.com/learning/network-layer/what-is-a-computer-network/",
    "Docker": "https://docs.docker.com/get-started/",
    "Kubernetes": "https://kubernetes.io/docs/tutorials/",
    "CI/CD Pipelines": "https://docs.github.com/en/actions",
    "Cloud Basics (AWS/GCP/Azure)": "https://aws.amazon.com/getting-started/",
    "Infrastructure as Code (Terraform)": "https://developer.hashicorp.com/terraform/tutorials",
    "Monitoring & Logging": "https://grafana.com/tutorials/",
    "Networking Fundamentals": "https://www.comptia.org/certifications/network",
    "Operating System Security": "https://www.cisecurity.org/",
    "Cryptography Basics": "https://cryptozombies.io/",
    "Ethical Hacking Basics": "https://www.hackthebox.com/",
    "Security Tools (Wireshark, Nmap, Burp Suite)": "https://www.wireshark.org/docs/",
    "Manual Testing Basics": "https://www.guru99.com/software-testing.html",
    "Test Automation (Selenium/Playwright)": "https://playwright.dev/docs/intro",
    "API Testing": "https://learning.postman.com/docs/introduction/overview/",
    "C# Basics": "https://learn.microsoft.com/en-us/dotnet/csharp/",
    "Unity Engine Basics": "https://learn.unity.com/",
    "Game Design Principles": "https://www.gamedesigning.org/learn/",
    "Blockchain Fundamentals": "https://ethereum.org/en/developers/docs/",
    "Solidity Basics": "https://docs.soliditylang.org/",
    "Smart Contract Development": "https://cryptozombies.io/",
    "Product Thinking Basics": "https://www.productplan.com/learn/",
    "Market & User Research": "https://www.nngroup.com/articles/",
    "Roadmapping & Prioritization": "https://www.productplan.com/learn/product-roadmap/",
}

# ---------------------------------------------------------------------------
# CORE LOGIC
# ---------------------------------------------------------------------------
def generate_roadmap(graph_dict, goal, known_skills=None):
    """
    Given the skill graph, a target goal, and skills the user already knows,
    return an ordered list of dicts: {skill, weeks, cumulative_weeks}.
    """
    if known_skills is None:
        known_skills = []

    G = nx.DiGraph()
    for skill, data in graph_dict.items():
        G.add_node(skill)
        for p in data["prereqs"]:
            G.add_edge(p, skill)

    if goal not in G:
        raise ValueError(
            f"Goal '{goal}' not found in skill graph. "
            f"Available goals: {list_all_goals(graph_dict)}"
        )

    ancestors = nx.ancestors(G, goal)
    ancestors.add(goal)
    subgraph = G.subgraph(ancestors)

    order = list(nx.topological_sort(subgraph))
    roadmap = [skill for skill in order if skill not in known_skills]

    timeline = []
    cumulative = 0
    for skill in roadmap:
        weeks = graph_dict[skill]["weeks"]
        cumulative += weeks
        timeline.append({
            "skill": skill,
            "weeks": weeks,
            "cumulative_weeks": cumulative
        })

    return timeline


def list_all_goals(graph_dict):
    """Nodes that are never a prerequisite for anything else (end-goal careers)."""
    all_skills = set(graph_dict.keys())
    used_as_prereq = set()
    for data in graph_dict.values():
        used_as_prereq.update(data["prereqs"])
    return sorted(all_skills - used_as_prereq)


# ---------------------------------------------------------------------------
# VISUAL ROADMAP (top-to-bottom flowchart with wrapped-text boxes)
# ---------------------------------------------------------------------------
def draw_roadmap_graph(graph_dict, timeline):
    """
    Draws the roadmap as a top-to-bottom flowchart with rectangular boxes
    and wrapped text, so long skill names stay readable.
    """
    skills_in_path = [step["skill"] for step in timeline]
    n = len(skills_in_path)

    fig_height = max(6, n * 1.1)
    fig, ax = plt.subplots(figsize=(8, fig_height))

    box_width = 5.5
    box_height = 0.8
    gap = 0.5
    x_center = 3

    positions = {}
    y = 0
    for skill in skills_in_path:
        positions[skill] = (x_center, y)
        y -= (box_height + gap)

    # Draw boxes
    for skill in skills_in_path:
        x, y_pos = positions[skill]
        wrapped_text = "\n".join(textwrap.wrap(skill, width=26))

        box = mpatches.FancyBboxPatch(
            (x - box_width / 2, y_pos - box_height / 2),
            box_width, box_height,
            boxstyle="round,pad=0.05,rounding_size=0.1",
            linewidth=1.5,
            edgecolor="#B23A3A",
            facecolor="#FF6B6B"
        )
        ax.add_patch(box)
        ax.text(x, y_pos, wrapped_text, ha="center", va="center",
                 fontsize=9, fontweight="bold", color="white")

    # Draw arrows connecting each step to the next
    for i in range(n - 1):
        skill_a = skills_in_path[i]
        skill_b = skills_in_path[i + 1]
        x_a, y_a = positions[skill_a]
        x_b, y_b = positions[skill_b]

        ax.annotate(
            "", xy=(x_b, y_b + box_height / 2 + 0.05),
            xytext=(x_a, y_a - box_height / 2 - 0.05),
            arrowprops=dict(arrowstyle="->", color="#888888", lw=1.5)
        )

    ax.set_xlim(0, 6)
    ax.set_ylim(y - 1, box_height)
    ax.set_axis_off()
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# STANDALONE TEST
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Available career goals:", list_all_goals(skill_graph))

    goal = "Full Stack Developer"
    known = ["HTML/CSS", "Programming Fundamentals"]

    timeline = generate_roadmap(skill_graph, goal, known)

    print(f"\nRoadmap to become a {goal}:\n")
    for i, step in enumerate(timeline, 1):
        print(f"{i}. {step['skill']} — {step['weeks']} week(s) "
              f"(by week {step['cumulative_weeks']})")