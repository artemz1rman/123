"""
CreditCalc — консольная программа для расчета стоимости кредита.

Выполняет расчет ежемесячного аннуитетного платежа и общей переплаты
по формуле аннуитетных платежей на основе введенной пользователем
суммы, годовой процентной ставки и срока кредитования (в месяцах).

Поддерживается ввод и вывод данных как через консоль, так и через
файлы. Предусмотрено сохранение расчетов в виде финансовых планов,
а также резервное копирование и восстановление данных.

Учебная практика, вариант 24.
ПМ 06 «Сопровождение информационных систем»
Выполнил: Колобов П.Н., группа ИСП-31
"""

import json
import os
import shutil
import zipfile
import datetime

# Каталог данных и путь к файлу финансовых планов
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "plans.json")
# Каталог резервных копий и максимальное число хранимых копий
BACKUP_DIR = "backup"
MAX_BACKUPS = 5

# Текущий расчет (заполняется после выполнения вычислений)
current_calc = None


def annuity_payment(amount, annual_rate, months):
    """Вычисляет ежемесячный аннуитетный платеж.

    Аргументы:
        amount      -- сумма кредита, руб.;
        annual_rate -- годовая процентная ставка, %;
        months      -- срок кредитования, месяцев.

    Возвращает размер ежемесячного платежа, руб.
    """
    i = annual_rate / 100 / 12          # месячная процентная ставка
    if i == 0:                          # беспроцентный кредит
        return amount / months
    k = (1 + i) ** months               # коэффициент наращения
    return amount * i * k / (k - 1)


def payment_schedule(amount, annual_rate, months, payment):
    """Строит график платежей по месяцам.

    Возвращает список строк вида:
    «Месяц | Платеж | Проценты | Погашение долга | Остаток».
    """
    i = annual_rate / 100 / 12
    balance = amount
    rows = []
    for m in range(1, months + 1):
        interest = balance * i                     # проценты за месяц
        principal = payment - interest             # погашение долга
        balance -= principal
        if m == months:                            # последний платеж
            principal += balance
            payment_m = payment + balance
            balance = 0
        else:
            payment_m = payment
        balance = max(balance, 0)
        rows.append("%3d | %10.2f | %10.2f | %10.2f | %10.2f"
                    % (m, payment_m, interest, principal, balance))
    return rows


def read_number(prompt, minimum=None, integer=False):
    """Запрашивает у пользователя число с проверкой корректности."""
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            value = float(raw)
            if integer:
                if value != int(value):
                    raise ValueError("срок должен быть целым числом")
                value = int(value)
            if minimum is not None and value < minimum:
                raise ValueError("значение не может быть меньше %s" % minimum)
            return value
        except ValueError as error:
            print("  Ошибка ввода:", error, "— повторите попытку.")


def print_result(amount, rate, months, payment):
    """Выводит результаты расчета в консоль и запоминает их."""
    total = payment * months
    overpay = total - amount
    print("\n  ─────────── РЕЗУЛЬТАТ РАСЧЕТА ───────────")
    print("  Сумма кредита:            %12.2f руб." % amount)
    print("  Годовая ставка:           %12.2f %%" % rate)
    print("  Срок кредитования:        %12d мес." % months)
    print("  Ежемесячный платеж:       %12.2f руб." % payment)
    print("  Общая сумма выплат:       %12.2f руб." % total)
    print("  Общая переплата:          %12.2f руб." % overpay)
    print("  ─────────────────────────────────────────")
    return {"amount": amount, "rate": rate, "months": months,
            "payment": round(payment, 2), "total": round(total, 2),
            "overpay": round(overpay, 2)}


def calc_from_console():
    """Расчет кредита при вводе исходных данных с клавиатуры."""
    global current_calc
    print("\n  Введите параметры кредита:")
    amount = read_number("  Сумма кредита, руб.: ", minimum=0.01)
    rate = read_number("  Годовая ставка, %: ", minimum=0)
    months = read_number("  Срок, месяцев: ", minimum=1, integer=True)
    payment = annuity_payment(amount, rate, months)
    current_calc = print_result(amount, rate, months, payment)


