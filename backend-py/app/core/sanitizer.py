import html
import re


def sanitize_text(value: str | None) -> str | None:
    if value is None:
        return None
    value = html.escape(value)
    value = re.sub(r"<[^>]*>", "", value)
    return value.strip()


def sanitize_html(value: str | None) -> str | None:
    if value is None:
        return None
    allowed_tags = {
        "p",
        "br",
        "strong",
        "em",
        "u",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "ul",
        "ol",
        "li",
        "a",
        "img",
        "blockquote",
        "code",
        "pre",
    }
    value = re.sub(r"<script[^>]*>.*?</script>", "", value, flags=re.DOTALL | re.IGNORECASE)
    value = re.sub(r"\s+on\w+\s*=\s*[\"'][^\"']*[\"']", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\s+on\w+\s*=\s*\S+", "", value, flags=re.IGNORECASE)
    value = re.sub(r"javascript\s*:", "", value, flags=re.IGNORECASE)
    value = re.sub(
        r"<(?!/?(?:" + "|".join(allowed_tags) + r")\b)[^>]*>",
        "",
        value,
        flags=re.IGNORECASE,
    )
    return value.strip()


def validate_password_strength(password: str) -> None:
    errors: list[str] = []
    if len(password) < 8:
        errors.append("密码至少 8 个字符")
    if not re.search(r"[A-Za-z]", password):
        errors.append("密码需包含字母")
    if not re.search(r"\d", password):
        errors.append("密码需包含数字")
    if errors:
        from app.core.exceptions import AppError

        raise AppError("；".join(errors), 400)
