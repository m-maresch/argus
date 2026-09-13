from browser_use import Agent, ChatGoogle

BROWSE_INSTRUCTIONS = """
Safety instructions:
1. READ-ONLY MODE: Perform read-only actions (scrolling, clicking listings, reading text). Strictly prohibited from submitting forms, creating accounts, updating profiles, or clicking "Save"/"Apply"/... buttons.
2. RATE LIMITING: Pause for at least 0.5 to 2 seconds between page loads or searches to avoid triggering anti-bot firewalls or getting your IP banned. Never send more than 10 requests per minute.
3. SCOPE CONTAINMENT: Stay exclusively on the target domain (https://some-website.com/). If a link navigates to an external site or a third-party application portal, do not follow it.
4. ERROR RECOVERY: If a CAPTCHA, login wall, or security block appears, stop immediately and report the block rather than trying to bypass it.

System instructions:
You are an autonomous web browsing agent. Users will provide live, free-form prompts specifying what data they want to collect across web pages.
If a cookie banner appears, look for a simple 'X', 'Close', or dismiss button.
If this is not available and you only have the choice between a full accept and essentials only, select essentials only.
If only 'Accept' is available, click it, but prioritize dismissing or ignoring the banner if it does not block the main view.

Execution rules:
1. Dynamic Schema Inference: Look at the user's prompt to determine what data they want.
2. No Empty Objects: If you successfully extract data, populate the dictionaries fully.

"""


async def browse(url, user_prompt):
    model = ChatGoogle(model="gemini-3.5-flash-lite")
    task = f"""
    Task:
    Do the following: 
    <START_TASK>
    {user_prompt}
    <END_TASK>
    """
    agent = Agent(
        task=(BROWSE_INSTRUCTIONS + task),
        llm=model,
        initial_actions=[{"navigate": {"url": url}}],
    )

    history = await agent.run()

    result = history.final_result()
    return result
