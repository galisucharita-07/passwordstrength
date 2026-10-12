
import re
import math

from pathlib import Path

COMMON_PASSWORDS_FILE = (
    Path(__file__).resolve().parent / "common_passwords.txt"
)

try:
    COMMON_PASSWORDS = {
        line.strip().casefold()
        for line in COMMON_PASSWORDS_FILE.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
except OSError:
    COMMON_PASSWORDS = {
        "password",
        "password123",
        "123456",
        "12345678",
        "qwerty",
        "admin",
        "letmein",
        "welcome",
        "iloveyou",
        "abc123",
        "123456789",
        "111111",
    }




COMMON_WORDS = {
    "password", "admin", "welcome", "qwerty", "letmein"
}

KEYBOARD_PATTERNS = [
    "qwerty", "asdfgh", "zxcvbn",
    "123456", "654321", "abcdef"
]


def calculate_character_pool(password):
    """Estimate the character pool used by the password."""
    pool = 0

    if re.search(r"[a-z]", password):
        pool += 26
    if re.search(r"[A-Z]", password):
        pool += 26
    if re.search(r"[0-9]", password):
        pool += 10
    if re.search(r"[^A-Za-z0-9]", password):
        pool += 33

    return pool


def analyze_password(password):
    """Analyze a password and return a structured security report."""

    if not isinstance(password, str):
        raise ValueError("Password must be text.")

    if not password:
        return {
            "strength": "No Password",
            "score": 0,
            "max_score": 100,
            "checks": {},
            "issues": ["Enter a password to analyze."],
            "suggestions": ["Choose a long, unique password."]
        }

    if len(password) > 1024:
        raise ValueError("Password must not exceed 1024 characters.")

    score = 0
    checks = {}
    issues = []
    suggestions = []

    # 1. Length assessment
    length = len(password)

    
    if length >= 20:
        score += 50
        checks["length"] = "Excellent"
    elif length >= 16:
        score += 40
        checks["length"] = "Very Good"
    elif length >= 12:
        score += 30
        checks["length"] = "Good"
    elif length >= 8:
        score += 20
        checks["length"] = "Fair"
    else:
        score += 5
        checks["length"] = "Poor"

        issues.append("Password is shorter than 8 characters.")
        suggestions.append("Use at least 12 characters, preferably more.")

    # 2. Character variety
    variety = 0

    if re.search(r"[a-z]", password):
        variety += 1
    if re.search(r"[A-Z]", password):
        variety += 1
    if re.search(r"\d", password):
        variety += 1
    if re.search(r"[^A-Za-z0-9]", password):
        variety += 1

    variety_points = [0, 5, 10, 15, 20]
    score += variety_points[variety]
    checks["character_variety"] = f"{variety}/4 types"

    if variety < 3:
        issues.append("Limited character variety.")
        suggestions.append(
            "Consider using a mix of character types or a long passphrase."
        )

    # 3. Common password detection
    if password.casefold() in COMMON_PASSWORDS:
        score = 0
        checks["common_password"] = "High risk"
        issues.append("This is a commonly used password.")
        suggestions.append("Replace it with a unique password.")
    else:
        checks["common_password"] = "Not in built-in list"

    # 4. Repeated-character detection
    if len(password) >= 3 and re.fullmatch(r"(.)\1+", password):
        score = min(score, 10)
        checks["repeated_characters"] = "High risk"
        issues.append("Password repeats the same character.")
        suggestions.append("Avoid passwords made of repeated characters.")
    elif re.search(r"(.)\1{2,}", password):
        score -= 5
        checks["repeated_characters"] = "Some repetition"
        issues.append("Three or more consecutive characters are repeated.")
    else:
        checks["repeated_characters"] = "No obvious repetition"

    # 5. Predictable sequence detection
    lowered = password.casefold()
    found_sequence = any(
        pattern in lowered for pattern in KEYBOARD_PATTERNS
    )

    if found_sequence:
        score -= 15
        checks["sequences"] = "Detected"
        issues.append("A predictable sequence was detected.")
        suggestions.append("Avoid keyboard or alphabetical sequences.")
    else:
        checks["sequences"] = "No listed sequence detected"

    # 6. Simple dictionary-word warning
    if any(word in lowered for word in COMMON_WORDS):
        score -= 10
        checks["common_words"] = "Detected"
        issues.append("A common password-related word was detected.")
        suggestions.append(
            "Avoid predictable words and common password patterns."
        )
    else:
        checks["common_words"] = "Not detected"

    # Keep the score between 0 and 100
    score = max(0, min(100, score))

    # Assign a rating
    if score < 30:
        strength = "Weak"
    elif score < 55:
        strength = "Fair"
    elif score < 75:
        strength = "Strong"
    else:
        strength = "Very Strong"

    if not suggestions:
        suggestions.append(
            "No obvious weaknesses were found by these basic checks."
        )

    # Educational estimate, not a real-world crack-time prediction
    pool = calculate_character_pool(password)

    if pool:
        estimated_combinations = pool ** length
        estimated_bits = length * math.log2(pool)
    else:
        estimated_combinations = 0
        estimated_bits = 0

    return {
        "strength": strength,
        "score": score,
        "max_score": 100,
        "checks": checks,
        "issues": issues,
        "suggestions": suggestions,
        "length": length,
        "estimated_search_space_bits": round(estimated_bits, 2),
        "estimated_combinations": str(estimated_combinations)
    }
