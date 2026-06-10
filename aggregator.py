import requests
import base64
import re
import os

def fetch_and_extract(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        content = response.text.strip()

        # Try to decode if it's purely base64
        try:
            # Clean possible whitespace for base64 decoding
            cleaned_content = content.replace('\n', '').replace('\r', '').strip()
            # If it's too short or doesn't look like base64, don't bother
            if len(cleaned_content) > 10 and not any(s in cleaned_content for s in ['://', ' ']):
                decoded = base64.b64decode(cleaned_content).decode('utf-8')
                if '://' in decoded:
                    content = decoded
        except Exception:
            pass

        # Extract proxy links using regex
        # Protocols: vmess, vless, ss, ssr, trojan, tuic, hysteria, hysteria2, hy2, socks, ssh, wireguard, wg, etc.
        pattern = r'(?:vmess|vless|ss|ssr|shadowsocks|trojan|trojan-go|tuic|hysteria|hysteria2|hy2|socks5|socks|ssh|wireguard|wg|snell|brook|juicity)://[^\s"\'<>]+'
        proxies = re.findall(pattern, content, re.IGNORECASE)

        return proxies
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

def main():
    if not os.path.exists('subscriptions.txt'):
        print("subscriptions.txt not found.")
        return

    with open('subscriptions.txt', 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    all_proxies = []
    for url in urls:
        print(f"Fetching {url}...")
        proxies = fetch_and_extract(url)
        print(f"Found {len(proxies)} proxies.")
        all_proxies.extend(proxies)

    # Save to aggregated.txt as requested
    with open('aggregated.txt', 'w') as f:
        for proxy in all_proxies:
            f.write(proxy + '\n')

    print(f"Finished. Total proxies: {len(all_proxies)}")

if __name__ == "__main__":
    main()
