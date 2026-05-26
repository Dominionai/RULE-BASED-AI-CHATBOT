# =============================================================================
# DecodeLabs | Batch 2026 | Project 1: Rule-Based AI Chatbot
# File: chatbot.py — The Logic Engine (Core Brain)
# Architecture: IPO Model + Dictionary O(1) Lookup
# =============================================================================

import random
import datetime


# =============================================================================
# PHASE 1: KNOWLEDGE BASE — The Dictionary (O(1) Lookup, NOT if-elif ladder)
# Each key maps to a list of responses for variety
# =============================================================================

KNOWLEDGE_BASE = {
    # --- Greetings ---
    "hello":        ["Hello! Welcome to RuleBot. How can I assist you today?",
                     "Hey there! I'm RuleBot, your rule-based assistant. What's on your mind?",
                     "Hi! Great to see you. How can I help?"],

    "hi":           ["Hi! How can I help you today?",
                     "Hello! RuleBot at your service.",
                     "Hey! What can I do for you?"],

    "hey":          ["Hey! What's up? How can I assist?",
                     "Hey there! RuleBot is listening."],

    "good morning": ["Good morning! Hope you have a productive day ahead!",
                     "Good morning! Let's get started — how can I help?"],

    "good afternoon":["Good afternoon! Hope your day is going well.",
                      "Good afternoon! How can I assist you?"],

    "good evening": ["Good evening! How can I help you tonight?",
                     "Good evening! What brings you here?"],

    # --- Identity ---
    "what is your name": ["I'm RuleBot — a rule-based AI chatbot built at DecodeLabs!",
                          "My name is RuleBot. I operate purely on programmatic logic."],

    "who are you":   ["I am RuleBot, an AI chatbot powered by deterministic if-else logic.",
                      "I'm RuleBot! A project built as part of the DecodeLabs AI Training Kit."],

    "who made you":  ["I was built by an AI Engineer intern at DecodeLabs, Batch 2026!",
                      "A DecodeLabs intern created me as Project 1 of the AI Training Kit."],

    "how old are you": ["I was born the moment this code ran for the first time!",
                        "Age is just a number. I live in the present moment of your session."],

    # --- Status ---
    "how are you":   ["I'm functioning perfectly — all rules are firing correctly!",
                      "All systems operational! No bugs detected today.",
                      "I'm great! My logic engine is running at 100%."],

    "are you ok":    ["Yes! All my conditions are evaluating correctly.",
                      "Absolutely fine — zero exceptions raised!"],

    # --- Capabilities ---
    "what can you do": ["I can:\n  • Respond to greetings\n  • Answer questions about myself\n  • Tell jokes\n  • Share motivational quotes\n  • Give the current time & date\n  • Discuss AI concepts\n  • Say goodbye!\n\nAll powered by pure dictionary lookup — no ML needed!",
                        "I handle greetings, identity questions, jokes, time/date, motivation, and farewells using rule-based logic!"],

    "help":          ["Here are things you can ask me:\n  • hello / hi / hey\n  • how are you\n  • what is your name\n  • tell me a joke\n  • motivate me\n  • what time is it\n  • what is AI\n  • bye"],

    # --- Jokes ---
    "tell me a joke": ["Why do programmers prefer dark mode?\nBecause light attracts bugs! 🐛",
                       "Why did the chatbot break up with the database?\nIt found someone more relational.",
                       "How many programmers does it take to change a lightbulb?\nNone — that's a hardware problem!",
                       "I would tell you a joke about UDP... but you might not get it.",
                       "Why do Python programmers wear glasses?\nBecause they can't C!"],

    "joke":          ["A SQL query walks into a bar, walks up to two tables and asks...\n'Can I join you?'",
                      "Why was the developer sad?\nBecause they used to C++ but now they only C.",
                      "Debugging is like being the detective in a crime movie where you're also the murderer."],

    # --- Motivation ---
    "motivate me":   ["Every expert was once a beginner. Keep coding! 💪",
                      "The best way to predict the future is to build it — one rule at a time!",
                      "You're doing amazing. One commit at a time, you're becoming an AI engineer!"],

    "i feel sad":    ["It's okay to feel that way. Remember: every great engineer faced obstacles.",
                      "Keep going. The fact that you're here, learning, means you're already ahead."],

    "inspire me":    ["An LLM without rules is a hallucination engine.\nYou are building the skeleton that holds intelligence together.",
                      "Code is poetry. Every function you write is a verse in the story of AI."],

    # --- AI Concepts (from the PDF) ---
    "what is ai":    ["AI is the simulation of human intelligence by machines.\nIt comes in two forms:\n  • Rule-Based (Deterministic) — what I am!\n  • Machine Learning (Probabilistic) — what comes next in your training."],

    "what is rule based ai": ["Rule-based AI uses explicit if-else logic to make decisions.\nIt's a 'white box' — fully transparent, traceable, and zero hallucination risk!\nPerfect for compliance in Finance & Healthcare."],

    "what is machine learning": ["Machine Learning is when a system learns patterns from data automatically.\nUnlike me, it doesn't need explicit rules — it discovers them on its own.\nBut first, you must master rules like me before ML!"],

    "what is ipo model": ["IPO stands for Input → Process → Output.\nIt's the blueprint for this chatbot:\n  • Input: Sanitize your raw text (lower + strip)\n  • Process: Match intent via dictionary lookup\n  • Output: Return the matched response or fallback"],

    "what is a dictionary": ["In Python, a dictionary is a hash map — key:value pairs.\nLookup time is O(1) — instant, regardless of size.\nThat's why we use it instead of an if-elif ladder!"],

    "what is o1":    ["O(1) means constant time complexity.\nNo matter how many rules exist, the lookup takes the same time.\nA dictionary gives us O(1). An if-elif chain gives us O(n) — much slower!"],

    # --- Time & Date ---
    "what time is it": ["__TIME__"],
    "current time":    ["__TIME__"],
    "what is today":   ["__DATE__"],
    "what is the date":["__DATE__"],
    "today date":      ["__DATE__"],

    # --- Gratitude ---
    "thank you":     ["You're very welcome! 😊",
                      "Happy to help anytime!",
                      "My pleasure — that's what rules are for!"],

    "thanks":        ["Anytime! Come back if you need help.",
                      "You're welcome!"],

    # --- Farewell (Exit Commands) ---
    "bye":           ["__EXIT__"],
    "goodbye":       ["__EXIT__"],
    "exit":          ["__EXIT__"],
    "quit":          ["__EXIT__"],
    "see you":       ["__EXIT__"],
    "farewell":      ["__EXIT__"],
}

