# Blush & Bloom — Makeup E-commerce Performance Case Study

## Features
- Login/demo entry page (name + email; no real account system)
- Makeup storefront with product search and category filtering
- Individual product details
- Add to bag and Buy Now actions
- Cart page with quantity changes and remove option
- Flask session-based cart
- Locust workload for performance testing customer journeys

## Run locally
1. Open this folder in VS Code.
2. In the terminal:
   ```bash
   python -m venv venv
   ```
3. Activate it on Windows:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt:
   ```cmd
   venv\Scripts\activate.bat
   ```
4. Install:
   ```bash
   pip install -r requirements.txt
   ```
5. Start:
   ```bash
   python app.py
   ```
6. Open http://127.0.0.1:5000/

## Performance test
Keep Flask running. Open a second terminal in this folder and run:
```bash
locust -f locustfile.py --host http://127.0.0.1:5000 --csv makeup_baseline
```
Open http://localhost:8089 and run a test with 10 users first. Later repeat with 50 and 100 users if your computer can handle it. Keep test duration and spawn rate consistent when comparing runs.

Locust creates CSV files. Use those real measurements for response time, P95, throughput and failure rate. Do not present sample or invented values as measured results.

## Notes
- This is a local academic prototype, not a production store.
- Login is a demo form, not secure authentication.
- Checkout is intentionally a demo alert; no payment is processed.
- Product images are loaded from Unsplash, so internet access is needed for images.
- Cart state is stored in Flask's signed session cookie for simplicity.
