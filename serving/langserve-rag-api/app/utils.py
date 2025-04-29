import os


def read_secrets(secrets_file: str) -> dict[str, str]:
    """This function returns secrets stored in a file.

    Args:
        secrets_file (str): Path to the secrets file.

    Returns:
        dict[str, str]: Secrets in a dictionary.
    """

    secrets = {
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
        "OPENAI_BASE_URL": os.environ.get("OPENAI_BASE_URL", ""),
        "OPENAI_MODEL": os.environ.get("OPENAI_MODEL", ""),
    }

    with open(secrets_file, "r") as f:
        for line in f.readlines():
            try:
                key, value = line.strip().split("=")
                secrets[key] = value
            except Exception:
                pass

    return secrets
