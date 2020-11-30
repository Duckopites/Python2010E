#declar global variable
cnt_enter_account = 0
cnt_enter_password = 0
database = {}

from datetime import datetime
import csv

def get_data_from_file():
    """
    Read data from input file and return a dictionay contains
    informations of users
    """
    fi = open('input.csv', 'r')
    for line in fi:
        if not len(line.split(",")) == 4:
            continue
        fullname, account, password, amount = line.split(",")
        database[account] = {
        'fullname': fullname,
        'account': account,
        'password': int(password),
        'amount': int(amount)
        }
    fi.close()

def write_data_to_file():
    """Update data to csv file"""
    fi = open('input.csv', 'w+', newline='')
    csvwriter = csv.writer(fi)
    #write to csv file
    for key in database:
        csvwriter.writerow([database[key]['fullname'], database[key]['account'], int(database[key]['password']), database[key]['amount']])

def check_account():
    """
    Check account is available in database. If entering account over 3 times, lock account
    """
    global cnt_enter_account
    # entered password is correct
    try:
        account =  input("Nhap so tai khoan: ")
        # get account number from database and compare with entered account
        if account == database[account].get('account'):
            print("NGAN HANG")
            print("Xin chao: " + database[account].get('fullname'))
            check_password(account)
    # entered password is not correct
    except KeyError:
        cnt_enter_account += 1
        # lock account if enter over 3 times
        if cnt_enter_account == 3:
            print("Ngân hàng tạm thời giữ thẻ do bạn nhập sai quá 3 lần")
            exit()
        print("So tai khoan khong dung, vui long lua chon:")
        print("1. Nhap lai so tai khoan")
        print("0. Thoat.")
        choice = int(input("Nhap lua chon: "))
        if choice == 1:
            check_account()
        elif choice == 0:
            exit()

def check_password(account):
    """
    Check password which correspond with account is correct or not.
    If entering password over 3 times, lock account.
    """
    global cnt_enter_password
    pass_word = int(input("Nhap mat khau: "))
    #get password from database and compare with entered password
    if pass_word == int(database[account].get('password')):
        display_menu(account)
    else:
        cnt_enter_password += 1
        print("Sai mat khau, vui long nhap lai.")
        # lock account if enter password over 3 times
        if cnt_enter_password == 3:
            print("Ngân hàng tạm thời giữ thẻ do bạn nhập sai mật khẩu 3 lần. \
                Vui lòng liên hệ nhân viên ngân hàng để được hỗ trợ")
            exit(1)
        check_password(account)

def check_amount(account):
    """
    Check and print amount in account
    """
    print("NGAN HANG: ")
    print("Ngay: ", datetime.now())
    print("So tien trong tai khoan cua ban la: %d" %int(database[account].get('amount')), "VND")
    other_choice(account)

def widthdraw_money(account):
    """
    Implement widthdrawing money from account
    """
    cash = int(input("Nhap so tien can rut: "))
    # widthdrawed money must less than amount in account
    if cash > int(database[account].get('amount')):
        print("Tài khoan không đủ để thực hiện giao dịch, vui long nhap lai")
        widthdraw_money(account)
    else:
        #update amount in database
        database[account]['amount'] = str(int(database[account].get('amount')) - int(cash))
        print("Giao dich thanh cong")
        print("So tien con lai trong tai khoan la: %d" %(int(database[account]['amount'])))
        other_choice(account)

def transfer_money(account):
    try:
        #enter account destination, which need transfering money
        account_dst = input("Nhap so tai khoan chuyen tien:")
        #check account destination is available in database or not
        if account_dst == database[account_dst].get('account'):
            cash_transfer = int(input("Nhap so tien can chuyen: "))
            if cash_transfer > int(database[account].get('amount')):
                print("Tài khoan không đủ để thực hiện giao dịch, vui long nhap lai")
                transfer_money(account)
            else:
                #Update amount in database
                database[account_dst]['amount'] = int(database[account_dst].get('amount')) + cash_transfer
                database[account]['amount'] = int(database[account].get('amount')) - cash_transfer
                print("So tien con lai trong tai khoan la: %d" %(int(database[account]['amount'])))
                other_choice(account)
    except KeyError:
        print("So tai khoan khong dung, vui long nhap lai.")
        transfer_money(account)

def change_password(account):
    """
    Change password
    """
    old_pass = int(input("Nhap mat khau cu:"))
    # Check old password is correct
    if old_pass == int(database[account].get('password')):
        new_pass = int(input("Nhap mat khau moi:"))
        new_pass_confirm = int(input("Xac nhan mat khau moi:"))
        if new_pass == new_pass_confirm:
            print("Thay doi mat khau thanh cong")
            database[account]['password'] = str(new_pass)
            print("Mat khau moi la: %d" %int(database[account]['password']))
            other_choice(account)
        else:
            print("Xac nhan mat khau khong dung")
    else:
        print("Mat khau cu khong dung")
        change_password(account)

def other_choice(account):
    """
    Display menu again or exit program
    """
    print("1. Giao dich khac.")
    print("0. Thoat")
    choice = int(input("Nhap lua chon: "))
    if choice == 1:
        display_menu(account)
    elif choice == 0:
        return

def display_menu(account):
    """
    Display menu and choice the option
    """
    print("1. Kiem tra so du.")
    print("2. Rut tien.")
    print("3. Chuyen tien.")
    print("4. Doi mat khau.")
    print("0. Thoat")
    enter_option = int(input("Nhap lua chon: "))
    if enter_option == 1:
        check_amount(account)
    elif enter_option == 2:
        widthdraw_money(account)
    elif enter_option == 3:
        transfer_money(account)
    elif enter_option == 4:
        change_password(account)
    elif enter_option == 0:
        return

if __name__ == "__main__":
    get_data_from_file()
    check_account()
    write_data_to_file()