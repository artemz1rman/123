# CreditCalc — кредитный калькулятор 

Консольная программа на языке **Python** для расчёта стоимости кредита:
ежемесячного платежа и общей переплаты по формуле аннуитетных платежей.
Программа сохраняет расчёты в виде финансовых планов и умеет делать
резервные копии данных с возможностью восстановления.

Проект выполнен в рамках учебной практики по профессиональному модулю
**ПМ 06 «Сопровождение информационных систем»** (вариант 24),
специальность 09.02.07 «Информационные системы и программирование».

---

## 1. Как установить

### Шаг 1. Установите Python (если его ещё нет)

Программа работает на Python **3.8 и новее**. Сторонние библиотеки
не используются — только стандартная библиотека, ничего дополнительно
устанавливать через `pip` не нужно.

- Проверить, установлен ли Python: откройте терминал (в Windows —
  командную строку или PowerShell) и выполните:

  ```bash
  python --version
  ```

  Если появилась версия (например, `Python 3.12.1`) — всё готово.
- Если Python не найден — скачайте его с официального сайта
  <https://www.python.org/downloads/> и при установке обязательно
  отметьте галочку **«Add Python to PATH»**.

### Шаг 2. Скачайте проект с GitHub

**Способ 1 — через Git (рекомендуется).** Установите Git с сайта
<https://git-scm.com/downloads>, затем в терминале перейдите в папку
для проектов и склонируйте репозиторий:

```bash
git clone https://github.com/username/CreditCalc.git
cd CreditCalc
```

Вместо `username` подставьте имя пользователя, которому принадлежит
репозиторий (например, своё).

**Способ 2 — ZIP-архивом (без Git).** На странице репозитория нажмите
зелёную кнопку **Code → Download ZIP**, распакуйте архив в любую папку
и откройте её в терминале:

```bash
cd C:\Users\Имя\Downloads\CreditCalc-main
```

**Способ 3 — GitHub Desktop.** На странице репозитория нажмите
**Code → Open with GitHub Desktop → Clone**, выберите папку — репозиторий
скопируется на компьютер автоматически.

### Шаг 3. Запустите программу

Находясь в папке проекта, выполните:

```bash
python creditcalc.py
```

В Windows, если команда `python` не срабатывает, используйте:

```bash
py creditcalc.py
```

Если в терминале появился заголовок «CreditCalc — расчет стоимости
кредита (вариант 24)» и меню — установка выполнена успешно.

---

## 2. Как пользоваться

### Главное меню

После запуска программа выводит меню:

```
Меню: 1-расчет (консоль)  2-расчет (файл)  3-график платежей
      4-сохранить план    5-список планов  6-просмотр плана
      7-резервная копия   8-восстановление 0-выход
```

Введите номер пункта и нажмите `Enter`.

### Расчёт с клавиатуры (пункт 1)

Программа последовательно запросит три параметра:

```
Сумма кредита, руб.: 500000
Годовая ставка, %: 18
Срок, месяцев: 24
```

Десятичный разделитель — точка или запятая (оба варианта принимаются).
Результат выводится на экран:

```
─────────── РЕЗУЛЬТАТ РАСЧЕТА ───────────
Сумма кредита:            500000.00 руб.
Годовая ставка:              18.00 %
Срок кредитования:              24 мес.
Ежемесячный платеж:         24962.05 руб.
Общая сумма выплат:        599089.22 руб.
Общая переплата:            99089.22 руб.
─────────────────────────────────────────
```

При вводе некорректных значений (буквы, отрицательные числа, срок меньше
одного месяца) программа сообщит об ошибке и попросит повторить ввод —
 аварийного завершения не произойдёт.

### Расчёт через файл (пункт 2)

Программа читает параметры из файла `credit_params.txt` и записывает
полный результат (сводку и график платежей) в файл `calc_results.txt`.
Если входного файла нет, программа сама создаст его образец — впишите
свои значения и запустите пункт 2 ещё раз.

Формат `credit_params.txt`:

```
Сумма кредита, руб.: 500000
Годовая ставка, %: 18
Срок, месяцев: 24
```

### График платежей (пункт 3)

Показывает по месяцам: платеж, начисленные проценты, погашение долга
и остаток задолженности. График строится для последнего выполненного
расчёта (сначала выполните пункт 1 или 2):

