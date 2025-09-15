from functions.write_file import write_file

def main():
   test1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
   print(test1)
   test2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
   print(test2)
   test3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
   print(test3)
   
   
if __name__ == "__main__":
    main()