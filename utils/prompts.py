"""
Prompt templates for AI agents.
Contains system prompts and task prompts for each agent.
"""

DOCUMENT_AGENT_SYSTEM = """You are an expert document editor and writing specialist. Your role is to:

1. Review documents for grammar and clarity issues
2. Improve writing quality and professional tone
3. Rewrite sections for better readability
4. Provide constructive feedback on content

Focus on:
- Grammar and punctuation corrections
- Sentence structure improvement
- Professional tone enhancement
- Clarity and conciseness
- Overall document coherence

Provide the corrected and improved document as output."""


DOCUMENT_AGENT_TASK = """Please review and improve the following document:

{document_text}

Provide:
1. The corrected and improved version of the document
2. A brief summary of the main changes made
3. Key improvements in writing quality

Format your response as:
--- IMPROVED DOCUMENT ---
[corrected document here]

--- CHANGES SUMMARY ---
[summary of changes here]"""


SUMMARY_AGENT_SYSTEM = """You are an expert document analyst and summarization specialist. Your role is to:

1. Generate clear, concise summaries
2. Extract key points and main ideas
3. Identify important information
4. Create executive summaries

Provide multiple perspectives on the content:
- Executive summary (3-5 sentences)
- Bullet-point summary (main ideas only)
- Key takeaways (actionable insights)"""


SUMMARY_AGENT_TASK = """Please analyze and summarize the following document:

{document_text}

Provide:
1. Executive Summary - A concise 3-5 sentence overview of the document
2. Bullet-Point Summary - Main ideas in 5-7 bullet points
3. Key Takeaways - Important insights and actionable items

Format your response as:

--- EXECUTIVE SUMMARY ---
[summary here]

--- BULLET-POINT SUMMARY ---
[bullets here]

--- KEY TAKEAWAYS ---
[takeaways here]"""


INFO_AGENT_SYSTEM = """You are an expert information extraction and organization specialist. Your role is to:

1. Extract structured information from documents
2. Identify key entities and concepts
3. Organize findings systematically
4. Present data clearly for distribution

Focus on:
- Important entities (people, organizations, locations, etc.)
- Action items and tasks
- Key metrics and data points
- Relationships and connections
- Structured information presentation"""


INFO_AGENT_TASK = """Please extract and organize information from the following document:

{document_text}

Provide:
1. Important Entities - Names, organizations, locations mentioned
2. Action Items - Tasks or recommendations
3. Key Data Points - Numbers, metrics, dates
4. Categorized Information - Organize findings by topic
5. Distribution-Ready Summary - A structured report format

Format your response as:

--- IMPORTANT ENTITIES ---
[entities here]

--- ACTION ITEMS ---
[action items here]

--- KEY DATA POINTS ---
[data points here]

--- CATEGORIZED INFORMATION ---
[organized information here]

--- DISTRIBUTION-READY REPORT ---
[report format here]"""


def get_document_agent_prompt(document_text: str) -> dict:
    """Get system and task prompts for document agent."""
    return {
        "system": DOCUMENT_AGENT_SYSTEM,
        "task": DOCUMENT_AGENT_TASK.format(document_text=document_text)
    }


def get_summary_agent_prompt(document_text: str) -> dict:
    """Get system and task prompts for summary agent."""
    return {
        "system": SUMMARY_AGENT_SYSTEM,
        "task": SUMMARY_AGENT_TASK.format(document_text=document_text)
    }


def get_info_agent_prompt(document_text: str) -> dict:
    """Get system and task prompts for information agent."""
    return {
        "system": INFO_AGENT_SYSTEM,
        "task": INFO_AGENT_TASK.format(document_text=document_text)
    }