def calc_from_file():
    """Читает параметры из файла credit_params.txt и пишет результат
    в файл calc_results.txt (ввод и вывод данных через файлы)."""
    global current_calc
    params_file, result_file = "credit_params.txt", "calc_results.txt"
    if not os.path.exists(params_file):
        with open(params_file, "w", encoding="utf-8") as f:
            f.write("Сумма кредита, руб.: 500000\n")
            f.write("Годовая ставка, %: 18\n")
            f.write("Срок, месяцев: 24\n")
        print("  Файл не найден — создан образец:", params_file)
    values = []
    with open(params_file, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:                    # формат «Ключ: число»
                line = line.split(":", 1)[1]
            digits = "".join(ch for ch in line
                             if ch.isdigit() or ch in ".,")
            digits = digits.replace(",", ".")
            if digits:
                values.append(float(digits))
    if len(values) < 3:
        print("  Ошибка: в файле должно быть три числа "
              "(сумма, ставка, срок).")
        return
    amount, rate, months = values[0], values[1], int(values[2])
    if amount <= 0 or rate < 0 or months < 1:
        print("  Ошибка: параметры не удовлетворяют ограничениям.")
        return
    payment = annuity_payment(amount, rate, months)
    current_calc = print_result(amount, rate, months, payment)
    schedule = payment_schedule(amount, rate, months, payment)
    with open(result_file, "w", encoding="utf-8") as f:
        f.write("РАСЧЕТ СТОИМОСТИ КРЕДИТА (аннуитетные платежи)\n")
        f.write("Сумма кредита:   %.2f руб.\n" % amount)
        f.write("Годовая ставка:  %.2f %%\n" % rate)
        f.write("Срок:            %d мес.\n" % months)
        f.write("Ежемесячный платеж: %.2f руб.\n" % payment)
        f.write("Общая сумма выплат: %.2f руб.\n" % (payment * months))
        f.write("Общая переплата:    %.2f руб.\n\n" % (payment * months - amount))
        f.write("График платежей:\n")
        f.write("Месяц |    Платеж |  Проценты |      Долг |    Остаток\n")
        for row in schedule:
            f.write(row + "\n")
    print("  Результат сохранен в файл:", result_file)


def show_schedule():
    """Выводит график платежей для текущего расчета."""
    if not current_calc:
        print("  Сначала выполните расчет (пункты меню 1 или 2).")
        return
    c = current_calc
    print("\n  Месяц |    Платеж |  Проценты |      Долг |    Остаток")
    for row in payment_schedule(c["amount"], c["rate"], c["months"],
                                c["payment"]):
        print(" ", row)


def load_plans():
    """Загружает список финансовых планов из файла plans.json."""
    if not os.path.exists(DATA_FILE):
        return {"plans": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_plans(data):
    """Сохраняет список финансовых планов в файл plans.json."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_plan():
    """Сохраняет текущий расчет в виде финансового плана (JSON)."""
    if not current_calc:
        print("  Сначала выполните расчет (пункты меню 1 или 2).")
        return
    name = input("  Название плана: ").strip() or "Без названия"
    data = load_plans()
    next_id = max([p["id"] for p in data["plans"]], default=0) + 1
    plan = {"id": next_id, "name": name, **current_calc,
            "created": datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}
    data["plans"].append(plan)
    save_plans(data)
    print("  План №%d «%s» сохранен в %s" % (next_id, name, DATA_FILE))


def list_plans():
    """Выводит список сохраненных финансовых планов."""
    data = load_plans()
    if not data["plans"]:
        print("  Сохраненных планов нет.")
        return
    print("\n  № | Название          | Сумма, руб. | Ставка | Срок | Платеж")
    for p in data["plans"]:
        print("  %2d | %-17s | %11.2f | %5.1f%% | %4d | %8.2f"
              % (p["id"], p["name"][:17], p["amount"], p["rate"],
                 p["months"], p["payment"]))


def load_plan():
    """Выводит подробную информацию о выбранном плане."""
    list_plans()
    data = load_plans()
    if not data["plans"]:
        return
    pid = read_number("  Номер плана для просмотра: ", minimum=1,
                      integer=True)
    for p in data["plans"]:
        if p["id"] == pid:
            print("\n  План №%(id)d «%(name)s» (создан %(created)s):" % p)
            print_result(p["amount"], p["rate"], p["months"], p["payment"])
            return
    print("  План с номером %d не найден." % pid)


def make_backup():
    """Создает резервную копию финансовых планов (zip-архив).

    В каталоге backup хранится не более MAX_BACKUPS копий;
    самые старые копии удаляются автоматически (ротация).
    """
    if not os.path.exists(DATA_FILE):
        print("  Нет данных для копирования — сначала сохраните план.")
        return
    os.makedirs(BACKUP_DIR, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive = os.path.join(BACKUP_DIR, "backup_" + stamp + ".zip")
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(DATA_FILE, os.path.basename(DATA_FILE))
    print("  Резервная копия создана:", archive)
    backups = sorted(f for f in os.listdir(BACKUP_DIR)
                     if f.endswith(".zip"))
    while len(backups) > MAX_BACKUPS:      # ротация копий
        oldest = os.path.join(BACKUP_DIR, backups.pop(0))
        os.remove(oldest)
        print("  Удалена старая копия:", os.path.basename(oldest))


def restore_backup():
    """Восстанавливает данные из последней резервной копии."""
    if not os.path.isdir(BACKUP_DIR):
        print("  Резервных копий не существует.")
        return
    backups = sorted(f for f in os.listdir(BACKUP_DIR)
                     if f.endswith(".zip"))
    if not backups:
        print("  Резервных копий не существует.")
        return
    latest = backups[-1]
    print("  Будет восстановлена копия:", latest)
    answer = input("  Продолжить? (да/нет): ").strip().lower()
    if answer not in ("да", "д", "yes", "y"):
        print("  Восстановление отменено.")
        return
    if os.path.exists(DATA_FILE):          # страховочная копия
        shutil.copy2(DATA_FILE, DATA_FILE + ".bak")
    os.makedirs(DATA_DIR, exist_ok=True)
    with zipfile.ZipFile(os.path.join(BACKUP_DIR, latest)) as z:
        z.extractall(DATA_DIR)
    print("  Данные восстановлены. Прежний файл сохранен как",
          os.path.basename(DATA_FILE) + ".bak")


def main():
    """Главная функция: цикл интерактивного меню программы."""
    print("=" * 52)
    print("  CreditCalc — расчет стоимости кредита (вариант 24)")
    print("=" * 52)
    actions = {"1": calc_from_console, "2": calc_from_file,
               "3": show_schedule, "4": save_plan, "5": list_plans,
               "6": load_plan, "7": make_backup, "8": restore_backup}
    while True:
        print("\n  Меню: 1-расчет (консоль)  2-расчет (файл)"
              "  3-график платежей")
        print("        4-сохранить план  5-список планов"
              "  6-просмотр плана")
        print("        7-резервная копия 8-восстановление  0-выход")
        choice = input("  Ваш выбор: ").strip()
        if choice == "0":
            print("  Работа завершена. До свидания!")
            break
        action = actions.get(choice)
        if action:
            try:
                action()
            except Exception as error:     # защита от аварийного выхода
                print("  Ошибка выполнения операции:", error)
        else:
            print("  Неизвестный пункт меню, повторите выбор.")


if __name__ == "__main__":
    main()
