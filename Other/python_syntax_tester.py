def modList(list):
    list.append(1)
    list.append(4)

def main():
    list = []
    modList(list)
    print(list[1])

main()