EXIT_MESSAGES = [
    "Goodbye! It was great chatting with you. Come back anytime! 👋",
    "See you later! Remember — rules make the world go round!",
    "Farewell! Keep building, keep learning. You're on your way to becoming an AI engineer!",
]

FALLBACK_RESPONSES = [
    "I don't have a rule for that yet! Try asking: hello, joke, help, time, or bye.",
    "Hmm, that input doesn't match any of my rules. Type 'help' to see what I can do!",
    "I'm still learning new rules. Try 'help' to see my current capabilities.",
]


# =============================================================================
# PHASE 2: INPUT SANITIZATION — Handle case & whitespace (IPO Phase 1)
# =============================================================================

def sanitize_input(raw_input: str) -> str:
    """
    Sanitize raw user input.
    - Converts to lowercase (so 'Hello', 'HELLO', 'hello' all match)
    - Strips leading/trailing whitespace
    """
    return raw_input.lower().strip()


# =============================================================================
# PHASE 3: INTENT MATCHING ENGINE — Dictionary O(1) Lookup (IPO Phase 2)
# =============================================================================

def get_response(clean_input: str) -> tuple[str, bool]:
    """
    Match user input to knowledge base and return response.
    Uses dictionary .get() — O(1) lookup + fallback in a single atomic operation.

    Returns:
        (response_text: str, is_exit: bool)
    """

    # Search for keyword match in knowledge base
    matched_responses = None
    for keyword in KNOWLEDGE_BASE:
        if keyword in clean_input:
            matched_responses = KNOWLEDGE_BASE[keyword]
            break

    # If no match found, use fallback (O(1) .get() pattern)
    if matched_responses is None:
        return random.choice(FALLBACK_RESPONSES), False

    # Pick a random response from matched list (adds personality variety)
    response = random.choice(matched_responses)

    # Handle special dynamic responses
    if response == "__EXIT__":
        return random.choice(EXIT_MESSAGES), True

    if response == "__TIME__":
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}.", False

    if response == "__DATE__":
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {today}.", False

    return response, False


# =============================================================================
# PHASE 4: THE HEARTBEAT — Infinite Loop (Terminal Mode)
# =============================================================================

def run_terminal_chatbot():
    """
    Run the chatbot in terminal mode.
    Continuous while True loop — the 'heartbeat' of the system.
    Exits cleanly on kill command (bye/exit/quit).
    """
    print("=" * 60)
    print("  DecodeLabs | RuleBot — Rule-Based AI Chatbot")
    print("  Project 1 | Batch 2026")
    print("  Type 'help' for commands | Type 'bye' to exit")
    print("=" * 60)
    print("\nRuleBot: Hello! I'm RuleBot. How can I help you today?\n")

    while True:
        # PHASE 1: Input
        raw = input("You: ")

        if not raw.strip():
            print("RuleBot: Please type something!\n")
            continue

        # PHASE 2: Sanitize
        clean = sanitize_input(raw)

        # PHASE 3: Process & Match
        response, is_exit = get_response(clean)

        # PHASE 4: Output
        print(f"\nRuleBot: {response}\n")

        # EXIT STRATEGY — clean break command
        if is_exit:
            break

    print("\n" + "=" * 60)
    print("  Session ended. Thank you for using RuleBot!")
    print("=" * 60)


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    run_terminal_chatbot()
