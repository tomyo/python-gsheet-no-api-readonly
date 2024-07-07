from gsheet_read import get_sheet_data

ID = "11jH0hVkrL52ahV-aNphRq4byh1hupthlbLTCo1zqnio" # gsheet id
GID = "1380064397" # gsheet gid

if __name__ == "__main__":
    print(get_sheet_data(id=ID, gid=GID))