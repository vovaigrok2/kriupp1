
class Contragent:
    """Контрагент (поставщик, покупатель, банк и т.д.)"""
    def __init__(self, contr_id, name, inn=None, phone=None):
        self.contr_id = contr_id
        self.name = name
        self.inn = inn
        self.phone = phone

    def __str__(self):
        extra = ""
        if self.inn:
            extra += f", ИНН {self.inn}"
        if self.phone:
            extra += f", тел. {self.phone}"
        return f"Контрагент: {self.name}{extra}"


class Account:
    """Статья учета (доходы, расходы, активы и т.п.)"""
    def __init__(self, acc_id, name, is_income=True):
        """
        is_income:
          True  → доходы / поступления
          False → расходы / выбытия
        """
        self.acc_id = acc_id
        self.name = name
        self.is_income = is_income

    def __str__(self):
        type_str = "Доход" if self.is_income else "Расход"
        return f"{type_str}: {self.name}"


class Transaction:
    """Бухгалтерская операция / проводка"""
    def __init__(self, trans_id, date_str, contragent, account, amount, comment=""):
        self.trans_id = trans_id
        self.date_str = date_str          # строка вида "2026-03-22"
        self.contragent = contragent      # объект Contragent
        self.account = account            # объект Account
        self.amount = float(amount)       # положительное число
        self.comment = comment

    def get_sign(self):
        """Знак для общей суммы: + для доходов, - для расходов"""
        return 1 if self.account.is_income else -1

    def get_signed_amount(self):
        return self.amount * self.get_sign()

    def __str__(self):
        sign = "+" if self.account.is_income else "-"
        return (f"Операция №{self.trans_id} от {self.date_str}  "
                f"{sign}{self.amount:8.2f} руб.  "
                f"{self.account.name}  →  {self.contragent.name}")


class AccountingSystem:
    """Основной класс системы бухгалтерии"""
    def __init__(self):
        self.contragents = {}     # dict: id → Contragent
        self.accounts = {}        # dict: id → Account
        self.transactions = []    # список операций
        self.next_trans_id = 1001

    def add_contragent(self, contr_id, name, inn=None, phone=None):
        if contr_id in self.contragents:
            print(f"Внимание: контрагент с ID {contr_id} уже существует")
        self.contragents[contr_id] = Contragent(contr_id, name, inn, phone)

    def add_account(self, acc_id, name, is_income=True):
        if acc_id in self.accounts:
            print(f"Внимание: статья с ID {acc_id} уже существует")
        self.accounts[acc_id] = Account(acc_id, name, is_income)

    def add_transaction(self, date_str, contragent_id, account_id, amount, comment=""):
        if contragent_id not in self.contragents:
            print(f"Ошибка: контрагент ID {contragent_id} не найден")
            return
        if account_id not in self.accounts:
            print(f"Ошибка: статья учета ID {account_id} не найдена")
            return

        trans = Transaction(
            self.next_trans_id,
            date_str,
            self.contragents[contragent_id],
            self.accounts[account_id],
            amount,
            comment
        )
        self.transactions.append(trans)
        self.next_trans_id += 1
        return trans

    def get_balance(self):
        """Возвращает текущий финансовый результат (прибыль/убыток)"""
        return sum(t.get_signed_amount() for t in self.transactions)

    def print_report(self):
        print("\n" + "="*70)
        print("ОТЧЁТ ПО ОПЕРАЦИЯМ")
        print("="*70)
        if not self.transactions:
            print("Операций пока нет.\n")
            return

        for t in sorted(self.transactions, key=lambda x: x.date_str):
            print(t)

        total = self.get_balance()
        print("-"*70)
        print(f"Итого финансовый результат: {total:12.2f} руб. "
              f"({'прибыль' if total >= 0 else 'убыток'})")
        print("="*70 + "\n")


def main():
    # Создаём систему
    acc_system = AccountingSystem()

    # Добавляем несколько контрагентов
    acc_system.add_contragent(1, "ООО Ромашка", "7723123456", "+7-495-123-45-67")
    acc_system.add_contragent(2, "ИП Иванов", "123456789012")
    acc_system.add_contragent(3, "ПАО Сбербанк")
    acc_system.add_contragent(4, "ООО Поставщик окон")

    # Добавляем статьи учета
    acc_system.add_account(101, "Продажа товаров", is_income=True)
    acc_system.add_account(201, "Оплата поставщикам", is_income=False)
    acc_system.add_account(202, "Зарплата сотрудников", is_income=False)
    acc_system.add_account(301, "Поступление кредита", is_income=True)
    acc_system.add_account(302, "Оплата аренды", is_income=False)

    # Примеры операций

    acc_system.add_transaction("2026-03-01", 1, 101, 185000, "Продажа партии мебели")
    acc_system.add_transaction("2026-03-03", 4, 201,  92000, "Оплата за материалы")
    acc_system.add_transaction("2026-03-05", 2, 202,  45000, "Зарплата за февраль")
    acc_system.add_transaction("2026-03-10", 3, 301, 500000, "Получен кредит")
    acc_system.add_transaction("2026-03-15", 3, 302,  35000, "Аренда офиса за март")
    acc_system.add_transaction("2026-03-20", 1, 101, 248000, "Реализация услуг монтажа")

    # Выводим отчёт
    acc_system.print_report()


if __name__ == "__main__":
    main()