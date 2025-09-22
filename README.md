# Healthcare AI Agent

A **Streamlit-based AI agent** designed to provide **healthcare information** using WHO guidelines, COVID-19 vaccine/symptom documents, and real-time COVID-19 statistical data analysis.

This agent integrates multiple tools, including **web scraping**, **knowledge base search**, and **SQL data analysis**, to deliver accurate, human-readable healthcare insights.

---

## Features

- **WHO Guidelines Access**
  Scrapes the official WHO publications site to provide the latest healthcare guidelines.

- **COVID-19 Vaccine & Symptom Information**
  Uses a document-based knowledge base to retrieve trusted information on vaccines and symptoms.

- **COVID-19 Data Analysis**
  Executes SQL queries on a COVID-19 dataset to provide statistics such as confirmed cases, recoveries, and deaths.

- **Conversational Interface**
  Streamlit chat UI with persistent session memory for continuous conversations.

---

## Setup Instructions

1. **Clone this repository**
   ```bash
   git clone https://github.com/ramiabu-shaqra/healthcare-ai-agent-aixplain.git
   ```

2. **Install dependencies**
   ```bash
   pip install aixplain
   pip install datasets
   pip install streamlit
   pip install pdfminer.six
   ```

3. **Set your API key**
   Replace the placeholder in the code with your actual `TEAM_API_KEY`:
   ```python
   os.environ["TEAM_API_KEY"] = "your_api_key_here"
   ```

4. **Prepare dataset and documents**
   Download and place the following files in your working directory:
   - [COVID-19 Dataset (Kaggle)](https://www.kaggle.com/datasets/imdevskp/corona-virus-report?resource=download) → save as `covid_19_dataset.csv`
   - [COVID-19 Vaccine Information Statement (CDC)](https://www.cdc.gov/vaccines/hcp/current-vis/downloads/covid-19.pdf) → save as `COVID-19_vaccine_information_statement.pdf`
   - [COVID-19 Symptoms Reference Document (Toronto)](https://thehub.utoronto.ca/family/wp-content/uploads/2020/09/COVID-19_reference_doc_symptoms.pdf) → save as `COVID-19_reference_doc_symptoms.pdf`

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

---

## Dataset & Sources

- **WHO Guidelines:** [https://www.who.int/publications/who-guidelines](https://www.who.int/publications/who-guidelines)
- **COVID-19 Dataset (Kaggle):** [Download Here](https://www.kaggle.com/datasets/imdevskp/corona-virus-report?resource=download)
- **COVID-19 Vaccine Document (CDC):** [Download Here](https://www.cdc.gov/vaccines/hcp/current-vis/downloads/covid-19.pdf)
- **COVID-19 Symptoms Document (Toronto):** [Download Here](https://thehub.utoronto.ca/family/wp-content/uploads/2020/09/COVID-19_reference_doc_symptoms.pdf)

---

## Tool Integration

This agent uses three main tools:

1. **Scraping Tool**
   - Fetches WHO guidelines directly from the official publications website.

2. **Knowledge Base Index**
   - Stores COVID-19 vaccine and symptom documents in a searchable format.

3. **SQL Tool**
   - Runs queries against the COVID-19 dataset (`covid_19_dataset.csv`).

---

## Example Inputs & Outputs

### 1. WHO Guidelines Query
- **User:** "How many guidelines were approved in July 2025?"
- **Agent:**
  "In July 2025, the World Health Organization approved a total of four guidelines. These guidelines focused on various health topics, including the management of asymptomatic sexually transmitted infections, clinical management of arboviral diseases, recommendations for the delivery of health services for the prevention and care of sexually transmitted infections, and a digital adaptation kit for self-monitoring of blood pressure during pregnancy. Each of these guidelines aims to enhance health outcomes and provide evidence-based recommendations for clinical practice and public health policy."
- **Tool Used:** `utilities-crewai-scrape_website_tool`

---

### 2. COVID-19 Data Query
- **User:** "How many confirmed COVID-19 cases in Jordan?"
- **Agent:**
  "As of now, Jordan has reported a total of 1,176 confirmed COVID-19 cases. This figure reflects the ongoing impact of the pandemic in the country and highlights the importance of continued public health measures and vaccination efforts."
- **Tool Used:** `SQL tool_query`

---

### 3. Vaccine Information Query
- **User:** "What are the allergic reactions that could appear after taking COVID-19 vaccine?"
- **Agent:**
  "After receiving a COVID-19 vaccine, some individuals may experience allergic reactions. Common reactions include pain, swelling, and redness at the injection site, as well as systemic symptoms such as fever, fatigue, headache, chills, muscle pain, joint pain, nausea, vomiting, and swollen lymph nodes.

  It is important to inform your vaccination provider if you have a history of allergic reactions to previous doses of COVID-19 vaccines or if you have severe, life-threatening allergies. In rare cases, a severe allergic reaction, known as anaphylaxis, can occur, which may manifest as hives, swelling of the face and throat, difficulty breathing, a fast heartbeat, dizziness, or weakness. If any of these symptoms arise, it is crucial to seek immediate medical attention."
- **Tool Used:** `search-aixplain-covid-19_knowledge_base_index`

---

### 4. Symptom Information Query
- **User:** "And what are the disease symptoms?"
- **Agent:**
  "COVID-19 symptoms may appear 2 to 14 days after exposure to the virus. Common symptoms include fever, chills, cough, shortness of breath or difficulty breathing, fatigue, muscle or body aches, headache, new loss of taste or smell, sore throat, congestion or runny nose, nausea, vomiting, and diarrhea.

  The severity of COVID-19 can range from mild to severe cases requiring hospitalization. Some individuals may experience symptoms that are not typically associated with other conditions, making it important to seek medical attention when suspected."
- **Tool Used:** `search-aixplain-covid-19_knowledge_base_index`

---

## Future Improvements

- **Expand Agent Coverage**
  Add more healthcare-related agents (e.g., nutrition, mental health).

- **UI Enhancements**
  Improve Streamlit interface with charts, dashboards, and interactive components.

- **Additional Data Integrations**
  Include real-time APIs for global health statistics and vaccination progress.
