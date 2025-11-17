from playwright.sync_api import sync_playwright
import json
import time
from pathlib import Path

OUT = Path("shopee_capture")
OUT.mkdir(exist_ok=True)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # True nếu muốn chạy nền
        context = browser.new_context(java_script_enabled=True)

        page = context.new_page()

        recommend_responses = []

        def on_response(response):
            try:
                if "recommend_v2" in response.url:
                    try:
                        j = response.json()
                    except Exception:
                        j = response.text()
                    recommend_responses.append({
                        "url": response.url,
                        "status": response.status,
                        "body": j
                    })
                    print("[+] captured recommend_v2 response:", response.url, "status", response.status)
            except Exception as e:
                print("on_response error:", e)

        page.on("response", on_response)

        target = "https://shopee.vn/Thời-Trang-Nam-cat.11035567"
        print("Navigating to", target)
        page.goto(target, wait_until="domcontentloaded")

        # --- Tương tác với page để Shopee sinh đủ token ---
        page.wait_for_timeout(3000)

        # scroll nhiều lần
        for i in range(5):
            page.mouse.wheel(0, 1000)
            time.sleep(1)

        # hover một số item (nếu có)
        for i in range(3):
            page.mouse.move(200 + i*100, 400 + i*50)
            time.sleep(0.5)

        # wait thêm để JS chạy
        page.wait_for_timeout(5000)

        # Lấy cookies + localStorage (nếu cần)
        cookies = context.cookies()
        local_storage = page.evaluate("""
            (() => { 
                const out = {}; 
                for (let i=0;i<localStorage.length;i++){ 
                    const k = localStorage.key(i); 
                    out[k] = localStorage.getItem(k);
                } 
                return out; 
            })()
        """)

        # Lưu kết quả
        meta = {
            "url": target,
            "timestamp": int(time.time()),
            "cookies": cookies,
            "local_storage": local_storage,
            "recommend_responses_count": len(recommend_responses)
        }
        (OUT / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        (OUT / "recommend_responses.json").write_text(json.dumps(recommend_responses, ensure_ascii=False, indent=2), encoding="utf-8")

        print("Saved meta and recommend responses to", OUT.resolve())
        print("Captured recommend_v2 responses:", len(recommend_responses))

        browser.close()

if __name__ == "__main__":
    main()
