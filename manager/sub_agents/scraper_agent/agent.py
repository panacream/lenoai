from google.adk.agents.llm_agent import LlmAgent
from dotenv import load_dotenv

load_dotenv("../../.env")

from google.adk.agents.llm_agent import LlmAgent
from dotenv import load_dotenv
import os
from .scraper_tool import (
    selenium_scrape_headlines,
    simple_crawler,
    extract_linkedin_links_from_html,
    scrape_linkedin_profile
)

load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

scraper_agent = LlmAgent(
    name="scraper_agent",
    model="gemini-2.0-flash",
    description="Handles advanced web scraping, crawling, and Google Custom Search using Selenium and custom tools.",
    instruction="""
You are a scraper agent.
You can:
- Scrape and crawl web pages
- Extract LinkedIn profiles and recruiter contact info
- Perform Google searches using the Google Custom Search API (requires a valid Custom Search Engine ID from the user)

Use the available tools to scrape web pages, extract content, crawl links, process recruiter info, and search Google.

Available tools:
- selenium_scrape_headlines: Scrape a web page and return its title and all H1 headlines using Selenium.
- simple_crawler: Crawl web pages starting from a URL, returning all unique URLs found up to a given depth.
- extract_linkedin_links_from_html: Extract all unique LinkedIn profile URLs from a block of HTML (e.g., Google search results).
- scrape_linkedin_profile: Scrape a LinkedIn profile page and extract recruiter info (name, company, email, phone) using Selenium.

Always explain what you are doing and report any errors to the user.
""",
    tools=[
        selenium_scrape_headlines,
        simple_crawler,
        extract_linkedin_links_from_html,
        scrape_linkedin_profile,
    ],
)

# --- Shared Session State Example for Sub-Agents ---
def handle_scraper_task(task, session):
    """
    Example function for the scraper_agent to demonstrate reading/writing shared session state.
    All sub-agents should follow this pattern to access shared memory.
    """
    # Read from shared session state
    last_user_request = session.state.get('last_user_request')
    # Log this agent's last task
    session.state['scraper_agent_last_task'] = task
    # Optionally, append to a shared actions log
    session.state.setdefault('actions', []).append({
        'agent': 'scraper_agent',
        'task': task
    })
    # Return something for demonstration
    return {
        'last_user_request': last_user_request,
        'scraper_agent_last_task': task,
        'all_actions': session.state['actions']
    }

# Document for other sub-agents: Accept `session` as an argument, use session.state for shared memory.