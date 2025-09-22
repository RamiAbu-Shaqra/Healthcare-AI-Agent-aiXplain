import os

# Setup API key
os.environ["TEAM_API_KEY"] = "YOUR TEAM API KEY HERE"

import re
from concurrent.futures import ThreadPoolExecutor
from pdfminer.high_level import extract_text

from aixplain.factories import AgentFactory, IndexFactory
from aixplain.modules.model.record import Record
from aixplain.enums import AssetStatus

AGENT_NAME = "Healthcare Information Agent"


class AgentManager:
    _instance = None
    _agent = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentManager, cls).__new__(cls)
        return cls._instance

    def get_agent(self):
        """Get the agent, initializing it only once."""
        if not self._initialized:
            self._agent = self._initialize_agent()
            self._initialized = True
        return self._agent

    def _check_existing_agent(self):
        """Check if there's already a deployed agent with the same name."""
        try:
            existing_agents = AgentFactory.list()

            if existing_agents and "results" in existing_agents:
                for existing_agent in existing_agents["results"]:
                    if (existing_agent.name == AGENT_NAME and
                            existing_agent.status == AssetStatus.ONBOARDED):
                        return existing_agent
            return None
        except Exception as e:
            print(f"Error checking for existing agent: {e}")
            return None

    def _initialize_agent(self):
        """Initialize the agent - either use existing or create new."""
        # First check if there's already a deployed agent
        existing_agent = self._check_existing_agent()
        if existing_agent:
            return existing_agent

        # No deployed agent found, create a new one
        return self._setup_new_agent()

    def _setup_new_agent(self):
        """Set up a completely new agent with all tools and indexes."""

        # Function to read PDF and extract text
        def read_pdf_text(pdf_path: str):
            try:
                text = extract_text(pdf_path)
                text = text.replace("\n", " ")
                return text
            except Exception as exception:
                print(f"Error in reading PDF file: {exception}")
                return None

        # Function to chunk text into smaller sections
        def chunk_text(text, max_chunk_size=100):
            sentences = re.split(r'(?<=[.!?]) +', text)
            chunks = []
            current_chunk = ""
            for sentence in sentences:
                if len(current_chunk) + len(sentence) <= max_chunk_size:
                    current_chunk += sentence + " "
                else:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence + " "
            if current_chunk:
                chunks.append(current_chunk.strip())
            return chunks

        # Function to process a single document and return a list of chunked records
        def process_document(doc):
            text = read_pdf_text(doc["pdf_url"])
            initial_records = []
            if text:
                chunks = chunk_text(text)
                for i, chunk in enumerate(chunks):
                    if chunk.strip():  # check if chunk is not empty or just whitespace
                        record = Record(
                            id=f"{doc['id']}_{i}",
                            value=chunk,
                            attributes={"category": doc["category"]})
                        initial_records.append(record)
            return initial_records

        # List of document
        data = [
            {"id": '1', "pdf_url": "COVID-19_vaccine_information_statement.pdf", "category": "COVID-19 Vaccine"},
            {"id": '2', "pdf_url": "COVID-19_reference_doc_symptoms.pdf", "category": "COVID-19 Symptoms"}
        ]

        # Process all PDF files in parallel
        with ThreadPoolExecutor() as executor:
            all_record_batches = executor.map(process_document, data)

        # Flatten the list of lists into one list of records
        records = [record for batch in all_record_batches for record in batch]

        # Get the existing indexes and delete them before creating a new one
        result = IndexFactory.list(query="COVID-19 Knowledge Base Index")
        indexes = result.get("results", [])
        for idx in indexes:
            idx.delete()

        # Create a new index for the COVID-19 knowledge base
        covid_19_index = IndexFactory.create(
            name="COVID-19 Knowledge Base Index",
            description="Index for COVID-19 knowledge base"
        )
        covid_19_index.upsert(records)

        # Setting up tools
        scraping_tool = AgentFactory.create_model_tool(model="66f423426eb563fa213a3531")  # Scrape Website Tool
        index_tool = AgentFactory.create_model_tool(
            model=covid_19_index,
            description="Search answers for COVID-19 knowledge base"
        )
        sql_tool = AgentFactory.create_sql_tool(
            name="SQL tool", description="Execute SQL queries on COVID-19 data",
            source="covid_19_dataset.csv", source_type="csv", tables=["COVID19"]
        )

        DESCRIPTION = (
            "A healthcare information agent that provides WHO guidelines, COVID-19 vaccine/symptom information, "
            "and COVID-19 data analysis")
        INSTRUCTION = (
            "You are a comprehensive healthcare information agent that helps users find WHO guidelines, "
            "COVID-19 vaccine and symptom information, and analyze COVID-19 statistical data. "
            "CRITICAL: You MUST ALWAYS provide responses in clear, human-readable text format. "
            "Never return raw JSON, XML, "
            "or structured data formats. "
            ""
            "Your capabilities include: "
            "1. Web scraping: Use the 'Scrape Website Tool' to fetch the latest WHO guidelines from "
            "[https://www.who.int/publications/who-guidelines] "
            "2. Knowledge base search: Use the 'Search answers for COVID-19 knowledge base' tool to find specific "
            "information about: "
            "   - COVID-19 vaccine information, effectiveness, and safety "
            "   - COVID-19 symptoms, diagnosis, and clinical guidance "
            "3. Data analysis: Use the 'SQL tool' to execute queries on COVID-19 dataset for statistical "
            "analysis and insights "
            ""
            "RESPONSE FORMATTING RULES (MANDATORY): "
            "1. Convert ALL tool outputs into natural language paragraphs and sentences "
            "2. Use clear headings (## for main topics, ### for subtopics) "
            "3. Present information as readable prose, not as data structures "
            "4. Use bullet points (•) only for listing items within sentences "
            "5. Write complete sentences and paragraphs that flow naturally "
            "6. If tool returns JSON/structured data, extract the meaningful information and rewrite it as "
            "human-readable text "
            ""
            "Your workflow should be: "
            "1. For WHO guidelines requests: "
            "   - Use the scraping tool to fetch the latest data from WHO website "
            "   - Extract key information from any structured data returned "
            "   - Rewrite the information as clear, flowing paragraphs "
            "   - Organize with proper headings and natural language structure "
            ""
            "2. For COVID-19 vaccine or symptom questions: "
            "   - Use the knowledge base search tool to find relevant information from the indexed documents "
            "   - Present findings in a clear, educational format "
            "   - Provide comprehensive answers based on the available medical literature "
            "   - Cite information appropriately when drawing from specific sources "
            ""
            "3. For COVID-19 data analysis queries: "
            "   - Use the SQL tool to query the dataset "
            "   - Convert numerical results into meaningful insights written in complete sentences "
            "   - Explain what the data means in plain English "
            "   - Provide context and implications of the statistical findings "
            ""
            "TOOL SELECTION GUIDELINES: "
            "- Use the knowledge base tool for specific medical questions about vaccines or symptoms "
            "- Use the web scraping tool for the most current WHO guidelines and recommendations "
            "- Use the SQL tool for statistical analysis, trends, and data-driven insights "
            "- You may use multiple tools in combination to provide comprehensive answers "
            ""
            "Always prioritize accuracy, clarity, and patient safety in your responses."
        )

        # Create the agent
        agent = AgentFactory.create(
            name=AGENT_NAME,
            tools=[scraping_tool, index_tool, sql_tool],
            description=DESCRIPTION,
            instructions=INSTRUCTION,
            llm_id="669a63646eb56306647e1091"  # GPT-4o Mini
        )

        # Deploy the agent
        agent.deploy()

        return agent


# Global function to get the agent instance
def get_healthcare_agent():
    """Get the healthcare agent instance."""
    agent_manager = AgentManager()
    return agent_manager.get_agent()
