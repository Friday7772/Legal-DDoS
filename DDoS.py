import asyncio
import aiohttp
from multiprocessing import Pool, cpu_count
import time
import psutil
import os
from threading import Thread
from datetime import datetime
import csv

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

request_times = []
stop_test = False
log_data = []

def get_user_input():
    global URL, TOTAL, CONCURRENT, METHOD, PAYLOAD
    clear_terminal()
    print("=== Friday Legal DDoS Test Script ===\n")
    url = input("Hedef URL/IP: ")
    port = input("Port (default 80): ") or "80"
    URL = f"http://{url}:{port}"
    TOTAL = int(input("Toplam istek: "))
    CONCURRENT = int(input("Eşzamanlı istek: "))
    METHOD = input("GET/POST (default GET): ").upper() or "GET"
    PAYLOAD = None
    if METHOD == "POST":
        PAYLOAD = input("POST payload: ")
    input("Başlatmak için Enter'a bas...")

async def fetch(session):
    start = time.time()
    status = None
    try:
        if METHOD == "GET":
            async with session.get(URL, headers={"User-Agent":"Friday"}) as resp:
                status = resp.status
        else:
            async with session.post(URL, data=PAYLOAD, headers={"User-Agent":"Friday"}) as resp:
                status = resp.status
    except:
        status = None
    end = time.time()
    elapsed = end - start
    request_times.append(elapsed)
    log_data.append({"time": datetime.now().strftime("%H:%M:%S"), "status": status, "duration": elapsed})
    return status

async def run_batch(n):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(fetch(session)) for _ in range(n)]
        return await asyncio.gather(*tasks)

def run_process(n):
    asyncio.run(run_batch(n))

def draw_bar(done, total, length=50):
    filled = int(done / total * length)
    return "#" * filled + "-" * (length - filled)

def show_stats():
    global stop_test
    last_done = 0
    while not stop_test:
        time.sleep(1)
        done = len(request_times)
        if done == last_done:
            continue
        avg = sum(request_times)/done
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        bar = draw_bar(done, TOTAL)
        print(f"{done}/{TOTAL} [{bar}] Avg:{avg:.2f}s CPU:{cpu}% RAM:{ram}%", end="\r")
        last_done = done
        if done >= TOTAL:
            stop_test = True
            break

def show_summary():
    clear_terminal()
    print("\nFriday Legal DDoS Test Tamamlandı!\n")
    print(f"Toplam süre: {sum(request_times):.2f}s")
    print(f"Ortalama süre: {sum(request_times)/len(request_times):.2f}s")
    print(f"Minimum süre: {min(request_times):.2f}s | Maksimum süre: {max(request_times):.2f}s")
    log_file = f"friday_ddos_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(log_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["time", "status", "duration"])
        writer.writeheader()
        for row in log_data:
            writer.writerow(row)
    print(f"Log kaydedildi: {log_file}")

def main():
    get_user_input()
    per_process = TOTAL // cpu_count()
    stat_thread = Thread(target=show_stats)
    stat_thread.start()
    with Pool(cpu_count()) as pool:
        pool.map(run_process, [per_process]*cpu_count())
    stat_thread.join()
    show_summary()

if __name__ == "__main__":
    main()
