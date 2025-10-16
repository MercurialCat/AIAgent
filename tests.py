from functions.run_python_file import run_python_file

def main():
   run1=run_python_file("calculator", "main.py") 
   print(run1)
   run2=run_python_file("calculator", "main.py",['6 + 9'])
   print(run2)
   run3=run_python_file("calculator", "tests.py")
   print(run3)
   run4=run_python_file("calculator", "../main.py") #(this should return an error)
   print(run4)
   run5=run_python_file("calculator", "nonexistent.py") #(this should return an error)
   print(run5)
   run6=run_python_file("calculator", "lorem.txt")
   print(run6)
   
if __name__ == "__main__":
    main()