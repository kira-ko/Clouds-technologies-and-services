#!/usr/bin/env python3
import time
import sys

def main():
    print("Добро пожаловать!")
    
    counter = 0
    try:
        while counter < 5:
            counter += 1
            print(f"Итерация #{counter}: Приложение работает...")
            time.sleep(1)
        
        print("\nПриложение успешно завершило работу!")
        return 0
    except KeyboardInterrupt:
        print("\n\nПриложение остановлено пользователем")
        return 130

if __name__ == "__main__":
    sys.exit(main())

