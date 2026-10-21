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
