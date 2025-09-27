# tools/respect_robots.py
import sys
import urllib.parse
import urllib.request


def can_fetch(url: str, agent: str = "Base44Bot"):
    parsed = urllib.parse.urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    try:
        from urllib.robotparser import RobotFileParser

        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(agent, url)
    except:
        return True


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com/"
    print("ALLOW" if can_fetch(url) else "DISALLOW")
