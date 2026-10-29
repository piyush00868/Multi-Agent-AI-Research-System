# 🔬 Multi-Agent AI Research System

A multi-agent pipeline that takes a research topic and returns a structured, sourced report. Four stages run in sequence: a **Search Agent** finds recent sources, a **Reader Agent** scrapes the most relevant page, a **Writer Chain** drafts the report, and a **Critic Chain** scores and reviews it.

It can be used from the terminal or through a Streamlit web UI (**ResearchOS**).

---

## How It Works

```
Topic ──▶ 🔎 Search Agent ──▶ 📖 Reader Agent ──▶ ✍️ Writer Chain ──▶ 🧐 Critic Chain ──▶ Report + Feedback
          (Tavily search)     (scrape top URL)     (structured report)  (score + critique)
```

| Stage | Type | What it does |
|-------|------|--------------|
| **Search Agent** | LangChain agent + `web_search` tool | Queries Tavily for recent, reliable information on the topic (top 5 results from the past week, with title, URL and snippet). |
| **Reader Agent** | LangChain agent + `scrape_webpage` tool | Picks the most relevant URL from the search results and scrapes its text for deeper content. |
| **Writer Chain** | Prompt → LLM → string parser | Combines search results and scraped content into a report with Introduction, Key Findings (3+ points), Conclusion and Sources. |
| **Critic Chain** | Prompt → LLM → string parser | Reviews the report and returns a score out of 10, strengths, areas to improve and a one-line verdict. |

All stages use Google Gemini through `langchain-google-genai`.

---

## Project Structure

```
.
├── agents.py          # LLM setup, search/reader agents, writer and critic chains
├── tools.py           # web_search (Tavily) and scrape_webpage (requests + BeautifulSoup) tools
├── pipeline.py        # run_research_pipeline(): runs the four stages and returns the state
├── app.py             # Streamlit UI (ResearchOS)
├── requirements.txt   # Python dependencies
└── .gitignore
```

---

## Tech Stack

- **Python**
- **LangChain** (agents, prompt templates, output parsers)
- **Google Gemini** via `langchain-google-genai`
- **Tavily** for web search
- **BeautifulSoup4 + Requests** for scraping
- **Streamlit** for the web UI
- **python-dotenv** and **Rich** for configuration and terminal output

---

## Getting Started

### Prerequisites

- Python 3.10+
- A [Google AI Studio](https://aistudio.google.com/) API key (Gemini)
- A [Tavily](https://tavily.com/) API key

### Installation

```bash
git clone https://github.com/piyush00868/Multi-Agent-AI-Research-System.git
cd Multi-Agent-AI-Research-System

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
pip install tavily-python       # provides the TavilyClient imported in tools.py
```

### Configuration

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

`.env` is listed in `.gitignore`, so your keys stay out of version control.

---

## Usage

### Option 1: Streamlit UI

```bash
streamlit run app.py
```

Enter a topic, click **🚀 Start Research**, and read the result in the tabs. The report can be downloaded as a Markdown file, and previous runs in the current session appear in the sidebar under **Recent Research**.

### Option 2: Command line

```bash
python pipeline.py
```

You will be prompted for a topic, and each stage prints its output as it finishes.

### Option 3: Use it in your own code

```python
from pipeline import run_research_pipeline

state = run_research_pipeline("Latest developments in AI agents")

print(state["report"])      # final report
print(state["feedback"])    # critic's review
```

The returned dictionary contains:

| Key | Contents |
|-----|----------|
| `search_results` | Raw output of the Search Agent |
| `scraped_content` | Output of the Reader Agent |
| `report` | Report written by the Writer Chain |
| `feedback` | Score and critique from the Critic Chain |

---

## Example Output

**Report structure**

- Introduction
- Key Findings (at least 3 explained points)
- Conclusion
- Sources (URLs found in the research)

**Critic format**

```
Score: X/10
Strengths:
- ...
Areas to Improve:
- ...
One line verdict:
...
```

---

## Customization

- **Model**: change the `model` value of `ChatGoogleGenerativeAI` in `agents.py`.
- **Search behaviour**: adjust `max_results`, `topic` and `time_range` in `web_search` (`tools.py`).
- **Scrape size**: the scraper keeps the first 5,000 characters of cleaned page text; change the slice in `scrape_webpage`.
- **Report and critique style**: edit `writer_prompt` and `critic_prompt` in `agents.py`.

---

## Limitations

- The Reader Agent scrapes a single page per run, so reports reflect the search results plus one source in depth.
- Pages that block scraping, need JavaScript to render, or time out (10 s) return an error string instead of content.
- Report quality depends on the sources Tavily returns for the past week; very niche or older topics may produce thin results.

---

## Roadmap

- Scrape and summarize multiple sources per run
- Feed critic feedback back to the writer for an automatic revision pass
- Persist research history across sessions
- Export reports to PDF

---