```
Месяц |    Платеж |  Проценты |      Долг |    Остаток
  1 |   24962.05 |    7500.00 |   17462.05 |  482537.95
  2 |   24962.05 |    7238.07 |   17723.98 |  464813.97
  ...
```

### Финансовые планы (пункты 4–6)

- **Пункт 4 — сохранить план.** Сохраняет текущий расчёт под введённым
  названием в файл `data/plans.json`. Так удобно сохранять несколько
  вариантов кредита и сравнивать их между собой.
- **Пункт 5 — список планов.** Выводит все сохранённые планы:
  номер, название, сумму, ставку, срок и платёж.
- **Пункт 6 — просмотр плана.** Показывает подробные результаты
  выбранного по номеру плана.

### Резервное копирование и восстановление (пункты 7–8)

- **Пункт 7 — резервная копия.** Архивирует `data/plans.json`
  в каталог `backup/backup_ГГГГММДД_ЧЧММСС.zip`. Хранятся последние
  5 копий, самые старые удаляются автоматически (ротация).
- **Пункт 8 — восстановление.** Восстанавливает данные из последней
  копии. Перед восстановлением программа спрашивает подтверждение
  и сохраняет прежний файл как `plans.json.bak`, поэтому данные
  не потеряются даже при ошибочном восстановлении.

### Выход (пункт 0)

Завершает работу программы. Все сохранённые планы и резервные копии
остаются на диске и доступны при следующем запуске.

---

## 3. Структура проекта

```
CreditCalc/
├── creditcalc.py        # исходный код программы
├── credit_params.txt    # образец входного файла с параметрами кредита
├── README.md            # этот файл (русский)
├── README_EN.md         # документация на английском языке
├── TZ_CreditCalc.md     # техническое задание (требования заказчика и разработчика)
├── Reglament_TO.md      # регламент технического обслуживания
├── data/                # финансовые планы (создаётся программой)
└── backup/              # резервные копии plans.json (создаётся программой)
```

## 4. Возможные проблемы

| Проблема | Решение |
|----------|---------|
| `python` не является внутренней или внешней командой | Переустановите Python с галочкой «Add Python to PATH» или используйте команду `py` |
| Программа не видит `credit_params.txt` | Запускайте программу из папки проекта: файлы ищутся в текущем каталоге |
| Восстановлена не та копия | Восстановление берёт самую последнюю копию из `backup/`; старый файл всегда остаётся как `plans.json.bak` |
| Ошибка «Permission denied» при записи | Закройте `calc_results.txt` и `plans.json`, открытые в других программах |

## 5. Автор

Колобов П.Н., группа ИСП-31, специальность 09.02.07
«Информационные системы и программирование».
Учебная практика, ПМ 06 «Сопровождение информационных систем», вариант 24.

# CreditCalc — Annuity Loan Calculator

A **Python** console application for calculating the cost of a loan:
the monthly annuity payment and the total overpayment based on the
user-entered loan amount, annual interest rate, and loan term.
The application stores calculations as financial plans and supports
data backup with restore capability.

The project was completed as part of the educational practice under the
professional module **PM 06 "Maintenance of Information Systems"**
(variant 24), specialty 09.02.07 "Information Systems and Programming".

---

## 1. Installation Guide

### Step 1. Install Python (if not installed yet)

The application requires Python **3.8 or newer**. No third-party
libraries are used — standard library only, so nothing extra has to be
installed via `pip`.

- Check whether Python is installed: open a terminal (Command Prompt
  or PowerShell on Windows) and run:

  ```bash
  python --version
  ```

  If you see a version number (for example, `Python 3.12.1`), you are
  ready to go.
- If Python is missing, download it from the official website
  <https://www.python.org/downloads/> and make sure to tick the
  **"Add Python to PATH"** checkbox during installation.

### Step 2. Download the project from GitHub

**Option 1 — using Git (recommended).** Install Git from
<https://git-scm.com/downloads>, then open a terminal, navigate to your
projects folder and clone the repository:

```bash
git clone https://github.com/username/CreditCalc.git
cd CreditCalc
```

Replace `username` with the account that owns the repository
(for example, your own).

