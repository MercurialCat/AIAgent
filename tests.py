from functions.get_files_info import get_files_info

def main():
   test1 = get_files_info("calculator", ".")
   print(test1)
   test2 = get_files_info("calculator", "pkg")
   print(test2)
   test3 = get_files_info("calculator", "/bin")
   print(test3)
   test4 = get_files_info("calculator", "../")
   print(test4)
if __name__ == "__main__":
    main()