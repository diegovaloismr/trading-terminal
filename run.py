import schedule
import time
from main import main

def job():
    print("Rodando sistema...")
    main()

schedule.every(5).minutes.do(job)

print("🚀 Rodando na nuvem...")

while True:
    schedule.run_pending()
    time.sleep(30)