**Option 2 — ZIP archive (without Git).** On the repository page press
the green **Code → Download ZIP** button, unpack the archive into any
folder and open it in a terminal:

```bash
cd C:\Users\Name\Downloads\CreditCalc-main
```

**Option 3 — GitHub Desktop.** On the repository page press
**Code → Open with GitHub Desktop → Clone**, choose a folder — the
repository will be copied to your computer automatically.

### Step 3. Run the application

Being in the project folder, run:

```bash
python creditcalc.py
```

On Windows, if the `python` command does not work, use:

```bash
py creditcalc.py
```

If the terminal shows the "CreditCalc" header and the main menu, the
installation was successful.

---

## 2. User Guide

### Main menu

After the launch the application shows the menu:

```
Menu: 1-calculation (console)  2-calculation (file)  3-payment schedule
      4-save plan              5-list of plans       6-view plan
      7-backup                 8-restore             0-exit
```

Type the item number and press `Enter`.

### Calculation from the keyboard (item 1)

The program asks for three parameters one by one:

```
Loan amount, RUB: 500000
Annual rate, %: 18
Term, months: 24
```

Both a dot and a comma are accepted as the decimal separator.
The result is printed to the screen:

```
─────────── CALCULATION RESULT ───────────
Loan amount:              500000.00 RUB
Annual rate:                 18.00 %
Loan term:                      24 months
Monthly payment:            24962.05 RUB
Total payments:             599089.22 RUB
Total overpayment:           99089.22 RUB
──────────────────────────────────────────
```

On invalid input (letters, negative numbers, term less than one month)
the program reports the error and asks to retry — there is no crash.

### File-based calculation (item 2)

The program reads the parameters from `credit_params.txt` and writes
the full result (summary and payment schedule) to `calc_results.txt`.
If the input file is missing, the program creates a sample one — put
your values in it and run item 2 again.

Format of `credit_params.txt`:

```
Сумма кредита, руб.: 500000
Годовая ставка, %: 18
Срок, месяцев: 24
```

(Loan amount / Annual rate / Term in months.)

### Payment schedule (item 3)

Displays month by month: payment, accrued interest, principal repaid
and the remaining balance. The schedule is built for the last
calculation performed (run item 1 or 2 first).

### Financial plans (items 4–6)

- **Item 4 — save plan.** Saves the current calculation under an
  entered name into `data/plans.json`. Handy for keeping several loan
  options and comparing them later.
- **Item 5 — list of plans.** Shows all saved plans: number, name,
  amount, rate, term and payment.
- **Item 6 — view plan.** Shows the detailed results of the plan
  selected by its number.

### Backup and restore (items 7–8)

- **Item 7 — backup.** Archives `data/plans.json` into
  `backup/backup_YYYYMMDD_HHMMSS.zip`. The last 5 copies are kept,
  the oldest ones are removed automatically (rotation).
- **Item 8 — restore.** Restores the data from the latest copy. Before
  restoring, the program asks for confirmation and saves the current
  file as `plans.json.bak`, so no data can be lost by a mistaken
  restore.

### Exit (item 0)

Ends the application. All saved plans and backups remain on disk and
are available at the next launch.

---

## 3. Project Structure

```
CreditCalc/
├── creditcalc.py        # source code
├── credit_params.txt    # sample input file with loan parameters
├── README.md            # documentation in Russian
├── README_EN.md         # this file
├── TZ_CreditCalc.md     # technical requirements (customer & developer)
├── Reglament_TO.md      # maintenance regulations
├── data/                # financial plans (created by the program)
└── backup/              # backups of plans.json (created by the program)
```

## 4. Troubleshooting

| Problem | Solution |
|---------|----------|
| `python` is not recognized as a command | Reinstall Python with the "Add Python to PATH" checkbox or use the `py` command |
| The program cannot find `credit_params.txt` | Run the program from the project folder: files are searched in the current directory |
| Wrong copy restored | Restore always takes the latest copy from `backup/`; the previous file is always kept as `plans.json.bak` |
| "Permission denied" when writing | Close `calc_results.txt` and `plans.json` opened in other programs |

## 5. Author

Kolobov P.N., group ISP-31, specialty 09.02.07
"Information Systems and Programming".
Educational practice, PM 06 "Maintenance of Information Systems",
variant 24.

