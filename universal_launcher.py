# universal_launcher.py
import webbrowser
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai  # Gemini AI
import os

# ============ SETUP GEMINI API ============
# Replace with your Gemini API key
GENAI_API_KEY = "AIzaSyDzDD7V-GzDBqQDjpgY0RJnkko7ZlkkkRY"
genai.configure(api_key=GENAI_API_KEY)

# ============ TEXT-TO-SPEECH ENGINE ============
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # speaking speed
engine.setProperty("volume", 1.0)  # max volume

# ============ PLATFORM DETECTION ============
PLATFORM_KEYWORDS = {
    "youtube": ["youtube", "video"],
    "linkedin": ["linkedin", "profile", "professional"],
    "shopping": ["amazon", "flipkart", "shopping", "buy", "laptop", "phone", "product"],
    "twitter": ["twitter", "tweet"],
    "github": ["github", "repository", "code", "repo"],
    "fun": ["joke", "fun", "quote", "story"],
    "google": []  # fallback
}

PLATFORM_URLS = {
    "youtube": "https://www.youtube.com/results?search_query={query}",
    "linkedin": "https://www.linkedin.com/search/results/people/?keywords={query}",
    "shopping_amazon": "https://www.amazon.in/s?k={query}",
    "shopping_flipkart": "https://www.flipkart.com/search?q={query}",
    "twitter": "https://twitter.com/search?q={query}",
    "github": "https://github.com/search?q={query}",
    "google": "https://www.google.com/search?q={query}"
}

# ============ PLATFORM DETECTION ============
def detect_platform(command):
    command_lower = command.lower()
    for platform, keywords in PLATFORM_KEYWORDS.items():
        for keyword in keywords:
            if keyword in command_lower:
                return platform
    return "google"

# ============ SMART CATEGORIZATION ============
def smart_categorization(command, platform):
    if platform == "shopping":
        print("\n🛒 Your query looks like shopping-related.")
        engine.say("Your query looks like shopping-related. Where should I search?")
        engine.runAndWait()
        print("1. Amazon\n2. Flipkart\n3. Google")
        choice = input("Enter 1/2/3: ").strip()
        if choice == "1":
            return "shopping_amazon"
        elif choice == "2":
            return "shopping_flipkart"
        else:
            return "google"
    return platform

# ============ BUILD SEARCH URL ============
def get_search_url(command):
    query = command.replace(" ", "+")
    platform = detect_platform(command)
    platform = smart_categorization(command, platform)
    return PLATFORM_URLS.get(platform, PLATFORM_URLS["google"]).format(query=query)

# ============ AI SUMMARY ============
def ai_summary(command):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Give a very short one-line response for this query: '{command}'"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "Opening the best result for you..."

# ============ FUN RESPONSES ============
FUN_RESPONSES = [
    "Why don’t scientists trust atoms? Because they make up everything!",
    "I told my computer I needed a break, and it said 'No problem, I’ll go to sleep.'",
    "Why did the scarecrow win an award? Because he was outstanding in his field!"
]

def fun_response():
    import random
    joke = random.choice(FUN_RESPONSES)
    print(f"🤖 Fun: {joke}")
    engine.say(joke)
    engine.runAndWait()

# ============ VOICE INPUT ============
def listen_to_voice():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("\n🎤 Speak now... (say 'exit' to quit)")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"🗣 You said: {command}")
        return command
    except sr.UnknownValueError:
        print("❌ Sorry, I could not understand your voice. Please try again.")
        engine.say("Sorry, I could not understand your voice. Please try again.")
        engine.runAndWait()
        return None
    except sr.RequestError:
        print("⚠️ Could not request results from Google Speech Recognition service.")
        engine.say("Could not request results from Google Speech Recognition service.")
        engine.runAndWait()
        return None

# ============ MAIN LOOP ============
def main():
    while True:
        print("\nChoose input method:")
        print("1. Type your command")
        print("2. Speak your command")
        choice = input("Enter 1 or 2 (or 'exit' to quit): ").strip()

        if choice.lower() == "exit":
            print("Exiting launcher...")
            engine.say("Exiting launcher. Goodbye!")
            engine.runAndWait()
            break

        if choice == "1":
            user_command = input("Enter your command: ").strip()
        elif choice == "2":
            user_command = listen_to_voice()
            if not user_command:
                continue
        else:
            print("Invalid choice. Please select 1 or 2.")
            engine.say("Invalid choice. Please select 1 or 2.")
            engine.runAndWait()
            continue

        if user_command.lower() == "exit":
            print("Exiting launcher...")
            engine.say("Exiting launcher. Goodbye!")
            engine.runAndWait()
            break

        # ============ CONFIRMATION BEFORE OPENING ============
        confirm_text = f"Yes! I am opening your command: {user_command}"
        print(f"🤖 AI Assistant: {confirm_text}")
        engine.say(confirm_text)
        engine.runAndWait()

        # AI summary (optional)
        summary = ai_summary(user_command)
        if summary:
            print(f"🤖 AI Summary: {summary}")
            engine.say(f"AI says: {summary}")
            engine.runAndWait()

        # Fun commands
        if detect_platform(user_command) == "fun":
            fun_response()
            continue

        # Open website
        search_url = get_search_url(user_command)
        engine.say("Opening the website for you.")
        engine.runAndWait()
        print(f"🌐 Opening: {search_url}")
        webbrowser.open(search_url)

if __name__ == "__main__":
    main() 
