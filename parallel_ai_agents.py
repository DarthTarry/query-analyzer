import concurrent.futures
import os
from datetime import datetime
import json

# -----------------------------------------
# Configuration - Add your API keys here
# -----------------------------------------

API_KEYS = {
    "openai": os.getenv("OPENAI_API_KEY", "your_openai_api_key_here"),
    "google": os.getenv("GOOGLE_API_KEY", "your_google_api_key_here"),
    "anthropic": os.getenv("ANTHROPIC_API_KEY", "your_anthropic_api_key_here"),
    "groq": os.getenv("GROQ_API_KEY", "your_groq_api_key_here"),
}

# -----------------------------------------
# AI Agent Classes
# -----------------------------------------

class AIAgent:
    """Base class for AI agents"""
    def __init__(self, name, api_key):
        self.name = name
        self.api_key = api_key
        self.response = None
        self.error = None
        self.timestamp = None

    def query(self, prompt):
        """Query the AI agent - to be implemented by subclasses"""
        raise NotImplementedError

    def format_response(self):
        """Return formatted response"""
        if self.error:
            return f"Error: {self.error}"
        return self.response if self.response else "No response"


class ChatGPTAgent(AIAgent):
    """OpenAI ChatGPT Agent"""
    def query(self, prompt):
        try:
            self.timestamp = datetime.now()
            # Uncomment this block when you have OpenAI API key
            # import openai
            # openai.api_key = self.api_key
            # response = openai.ChatCompletion.create(
            #     model="gpt-4",
            #     messages=[{"role": "user", "content": prompt}]
            # )
            # self.response = response.choices[0].message.content
            
            # Placeholder for demo
            self.response = f"[ChatGPT] Response to: {prompt[:50]}..."
        except Exception as e:
            self.error = str(e)


class GeminiAgent(AIAgent):
    """Google Gemini Agent"""
    def query(self, prompt):
        try:
            self.timestamp = datetime.now()
            # Uncomment this block when you have Google API key
            # import google.generativeai as genai
            # genai.configure(api_key=self.api_key)
            # model = genai.GenerativeModel('gemini-pro')
            # response = model.generate_content(prompt)
            # self.response = response.text
            
            # Placeholder for demo
            self.response = f"[Gemini] Response to: {prompt[:50]}..."
        except Exception as e:
            self.error = str(e)


class ClaudeAgent(AIAgent):
    """Anthropic Claude Agent"""
    def query(self, prompt):
        try:
            self.timestamp = datetime.now()
            # Uncomment this block when you have Anthropic API key
            # from anthropic import Anthropic
            # client = Anthropic(api_key=self.api_key)
            # response = client.messages.create(
            #     model="claude-3-opus-20240229",
            #     max_tokens=1024,
            #     messages=[{"role": "user", "content": prompt}]
            # )
            # self.response = response.content[0].text
            
            # Placeholder for demo
            self.response = f"[Claude] Response to: {prompt[:50]}..."
        except Exception as e:
            self.error = str(e)


class GroqAgent(AIAgent):
    """Groq API Agent"""
    def query(self, prompt):
        try:
            self.timestamp = datetime.now()
            from groq import Groq
            client = Groq(api_key=self.api_key)
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}]
            )
            self.response = response.choices[0].message.content
        except Exception as e:
            self.error = str(e)


# -----------------------------------------
# Parallel Query Manager
# -----------------------------------------

class ParallelAIManager:
    """Manages parallel queries to multiple AI agents"""
    
    def __init__(self):
        self.agents = {
            "ChatGPT": ChatGPTAgent("ChatGPT", API_KEYS["openai"]),
            "Gemini": GeminiAgent("Gemini", API_KEYS["google"]),
            "Claude": ClaudeAgent("Claude", API_KEYS["anthropic"]),
            "Groq": GroqAgent("Groq", API_KEYS["groq"]),
        }
        self.results = {}

    def query_all_agents(self, prompt, timeout=30):
        """Send prompt to all agents in parallel"""
        print(f"\n{'='*70}")
        print(f"Sending prompt to all agents (Timeout: {timeout}s)...")
        print(f"{'='*70}")
        print(f"Prompt: {prompt}\n")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            # Submit all queries
            futures = {
                executor.submit(agent.query, prompt): name 
                for name, agent in self.agents.items()
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(futures, timeout=timeout):
                agent_name = futures[future]
                try:
                    future.result()
                    self.results[agent_name] = {
                        "status": "success",
                        "response": self.agents[agent_name].response,
                        "timestamp": self.agents[agent_name].timestamp.isoformat()
                    }
                except Exception as e:
                    self.results[agent_name] = {
                        "status": "failed",
                        "error": str(e),
                        "timestamp": datetime.now().isoformat()
                    }

    def display_results(self):
        """Display results from all agents"""
        print(f"\n{'='*70}")
        print("RESULTS FROM ALL AGENTS")
        print(f"{'='*70}\n")
        
        for agent_name, result in self.results.items():
            print(f"{'─'*70}")
            print(f"Agent: {agent_name}")
            print(f"Status: {result['status']}")
            print(f"Timestamp: {result['timestamp']}")
            print(f"{'-'*70}")
            
            if result['status'] == 'success':
                print(f"Response:\n{result['response']}")
            else:
                print(f"Error:\n{result.get('error', 'Unknown error')}")
            
            print()

    def save_results_to_file(self, filename="parallel_ai_results.json"):
        """Save results to JSON file"""
        output = {
            "timestamp": datetime.now().isoformat(),
            "results": self.results
        }
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"Results saved to: {filename}")


# -----------------------------------------
# Main execution
# -----------------------------------------

def main():
    import tkinter as tk
    from tkinter import simpledialog, messagebox
    
    # Create a hidden root window
    root = tk.Tk()
    root.withdraw()
    
    # Get prompt from user
    prompt = simpledialog.askstring(
        "Parallel AI Agents",
        "Enter your prompt:\n\n(This will be sent to ChatGPT, Gemini, Claude, and Groq in parallel)"
    )
    
    if not prompt:
        messagebox.showwarning("Input Required", "No prompt provided. Exiting.")
        root.destroy()
        return
    
    root.destroy()
    
    # Create manager and query all agents
    manager = ParallelAIManager()
    
    try:
        manager.query_all_agents(prompt)
    except concurrent.futures.TimeoutError:
        print("⚠️ Timeout: Some agents did not respond within the time limit.")
    
    # Display results
    manager.display_results()
    
    # Save results
    manager.save_results_to_file()
    
    print(f"\n{'='*70}")
    print("✓ All queries completed!")
    print(f"{'='*70}")


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║     Parallel AI Agents Query Script                      ║
    ║     Send prompts to multiple AI services simultaneously   ║
    ║                                                          ║
    ║  Supported Agents:                                       ║
    ║   • ChatGPT (OpenAI)                                     ║
    ║   • Gemini (Google)                                      ║
    ║   • Claude (Anthropic)                                   ║
    ║   • Groq                                                 ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    print("Setup Instructions:")
    print("─" * 60)
    print("1. Install required packages:")
    print("   pip install openai google-generativeai anthropic groq")
    print()
    print("2. Set API keys as environment variables:")
    print("   set OPENAI_API_KEY=your_key")
    print("   set GOOGLE_API_KEY=your_key")
    print("   set ANTHROPIC_API_KEY=your_key")
    print("   set GROQ_API_KEY=your_key")
    print()
    print("3. Uncomment the actual API calls in agent classes")
    print("4. Run the script and enter your prompt")
    print("─" * 60)
    print()
    
    main()
