import os


def read_secrets(path):

    secrets = {
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
        "OPENAI_BASE_URL": os.environ.get("OPENAI_BASE_URL", ""),
        "OPENAI_MODEL": os.environ.get("OPENAI_MODEL", "")
    }

    with open(path, "r") as secrets_file:
        for line in secrets_file.readlines():
            try:
                key, value = line.strip().split("=")
                secrets[key] = value
            except Exception:
                pass

    return secrets
