# Fund Brochure Generator

A Python utility that scrapes investment fund websites, intelligently selects relevant pages, and generates a concise, markdown-formatted brochure using OpenAI's GPT-4o-mini model.

---

## 📑 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

---

## 📘 Overview

This project automates the process of creating a summary brochure for investment funds. It:

- Crawls a fund's website to extract all links and page contents.
- Uses an LLM to classify and select only the most relevant subpages (e.g., Performance, Holdings, Fees).
- Scrapes the content of these pages.
- Generates a markdown brochure summarizing key aspects such as overview, strategy, risk, performance, and fees.

---

## 🚀 Features

- **Automated Web Scraping**: Fetches and parses fund website content and links.
- **Intelligent Link Selection**: Utilizes GPT-4o-mini to identify pages most relevant for fund brochures.
- **Brochure Generation**: Summarizes the collected information into a clean, readable markdown document.
- **Streaming Output**: Optionally streams the brochure generation process in real time within Jupyter notebooks.
- **Customizable**: Easily adapt prompts or extend logic for other financial products.

---

## 🛠 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/fund-brochure-generator.git
cd fund-brochure-generator
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set up environment variables:

Create a `.env` file in the project root with your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

See the [python-dotenv documentation](https://github.com/theskumar/python-dotenv) for details.

---

## 🧪 Usage

You can run the main logic in a Jupyter notebook or as a Python script.

Example (in a notebook):

```python
from your_module import stream_brochure

stream_brochure(
    "Kinetics Global No Load Class",
    "https://fundresearch.fidelity.com/mutual-funds/summary/494613805"
)
```

To use non-streaming (batch) mode, call the `create_brochure` function (uncomment in code).

---

## ⚙️ Configuration

- **Model**: Uses `gpt-4o-mini` by default. You can change the `MODEL` variable to use another OpenAI model.
- **Prompts**: System and user prompts are defined in the code and can be customized to adjust the brochure's style or focus.
- **Headers**: HTTP headers mimic a real browser to improve request compatibility.

---

## 🔍 How It Works

### Website Scraping:
- The `Website` class fetches HTML, extracts the title, all links, and main text from the body (excluding scripts and styles).

### Link Classification:
- The OpenAI model receives the list of links and returns a JSON object mapping key sections (Overview, Performance, etc.) to URLs.

### Content Aggregation:
- The selected pages are scraped, and their content is collected for brochure generation.

### Brochure Generation:
- All content is sent to the OpenAI model to generate a markdown summary focused on relevant fund details.

### Streaming Output:
- In Jupyter, the `stream_brochure` function streams the markdown output interactively.

---

## 📦 Dependencies

- Python 3.8+
- `requests`
- `beautifulsoup4`
- `python-dotenv`
- `openai`
- `IPython`

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to improve.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
