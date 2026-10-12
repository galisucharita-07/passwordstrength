
import re


MAX_PASSWORD_LENGTH = 1024

KEYBOARD_PATTERNS = (
    "qwerty",
    "asdfgh",
    "zxcvbn",
    "123456",
    "654321",
    "abcdef",
)


def validate_password(password):
    """Validate password input before analysis."""

    if not isinstance(password, str):
        return {
            "valid": False,
            "error": "Password must be text."
        }

    if len(password) > MAX_PASSWORD_LENGTH:
        return {
            "valid": False,
            "error": "Password must not exceed 1024 characters."
        }

    return {
        "valid": True,
        "error": None
    }


def detect_security_risks(password):
    """Identify common predictable password patterns."""

    risks = []

    if not password:
        return risks

    if password.casefold() in {
        "password",
        "password123",
        "admin",
        "qwerty",
        "123456",
        "12345678",
    }:
        risks.append({
            "type": "common_password",
            "severity": "high",
            "message": "This password is in the built-in common-password list."
        })

    if re.fullmatch(r"(.)\1+", password):
        risks.append({
            "type": "repeated_characters",
            "severity": "high",
            "message": "The password consists of one repeated character."
        })
    elif re.search(r"(.)\1{2,}", password):
        risks.append({
            "type": "character_repetition",
            "severity": "medium",
            "message": "The password contains three or more repeated characters in a row."
        })

    lowered = password.casefold()

    if any(pattern in lowered for pattern in KEYBOARD_PATTERNS):
        risks.append({
            "type": "predictable_sequence",
            "severity": "medium",
            "message": "A common keyboard or character sequence was detected."
        })

    if len(password) < 12:
        risks.append({
            "type": "short_password",
            "severity": "medium",
            "message": "Consider using a longer password or passphrase."
        })

    return risks
