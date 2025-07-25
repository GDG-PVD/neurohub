"""
Research Agent - Functional example using FutureHouse API
Demonstrates how to build agents that integrate with real scientific research APIs
"""

import os
import asyncio
import json
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass

from core.a2a_client import A2AAgent, A2ATask
from integrations.omi_connector import OMIMemory

# FutureHouse client wrapper
class FutureHouseClient:
    """Client for FutureHouse research platform"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.futurehouse.org/v1"
        
    async def run_task(self, task_data: dict) -> dict:
        """Run a FutureHouse task (CROW, FALCON, OWL, PHOENIX)"""
        # In production: Make actual API call
        # For workshop: Simulated response
        import aiohttp
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Simulated response for demonstration
        if not self.api_key or self.api_key == "demo":
            return self._get_demo_response(task_data)
        
        # Real API call
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/tasks",
                json=task_data,
                headers=headers
            ) as response:
                return await response.json()
    
    def _get_demo_response(self, task_data: dict) -> dict:
        """Demo responses for workshop"""
        query = task_data.get("query", "")
        
        if "AI" in query or "artificial intelligence" in query:
            return {
                "status": "completed",
                "result": {
                    "answer": "Recent AI developments in neuroscience include:\n"
                             "1. DeepMind's protein folding predictions for neurodegenerative diseases\n"
                             "2. ML models detecting Alzheimer's from speech patterns\n"
                             "3. AI-assisted drug discovery for Parkinson's",
                    "citations": [
                        {"title": "AlphaFold and neurodegeneration", "year": 2023},
                        {"title": "Speech biomarkers in AD", "year": 2024}
                    ]
                }
            }
        
        return {
            "status": "completed",
            "result": {
                "answer": f"Research findings for: {query}",
                "citations": []
            }
        }


@dataclass
class ResearchQuery:
    """Structured research query extracted from conversation"""
    question: str
    context: str
    priority: str = "medium"
    research_type: str = "CROW"  # CROW, FALCON, OWL, PHOENIX


class ScientificResearchAgent(A2AAgent):
    """
    Agent that extracts research questions from OMI conversations
    and uses FutureHouse to find scientific answers
    """
    
    def __init__(self):
        super().__init__(
            name="scientific-research-agent",
            capabilities=[
                "extract_research_questions",
                "search_literature", 
                "synthesize_findings",
                "track_citations"
            ]
        )
        
        # Initialize FutureHouse client
        api_key = os.getenv("FUTUREHOUSE_API_KEY", "demo")
        self.fh_client = FutureHouseClient(api_key)
        
        # Track research history
        self.research_history = []
        
    async def process_task(self, task: A2ATask) -> dict:
        """Process incoming research tasks"""
        
        if task.type == "analyze_conversation":
            return await self.analyze_research_conversation(task.data)
        elif task.type == "deep_research":
            return await self.conduct_deep_research(task.data)
        elif task.type == "find_precedent":
            return await self.find_scientific_precedent(task.data)
        else:
            return {"error": f"Unknown task type: {task.type}"}
    
    async def analyze_research_conversation(self, data: dict) -> dict:
        """Extract and research questions from OMI conversation"""
        
        transcript = data.get("transcript", "")
        
        # Step 1: Extract research questions
        questions = self.extract_research_questions(transcript)
        
        # Step 2: Research each question
        research_results = []
        for query in questions:
            result = await self.research_question(query)
            research_results.append(result)
        
        # Step 3: Synthesize findings
        synthesis = self.synthesize_findings(questions, research_results)
        
        # Store in history
        self.research_history.append({
            "timestamp": datetime.now().isoformat(),
            "questions": [q.question for q in questions],
            "synthesis": synthesis
        })
        
        return {
            "status": "success",
            "questions_found": len(questions),
            "research_results": research_results,
            "synthesis": synthesis,
            "next_steps": self.suggest_next_steps(synthesis)
        }
    
    def extract_research_questions(self, transcript: str) -> List[ResearchQuery]:
        """Extract research questions from conversation"""
        
        questions = []
        
        # Simple extraction logic - in production use NLP
        question_indicators = [
            "i wonder", "what if", "how does", "why does", 
            "could we", "is it possible", "what about"
        ]
        
        sentences = transcript.lower().split('.')
        for sentence in sentences:
            for indicator in question_indicators:
                if indicator in sentence:
                    questions.append(ResearchQuery(
                        question=sentence.strip(),
                        context=transcript[:100],  # Include some context
                        research_type="CROW"  # Quick search by default
                    ))
                    break
        
        # Also look for explicit research requests
        if "research" in transcript.lower() or "look up" in transcript.lower():
            # Extract the specific topic
            words = transcript.split()
            for i, word in enumerate(words):
                if word.lower() in ["research", "investigate", "explore"]:
                    topic = " ".join(words[i+1:i+6])  # Next 5 words
                    questions.append(ResearchQuery(
                        question=f"What is the latest research on {topic}?",
                        context=transcript[:100],
                        priority="high",
                        research_type="CROW"
                    ))
        
        return questions
    
    async def research_question(self, query: ResearchQuery) -> dict:
        """Research a single question using FutureHouse"""
        
        # Choose appropriate FutureHouse agent
        fh_task = {
            "name": query.research_type,
            "query": query.question,
            "context": query.context
        }
        
        # Call FutureHouse API
        result = await self.fh_client.run_task(fh_task)
        
        return {
            "question": query.question,
            "answer": result.get("result", {}).get("answer", "No results found"),
            "citations": result.get("result", {}).get("citations", []),
            "confidence": result.get("confidence", 0.8)
        }
    
    async def conduct_deep_research(self, data: dict) -> dict:
        """Use FALCON for comprehensive research"""
        
        topic = data.get("topic", "")
        
        fh_task = {
            "name": "FALCON",
            "query": f"Comprehensive review of {topic}",
            "max_sources": 50
        }
        
        result = await self.fh_client.run_task(fh_task)
        
        return {
            "status": "success",
            "topic": topic,
            "report": result.get("result", {}).get("report", ""),
            "num_sources": len(result.get("result", {}).get("citations", []))
        }
    
    async def find_scientific_precedent(self, data: dict) -> dict:
        """Use OWL to check if something has been done before"""
        
        idea = data.get("idea", "")
        
        fh_task = {
            "name": "OWL",
            "query": idea
        }
        
        result = await self.fh_client.run_task(fh_task)
        
        return {
            "status": "success",
            "idea": idea,
            "precedents": result.get("result", {}).get("precedents", []),
            "novelty_assessment": result.get("result", {}).get("assessment", "")
        }
    
    def synthesize_findings(self, questions: List[ResearchQuery], 
                          results: List[dict]) -> str:
        """Synthesize research results into actionable insights"""
        
        if not results:
            return "No research results to synthesize."
        
        synthesis = "Research Summary:\n\n"
        
        # Group by topic
        key_findings = []
        citations_count = 0
        
        for i, result in enumerate(results):
            if result.get("answer") and result["answer"] != "No results found":
                key_findings.append(f"- {result['answer'][:200]}...")
                citations_count += len(result.get("citations", []))
        
        synthesis += f"Found {len(key_findings)} relevant insights "
        synthesis += f"backed by {citations_count} citations.\n\n"
        synthesis += "Key Findings:\n" + "\n".join(key_findings)
        
        return synthesis
    
    def suggest_next_steps(self, synthesis: str) -> List[str]:
        """Suggest follow-up actions based on research"""
        
        suggestions = []
        
        # Analyze synthesis for patterns
        if "protein" in synthesis.lower():
            suggestions.append("Consider using PHOENIX for molecular analysis")
        
        if "clinical trial" in synthesis.lower():
            suggestions.append("Search ClinicalTrials.gov for active studies")
        
        if len(self.research_history) > 3:
            suggestions.append("Review research history for emerging patterns")
        
        # Always suggest deeper dive
        suggestions.append("Use FALCON for comprehensive literature review")
        
        return suggestions


# Example usage for workshop
async def demo_research_agent():
    """Demonstrate the research agent with sample conversation"""
    
    agent = ScientificResearchAgent()
    
    # Sample conversation from OMI device
    sample_conversation = """
    I've been thinking about how AI could help with early detection of 
    neurodegenerative diseases. I wonder if machine learning models could 
    analyze speech patterns to detect early signs? What about using 
    protein folding predictions? We should research the latest developments 
    in AI for Alzheimer's detection.
    """
    
    # Create task
    task = A2ATask(
        id="demo-1",
        type="analyze_conversation",
        data={"transcript": sample_conversation}
    )
    
    # Process task
    print("🔬 Scientific Research Agent Demo\n")
    print(f"Analyzing conversation:\n{sample_conversation}\n")
    print("Processing...\n")
    
    result = await agent.process_task(task)
    
    # Display results
    print(f"✅ Found {result['questions_found']} research questions\n")
    
    for i, research in enumerate(result['research_results']):
        print(f"Question {i+1}: {research['question']}")
        print(f"Answer: {research['answer'][:200]}...")
        print(f"Citations: {len(research['citations'])} sources")
        print()
    
    print("📊 Synthesis:")
    print(result['synthesis'])
    print()
    
    print("🚀 Suggested Next Steps:")
    for step in result['next_steps']:
        print(f"  - {step}")


if __name__ == "__main__":
    # Run the demo
    asyncio.run(demo_research_agent())