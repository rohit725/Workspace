def parser(lst):
    count, start, end, ind, val = [0] * 5
    flag = True
    while True:
        if lst[ind] == "(":
            if count == 0:
                start = ind
            count += 1
        elif lst[ind] == ")":
            count -= 1
            if count == 0:
                end = ind
        if not (start == 0 and end == 0):
            print(lst[start+1:end])
            val = parser(lst[start+1:end])
            if not val:
                break
            if not end + 1 == len(lst):
                end_slice = lst[end+1:len(lst)]
            else:
                end_slice = []
            lst = lst[0:start].append(val)
            lst = lst.extend(end_slice)
            ind = lst.index(val)
            flag = False
            start = 0
            end = 0
        if ind == len(lst) - 1:
            if "(" in lst or ")" in lst:
                print("Incorrect Expression")
                val = None
                break
            else:
                val = eval("".join(lst))
                print(val)
                break
        if flag:
            ind += 1
        else:
            flag = True
    return val

if __name__ == "__main__":
    a = "1+2+1+(3+1-(2+21-(23-4)))+24-9+(22-6+12-(21+2)) + 22"
    a = list(a)
    val = parser(a)
    print(val)
