import random
import speech_recognition as sr
import difflib

# Dictionary of phrases similar to "unlock the door"
unlock_phrases = {
    "physical actions": [
        "open the door", "unfasten the door", "disengage the lock",
        "release the latch", "unbolt the door", "unseal the door"
    ],
    "requests or commands": [
        "let me in", "grant access", "allow entry", 
        "permit entrance", "give access to the room"
    ],
    "metaphorical expressions": [
        "clear the way", "remove the barrier", "open up the path", 
        "break the seal", "lift the restriction"
    ],
    "technology-related": [
        "unlock the system", "disable security", "grant permission", 
        "release access", "deactivate the lock"
    ]
}

# Predefined list of human-readable phrases for verification
verification_phrases = [
    "The quick brown fox jumps over the lazy dog",
    "Unlock the treasure chest",
    "Security is the key to success",
    "Safe and sound",
    "Open sesame",
    "Welcome to the future",
    "Your access has been granted",
    "The door opens wide"
]

# Maximum attempts for verification
max_attempts = 3

# Initialize recognizer for voice input
recognizer = sr.Recognizer()

# Function to capture voice commands with timeout and noise adjustment
def capture_voice_command():
    with sr.Microphone() as source:
        print("Listening for your command...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)  # Timeout added
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for command.")
            return None
        except sr.UnknownValueError:
            print("Sorry, I did not understand your command.")
            return None
        except sr.RequestError as e:
            print(f"Error: {e}")
            return None

# Function to generate a random human-readable phrase
def generate_random_phrase():
    return random.choice(verification_phrases)

# Function to capture voice verification (saying the phrase)
def capture_voice_verification():
    with sr.Microphone() as source:
        print("Please say the phrase...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)  # Timeout added
            verification = recognizer.recognize_google(audio).upper()
            print(f"You said: {verification}")
            return verification
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for verification.")
            return None
        except sr.UnknownValueError:
            print("Sorry, I did not understand.")
            return None
        except sr.RequestError as e:
            print(f"Error: {e}")
            return None

# Function to capture text input for phrase verification
def capture_text_verification():
    verification = input("Please type the phrase: ").upper()
    return verification

# Function to check if the command matches any phrase in the unlock_phrases dictionary using fuzzy matching
def is_unlock_command(command):
    threshold = 0.6  # Similarity threshold (60%)
    for category, phrases in unlock_phrases.items():
        for phrase in phrases:
            similarity = difflib.SequenceMatcher(None, phrase, command).ratio()
            if similarity >= threshold:  # Match if similarity is above the threshold
                return True
    return False

# Function to simulate unlocking the door
def unlock_door():
    print("The door is unlocked. Welcome!")

# Function to set the user's own phrase with a renewal period and ensure valid input
def set_custom_phrase():
    renewal_periods = {1: 3, 2: 5, 3: 7, 4: 15, 5: 30}
    
    while True:  # Loop until valid phrase is confirmed
        method = input("Do you want to set the custom phrase by typing or by voice? (type/voice): ").lower()

        if method == "voice":
            print("Listening for your custom phrase...")
            phrase = capture_voice_command()
            if phrase is None:  # Handle case where no valid phrase was captured
                print("Sorry, could not capture your phrase. Let's try again.")
                continue
            phrase = phrase.upper()
        elif method == "type":
            phrase = input("Please type your custom phrase: ").upper()
        else:
            print("Invalid method chosen. Please choose 'type' or 'voice'.")
            continue

        if not phrase.strip():
            print("The phrase cannot be empty. Please try again.")
            continue
        
        print(f"Your phrase is: '{phrase}'")
        confirmation = input("Is this correct? (yes/no): ").lower()
        if confirmation == 'yes':
            print("Select the renewal period: ")
            print("1. 3 days\n2. 5 days\n3. 7 days (recommended)\n4. 15 days\n5. 30 days")
            
            period_choice = int(input("Please choose a renewal period (1-5): "))
            renewal_days = renewal_periods.get(period_choice, 7)  # Default to 7 days if input is invalid
            print(f"Phrase '{phrase}' is set and will renew after {renewal_days} days.")
            return phrase
        else:
            print("Let's try again to set your custom phrase.")

# Main function to handle the authorization process
def authorize_user():
    # Ask user if they want to set their own phrase or use a random one
    choice = input("Do you want to set your own phrase or use a random one? (custom/random): ").lower()
    
    if choice == 'custom':
        custom_phrase = set_custom_phrase()
        if custom_phrase:
            for attempt in range(max_attempts):
                print("Please say or type the custom phrase.")
                method = input("Do you want to verify the phrase by typing or by voice? (type/voice): ").lower()
                
                if method == "voice":
                    user_input = capture_voice_verification()
                elif method == "type":
                    user_input = capture_text_verification()
                else:
                    print("Invalid method chosen.")
                    return
                
                if user_input == custom_phrase:
                    unlock_door()
                    return
                else:
                    print(f"Incorrect phrase. Attempts remaining: {max_attempts - attempt - 1}")
        else:
            print("Error setting custom phrase.")
            return

    elif choice == 'random':
        random_phrase = generate_random_phrase()
        print(f"Generated random phrase: '{random_phrase}'")
        print(f"Please say or type this phrase: '{random_phrase}'")
        
        for attempt in range(max_attempts):
            method = input("Do you want to verify the phrase by typing or by voice? (type/voice): ").lower()

            if method == "voice":
                user_input = capture_voice_verification()
            elif method == "type":
                user_input = capture_text_verification()
            else:
                print("Invalid method chosen.")
                return
            
            if user_input == random_phrase.upper():
                unlock_door()
                return
            else:
                print(f"Incorrect phrase. Attempts remaining: {max_attempts - attempt - 1}")
        
    else:
        print("Invalid choice.")
        return

    print("Maximum attempts reached. Access denied.")

# Run the program
if __name__ == "__main__":
    authorize_user()
