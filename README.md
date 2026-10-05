# PYSTDA45 - Pythonprogrammering och statistisk dataanalys
45-point course in the EC-utbildning Data Science program. This repository contains course materials, practical exercises, and individual/group projects bridging the gap between programming skills, mathematical theory, and real-world data analysis.

---

## 📈 Course Purpose & Overview
The primary objective of this course is to equip you with the essential **programming skills** and **mathematical tools** required to perform qualified, high-level data analysis. 

Throughout the course, we focus heavily on practical application—translating theoretical mathematical concepts into executable, clean, and efficient Python code.

---

## 🛠️ Tech Stack & Key Libraries
We use **Python** as our primary programming language. To manipulate, analyze, and visualize data, we work extensively with industry-standard libraries such as:

* **Data Handling:** [Pandas](https://pydata.org) & [NumPy](https://numpy.org)
* **Data Visualization:** [Matplotlib](https://matplotlib.org)
* **Standard Utilities & Engineering:** `json`, `argparse`, `hashlib`, `os`, `random`

---

## 💻 Development Environment & Tools
To build, test, and collaborate on the course modules, the following professional environment is utilized:

* **IDE / Editor:** [Visual Studio Code (VS Code)](https://visualstudio.com) for writing clean scripts, refactoring, and debugging.
* **Collaboration:** [VS Code Live Share](https://microsoft.com) used for agile team collaboration, real-time pair programming, and collaborative debugging.
* **Interactive Analysis:** [Jupyter Notebooks](https://jupyter.org) for exploratory data analysis, testing out statistical models, and visualizing data step-by-step.
* **Version Control:** Managed history and synchronized development pipelines using **Git** and [GitHub](https://github.com).

---

## 🧠 Core Topics & Engineering Insights

### 1. Python Programming & Architecture
* **Object-Oriented Programming (OOP):** Designing decoupled and scalable applications. Focus lies on structuring programs into modular classes with dedicated responsibilities (e.g., separating data ingestion, business logic, and user interfaces).
* **Data Structures:** Strategic usage of advanced built-in Python structures such as nested dictionaries, sets, and tuples depending on the data modeling needs.
* **Data Persistence:** Utilizing the `json` and `os` modules to separate static application data from runtime execution, enabling robust reading/writing states.
* **CLI Engineering & Input Defense:** Implementing the `argparse` library to handle complex command-line arguments and flags efficiently, paired with robust input validation algorithms.
* **Cryptographic Security:** Utilizing the `hashlib` library to implement secure identity validation using one-way cryptographic hashing algorithms (SHA-256) enhanced with unique salt strings.
* **Reproducibility:** Structuring workflows, configurations, and clean code principles (PEP 8) to ensure reliable and repeatable data execution.

### 2. Applied Project: Quiz Application
As a practical laboratory playground to test out early engineering principles, this repository includes an ongoing **Quiz Application**. Rather than just running a simple procedural script, the application serves as a hands-on exercise in transitioning basic data tracking into an **Object-Oriented architecture**. It implements command-line parsing, encrypted administrative panels, automated JSON file persistence, and robust defensive programming against invalid user inputs.

### 3. Mathematics & Data Science
* **Probability & EDA:** Exploratory Data Analysis, descriptive statistics, and data cleaning pipelines.
* **Statistical Inference:** Sampling, variation, confidence intervals, p-values, and hypothesis testing (A/B testing).
* **Linear Algebra & Regression:** Vectors, matrices, and coordinate transformations linked directly to linear regression and practical data analysis.

### 4. Agile Methodologies & Team Collaboration
Beyond the technical stack, this course emphasizes how modern software teams actually organize and deliver work. We study and apply three core agile frameworks:

* **SCRUM:** Structuring work into time-boxed sprints, with defined roles (Product Owner, Scrum Master, Development Team) and ceremonies (sprint planning, daily stand-ups, sprint review, and retrospective) to iteratively deliver working increments of a product.
* **Kanban:** Visualizing workflow using a continuous-flow board (To Do / In Progress / Done), limiting work-in-progress to improve throughput and identify bottlenecks without fixed sprint cycles.
* **Extreme Programming (XP):** Engineering-focused practices that reinforce code quality and collaboration, including pair programming, test-driven development (TDD), continuous integration, and frequent, small releases.

These frameworks are applied hands-on throughout the course's group projects, using tools like GitHub Issues/Projects for backlog and task tracking, alongside VS Code Live Share for real-time pair programming sessions.

---

## 🎓 Learning Outcomes
By the end of this course, you will be able to:
1. **Write & Structure Python Code:** Develop clean, modular, and maintainable scripts adhering to best practices and OOP architecture.
2. **Analyze Complex Data:** Clean, manipulate, and extract meaningful insights from diverse datasets using Pandas.
3. **Present Professional Results:** Create compelling data visualizations and communicate statistical findings in a clear, structured manner.

---

## 🏁 Getting Started

### Prerequisites
Make sure you have Python installed. It is highly recommended to use a virtual environment or an [Anaconda distribution](https://anaconda.com).

### Installation
Clone this repository to your local machine:
```bash
git clone https://github.comYOUR-USERNAME/YOUR-REPOSITORY-NAME.git
cd YOUR-REPOSITORY-NAME
```

Install the required packages:
```bash
pip install -r requirements.txt
```
