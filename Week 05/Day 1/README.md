\# Week 5 Day 1 - PandasAI + Ollama



\## Objective



Use PandasAI with a real Indian Census 2011 dataset and a local Ollama LLM to answer natural-language data questions.



\## Dataset



Indian District Census 2011 dataset.



\- Rows: 640

\- Columns: 118

\- Dataset file: `india\_districts\_census\_2011.csv`



\## Tools Used



\- Python 3.11

\- PandasAI 3.0.0

\- Pandas

\- Ollama

\- Llama 3.2 3B

\- LiteLLM



\## Tasks Completed



\### 1. PandasAI Natural Language Queries



Tested PandasAI using natural-language questions such as:



\- Average population across districts

\- Total population

\- Top 10 districts by population



The local Ollama model was used instead of a paid cloud API.



\### 2. PandasAI vs Manual Pandas



Three questions were compared using PandasAI and manual Pandas calculations.



| Question | Result |

|---|---|

| Average population | MATCH |

| Total population | MATCH |

| Number of districts | MATCH |



\### 3. Error Handling



Added `pandasai\_error\_handling.py` to handle failed PandasAI queries.



Errors are logged to:



`pandasai\_errors.log`



The error log captures failed queries, timestamps, exception types, and tracebacks.



\## Files



\- `india\_districts\_census\_2011.csv` - Dataset

\- `test\_pandasai.py` - PandasAI query testing

\- `pandasai\_comparison.py` - Manual Pandas comparison

\- `pandasai\_error\_handling.py` - Error handling implementation

\- `pandasai\_errors.log` - Error evidence

\- `README.md` - Task documentation

