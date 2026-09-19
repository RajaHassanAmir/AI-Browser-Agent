import asyncio
import requests
from dotenv import load_dotenv
from browser_use import Agent, ChatGoogle, Browser

load_dotenv()
WEBHOOK_URL = "Your Webhook URL if u want to connect it to your workflow for notifications."
INTERVAL_SECONDS = 86400  # Runs every 24 hours

async def run_agent_job():
    browser = Browser(headless=True)
    llm = ChatGoogle(model="gemini-3.5-flash-lite")
    
    task = (
        "Go to https://lms.umt.edu.pk/login/index.php"
        "Log in with following Credentials Username:'f2024376495' and password:'Year2019#'"
        "Click on Dashboard and see in the timeline section if there are any Activites that require action."
    )
    
    agent = Agent(
        task=task, 
        llm=llm,
        browser=browser,
        use_vision=False,
    )
    
    try:
        history = await agent.run()
        result_text = history.final_result()
        
        print(f"\n=== AGENT RESULT ===\n{result_text}")

        if result_text:
            payload = {
                "source": "Hacker News Browser Agent",
                "search_query": "Python",
                "summary": result_text
            }
            response = requests.post(WEBHOOK_URL, json=payload)
            print(f"✅ Webhook sent! Status Code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error during agent execution: {e}")
    finally:
        await browser.close()

async def main():
    print("🔄 Browser Agent Scheduler started. Running tasks daily...")
    while True:
        print(f"\n--- Starting scheduled run ---")
        await run_agent_job()
        print(f"⏳ Sleeping for 24 hours until the next run...")
        await asyncio.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())
