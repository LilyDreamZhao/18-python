def printMenu():
    print("\n\n")
    print("="*60)
    print(" =\t\t欢迎进入到名片管理系统V1.0")
    print(" = 1. 添加名片")
    print(" = 2. 删除名片")
    print(" = 3. 修改名片")
    print(" = 4. 查询名片")
    print(" = 5. 清空名片系统")
    print(" = 6. 打印名片系统")
    print(" = 7. 退出系统")
    print("="*60)
printMenu()
students = []#名片列表
#姓名，电话，地址
length = 0
while True:
    flag = int(input("请输入名片操作系统的操作序号："))
    printMenu()
    if flag == 1:
        student = {}
        newName =  input("name: ")
        age = input("phone: ")
        address = input("address：")
        student['name'] = newName
        student['age'] = age
        student['address'] = address
        students.append(student)
        length += 1
    elif flag == 2:
        delName = input("删除名片，请输入该人名： ")
        existFlag = False
        for i in range(length):
            if students[i]['name'] == delName:
                del students[i]
                length -= 1
                existFlag = True
        if existFlag == False:
            print("该名片系统没有该人名")
    elif flag == 3:
        modifyName =  input("修改名片，请输入该人名： ")
        existFlag = False
        for i in range(length):
            if students[i]['name'] == modifyName:
                students[i]['age'] = input("新的年龄：")
                students[i]['address'] = input("新的地址：")
                existFlag = True
                break
        if existFlag == False:
            print("该名片系统中没有该人名！")
    elif flag == 4:
        searchName = input("查询名片，请输入该人名： ")
        existFlag = False
        for i in range(length):
            if students[i]['name'] == searchName:
                print(students[i])
                existFlag = True
                break
        if existFlag == False:
            print("该名片系统中没有该人名！")
    elif flag == 5:
        del students
        students = []
        length = 0
    elif flag == 6:
        if length == 0:
            print("该名片系统为空！")
            continue
        print(students)    
    elif flag == 7:
        print("退出名片系统操作")
        break
