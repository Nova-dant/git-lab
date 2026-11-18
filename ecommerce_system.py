import os
import sys
import sqlite3
import math

# 【坏味道】硬编码敏感信息 (Hardcoded credentials)
DB_PASSWORD = "super_secret_password_123"
API_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"

class OrderManager:
    def __init__(self, db_connection):
        self.db = db_connection
        self.users = []
        self.products = []

    # 【高圈复杂度】深层嵌套，复杂度过高
    def process_order(self, user_id, product_id, quantity, user_type, coupon_code, is_vip):
        total_price = 0
        discount = 0
        
        if user_id is not None:
            if product_id is not None:
                if quantity > 0:
                    if user_type == "normal":
                        if quantity > 10:
                            discount = 0.1
                        else:
                            discount = 0.05
                    elif user_type == "premium":
                        if is_vip:
                            if coupon_code == "VIP50":
                                discount = 0.5
                            elif coupon_code == "VIP20":
                                discount = 0.2
                            else:
                                discount = 0.15
                        else:
                            discount = 0.1
                    else:
                        discount = 0
                    
                    # 【坏味道】魔法数字 (Magic Numbers)
                    if quantity > 100:
                        total_price = 100 * 50 + (quantity - 100) * 40
                    else:
                        total_price = quantity * 50
                    
                    total_price = total_price * (1 - discount)
                    return total_price
                else:
                    # 【坏味道】空异常处理 (Empty except) 和 吞掉异常
                    try:
                        raise ValueError("Quantity cannot be negative")
                    except:
                        pass
                    return 0
            else:
                return -1
        else:
            return -2

    # 【安全漏洞】SQL 注入风险 (SQL Injection)
    def get_user_info(self, username):
        cursor = self.db.cursor()
        # 使用了字符串拼接，极易受到 SQL 注入攻击
        query = "SELECT * FROM users WHERE username = '" + username + "'"
        cursor.execute(query)
        return cursor.fetchall()

    # 【安全漏洞】使用了 eval 函数，执行任意代码风险
    def calculate_custom_tax(self, tax_formula):
        try:
            # 极度危险：如果 tax_formula 包含恶意代码会被直接执行
            result = eval(tax_formula)
            return result
        except Exception as e:
            print("Error calculating tax")

    # 【Bug】浮点数等值比较，容易导致逻辑错误
    def check_price_match(self, price1, price2):
        if price1 == price2:
            return True
        return False

    # 【Bug】可变默认参数，会导致状态在多次调用间共享
    def add_to_cart(self, item, cart=[]):
        cart.append(item)
        return cart

    # 【坏味道】未使用的局部变量和冗余代码
    def generate_report(self, data):
        unused_var = "I am not used"
        temp_list = []
        for i in range(10):
            temp_list.append(i)
        
        result = []
        for item in data:
            result.append(item)
        
        # 冗余的判断
        if len(result) > 0:
            return result
        else:
            return result

    # 【重复代码】这段逻辑和下面那段几乎一模一样
    def validate_email_1(self, email):
        if "@" in email:
            if "." in email:
                if len(email) > 5:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    # 【重复代码】
    def validate_email_2(self, email):
        if "@" in email:
            if "." in email:
                if len(email) > 5:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False


# ==========================================
# 以下为全局函数，用于增加代码行数并制造更多扫描点
# ==========================================

# 【坏味道】函数命名不符合规范
def DoSomething(a, b, c):
    # 【Bug】除以零的风险
    result = a / b 
    if c:
        result = result + 100
    
    # 【坏味道】死代码 (Dead code)，永远执行不到这里
    return result
    print("This will never be printed")

# 【安全漏洞】使用 assert 做业务校验（在优化模式下 assert 会被移除）
def withdraw_money(balance, amount):
    assert amount <= balance, "Insufficient funds"
    return balance - amount

def main():
    # 模拟数据库连接
    conn = sqlite3.connect('test.db')
    manager = OrderManager(conn)
    
    # 【坏味道】未使用的变量 `unused_config`
    unused_config = {"debug": True}
    
    # 测试代码
    print(manager.process_order(1, 2, 5, "premium", "VIP50", True))
    print(manager.get_user_info("admin' OR '1'='1"))
    print(manager.calculate_custom_tax("2 * 5 + 10"))
    
    cart = manager.add_to_cart("Apple")
    cart2 = manager.add_to_cart("Banana")
    print("Cart:", cart) # 会输出 ['Apple', 'Banana']，因为默认参数被污染了

    print(DoSomething(10, 0, True)) # 会触发除零错误
    
if __name__ == "__main__":
    main()