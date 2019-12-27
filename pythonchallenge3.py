import requests
import re


class node:
   def __init__(self, val):
     self.val = val
     self.next = None


def main():
   lst = []
   uri = "http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing="
   nodeobj = node('12345')
   with open("r.txt", "w") as f:
     f.write('12345')
     for i in range(0, 400):
       res = requests.get(uri + nodeobj.val)
       print(res.text)
       nextval = re.search("and the next nothing is (\d+)", res.text)
       if nextval:
         nextval = nextval.group(1)
       else:
         break
       f.write(nextval + "\n")
       tmp = node(nextval)
       nodeobj.next = tmp
       nodeobj = tmp
   nextval = str(int(nextval)/2)
   res = requests.get(uri + nodeobj.val)
   print(res.text)
   print(len(lst))


if __name__ == '__main__':
   main()
