#define macro for account_state
ENTER_ACCOUNT = 0
ENTER_PASSWORD = 1

#define macro for main state
CHECK_ACCOUNT = 0
CHOOSE_OPTION = 1
FINISH = 2

#define macro for option state
MENU = 0
CHECK_MONEY = 1
WIDTHDRAW_CASH = 2
TRANSFER_MONEY = 3
CHANGE_PASSWORD = 4
EXIT = 5

#define global variable
account_state = 0
money_check = 0
user_name = ""
password = 0
state = 0
count_enter_account = 0
count_enter_password = 0
count_enter_cash = 0
option_state = 0

from datetime import datetime

#check account whether exist in data file
def check_acc_valid(acc_num, csv_file):
    """
    Check account number and return true if acount number is available
    in csv file or return false if acount number is not available
    in csv file
    """
    global user_name
    global password
    global money_check
    is_acc_valid = False
    with open(csv_file, "r", encoding='utf-8') as csv:
        for line in csv:
            if acc_num == int(line.split(",")[1]):
                user_name = str(line.split(",")[0])
                password = int(line.split(",")[2])
                money_check = int(line.split(",")[3])
                is_acc_valid = True
    return is_acc_valid, user_name, password, money_check

#check account and password is correct
def check_account_and_password():
    """
    Check whether account, password is entered by user is correct.
    If they are correct, allow user choose options. Otherwise, check if user enter over 3 times
    => Lock account.
    """
    global count_enter_account
    global count_enter_password
    global user_name
    global password
    global money_check
    global account_state
    global state
    state = FINISH
    csv_file = 'input.csv'
    #Enter account and check
    if account_state == ENTER_ACCOUNT:
        acc_num = input("Nhap so tai khoan: ")
        #check account and get user name, password, money in data file
        is_acc_valid, user_name, password, money_check = check_acc_valid(int(acc_num), csv_file)
        if(is_acc_valid):
            print("NGAN HANG")
            print("Xin chao: " + user_name)
            # Acc is valid, jump in to enter password
            account_state = ENTER_PASSWORD
            state = CHECK_ACCOUNT
        else:
            count_enter_account += 1
            print("Số tài khoản không đúng. Vui lòng lựa chọn")
            print("1. Nhap lai so tai khoan")
            print("0. Thoat.")
            #if user enter account less than 3 times, enter again, else lock account
            if count_enter_account < 3:
                user_name_option = int(input("Nhap lua chon: "))
                if user_name_option == 1:
                    state = CHECK_ACCOUNT
                    account_state = ENTER_ACCOUNT
                elif user_name_option == 0:
                    state = FINISH
            else:
                print("Ngân hàng tạm thời giữ thẻ do bạn nhập sai tài khoản 3 lần. \
                        Vui lòng liên hệ nhân viên ngân hàng để được hỗ trợ")
                state = FINISH
    #Enter password and check
    elif account_state == ENTER_PASSWORD:
        password_input = int(input("Nhap mat khau: "))
        if password_input == password:
            state = CHOOSE_OPTION
        else:
            print("Sai mat khau, vui long nhap lai.")
            if count_enter_password < 3:
                state = CHECK_ACCOUNT
                account_state = ENTER_PASSWORD
                count_enter_password += 1
            else:
                print("Ngân hàng tạm thời giữ thẻ do bạn nhập sai mật khẩu 3 lần. \
                        Vui lòng liên hệ nhân viên ngân hàng để được hỗ trợ")
                state = FINISH
    return state

def choose_option():
    """
    Choose option menu
    """
    global state
    global money_check
    global account_state
    global option_state
    cash = 0
    global count_enter_cash
    #Menu option
    if option_state == MENU:
        print("1. Kiem tra so du.")
        print("2. Rut tien.")
        print("3. Chuyen tien.")
        print("4. Doi mat khau.")
        print("0. Thoat")
        option_enter = int(input("Nhap lua chon:"))
        if option_enter == 1:
            option_state = CHECK_MONEY
        elif option_enter == 2:
            option_state = WIDTHDRAW_CASH
        elif option_enter == 3:
            option_state = TRANSFER_MONEY
        elif option_enter == 4:
            option_state = CHANGE_PASSWORD
    # Check money in account
    elif option_state == CHECK_MONEY:
        print("NGAN HANG: ")
        print("Ngay: ", datetime.now())
        print("So tien trong tai khoan cua ban la: %d" %money_check , "VND")
        print("1. Giao dich khac.")
        print("0. Thoat")
        check_input = int(input("Nhap lua chon: "))
        if check_input == 0:
            state = FINISH
        elif check_input == 1:
            state = CHOOSE_OPTION
            option_state = MENU
    # Widthdraw cash
    elif option_state == WIDTHDRAW_CASH:
        print("NGAN HANG: ")
        print("Ngay: ", datetime.now())
        print("So tien trong tai khoan cua ban la: %d" %money_check , "VND")
        cash = int(input("Nhap so tien:"))
        # cash in account is not enough to widthdraw
        if cash > int(money_check):
            count_enter_cash += 1
            state = CHOOSE_OPTION
            option_state = WIDTHDRAW_CASH
            print("Tài khoan không đủ để thực hiện giao dịch, vui long nhap lai")
            if count_enter_cash == 3:
                print("Quý khách nhập sai quá 3 lần. Vui lòng đăng nhập lại.")
                #reset all state
                state = CHECK_ACCOUNT
                account_state = ENTER_ACCOUNT
                option_state = MENU
        # cash in account is enough to widthdraw
        else:
            money_check = int(money_check) - int(cash)
            print("Giao dich thanh cong")
            print("So tien con lai trong tai khoan la: %d" %money_check)
            print("1. Giao dich khac.")
            print("0. Thoat")
            check_input = int(input("Nhap lua chon: "))
            if check_input == 0:
                state = FINISH
            elif check_input == 1:
                state = CHOOSE_OPTION
                option_state = MENU
    elif option_state == EXIT:
        state = FINISH
    return state

if __name__ == "__main__":
    state = CHECK_ACCOUNT
    while True:
        if state == CHECK_ACCOUNT:
            state = check_account_and_password()
        # Enter option when user name and password is
        elif state == CHOOSE_OPTION:
            state = choose_option()
        #exit
        elif state == FINISH:
            break



