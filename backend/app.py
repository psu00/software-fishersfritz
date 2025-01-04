from catch import catch_data
from history import save_history
from setup_db import setup_database

def main():
    print(setup_database())
    data = catch_data()
    print(data)
    print(save_history(data))

if __name__ == "__main__":
    main()

