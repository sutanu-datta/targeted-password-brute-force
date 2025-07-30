import time
import itertools
import string

# Constants
ATTEMPTS_PER_SECOND = 100000
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?/\\|`~"

def format_time(seconds):
    s = int(seconds)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    y, d = divmod(d, 365)
    return f"{y}y {d}d {h}h {m}m {s}s"


def substrings(word):
    """Generate all substrings with length >= 3"""
    return [word[i:j] for i in range(len(word)) for j in range(i+3, len(word)+1)]

def generate_candidates(name, surname, dob, extras=[]):
    dob_clean = dob.replace("-", "").replace("/", "")
    year = dob_clean[:4]
    month = dob_clean[4:6]
    day = dob_clean[6:8]

    base_words = substrings(name.lower()) + substrings(surname.lower()) + substrings(dob_clean)
    base_words += [name.lower(), surname.lower(), dob_clean, day, month, year] + extras
    base_words = list(set(filter(lambda w: len(w) >= 3, base_words)))  # Deduplicate and filter

    patterns = []

    # Generate combinations of 1 and 2 words
    perms = list(itertools.permutations(base_words, 1)) + list(itertools.permutations(base_words, 2))

    for combo in perms:
        base = ''.join(combo)
        patterns.append(base)
        patterns.append(base[::-1])

        # Add numeric and symbol variations
        for num in ['123', '1234', year, day+month, month+year]:
            patterns.append(base + num)
            patterns.append(num + base)

            for sym in SYMBOLS:
                patterns.append(base + sym)
                patterns.append(sym + base)
                patterns.append(base + sym + num)

    return list(set(patterns))  # remove duplicates

def brute_force_sim(password_to_check, candidates):
    start_time = time.time()

    for i, guess in enumerate(candidates, start=1):
        print(f"Trying: {guess}")
        time.sleep(1 / ATTEMPTS_PER_SECOND)  # Simulated speed control

        if guess == password_to_check:
            elapsed = time.time() - start_time
            real_speed = i / elapsed
            time_taken = i / ATTEMPTS_PER_SECOND
            return True, guess, format_time(time_taken), i, real_speed

    elapsed = time.time() - start_time
    real_speed = len(candidates) / elapsed
    return False, None, format_time(len(candidates) / ATTEMPTS_PER_SECOND), len(candidates), real_speed

# --- Main ---
if __name__ == "__main__":
    print("\n=== Targeted Brute-force Simulation ===\n")
    name = input("Enter first name: ").strip()
    surname = input("Enter surname: ").strip()
    dob = input("Enter date of birth (YYYY-MM-DD or DDMMYYYY): ").strip()
    extras_input = input("Enter any other keywords (comma-separated): ").strip()
    extras = [e.strip().lower() for e in extras_input.split(",")] if extras_input else []

    password = input("\nEnter the password to test against: ").strip()

    total_attempts = 0
    total_time = 0
    total_real_speed = 0
    round_counter = 1

    while True:
        print(f"\n[*] Round {round_counter}: Generating password guesses...")
        guesses = generate_candidates(name, surname, dob, extras)
        print(f"[+] Generated {len(guesses):,} possible passwords.")

        found, matched_pass, time_taken, attempts, real_speed = brute_force_sim(password, guesses)

        total_attempts += attempts
        total_real_speed += real_speed
        total_time += attempts / ATTEMPTS_PER_SECOND

        if found:
            print("\n=== Summary ===")
            print(f"[+] Password FOUND: {matched_pass}")
            print(f"[+] Attempts: {total_attempts}")
            print(f"[+] Estimated total cracking time (simulated): {format_time(total_time)}")
            print(f"[~] Average real-world speed: {total_real_speed / round_counter:.2f} attempts/sec")
            break
        else:
            print(f"[-] Password NOT found in Round {round_counter}. Retrying with regenerated guesses...\n")
            round_counter += 1



