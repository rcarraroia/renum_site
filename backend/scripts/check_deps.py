try:
    import langchain_openai
    print("langchain_openai: OK")
except ImportError:
    print("langchain_openai: MISSING")

try:
    import pypdf
    print("pypdf: OK")
except ImportError:
    print("pypdf: MISSING")
