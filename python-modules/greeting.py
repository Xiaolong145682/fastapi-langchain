__all__ = ["DEFAULT_GREETING", "say_hello", "Greeter"]

DEFAULT_GREETING = "你好"

def _normalize_name(name: str) -> str:
    return name.strip() or "朋友"

def say_hello(name: str) -> str:
    return f"{DEFAULT_GREETING}，{_normalize_name(name)}！"

class Greeter:
    def greet(self, name: str) -> str:
        return say_hello(name)

def main() -> None:
    print(say_hello("小微"))

if __name__ == "__main__":
    main()
