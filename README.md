# Habr & SuperJob Salary Analyzer

The program collects statistics on programming language salaries from two job platforms: Habr Career and SuperJob. It displays the number of vacancies found, processed, and the average salary for each language in a formatted table.

## How to install

### Obtaining API Keys

The program requires the following keys for SuperJob API:

#### SuperJob API Key
1. Go to [api.superjob.ru](https://api.superjob.ru/)
2. Register or log in to your account
3. Create a new application in your dashboard
4. Get your Secret key (looks like `v3.r.137792131.9f0c8d5f3a9e...`)


Create a `.env` file in the project root and add your SuperJob API key:
```
SUPERJOB_SECRET_KEY=[Your token]
```

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

## Launch
### Scripts Usage Examples
#### Run Full Analysis
```
# Run analysis for all supported languages (Python, Java, JavaScript, Ruby, PHP, C++, C#, CSS)
python main.py
```

## Output Example

```
+Habr Moscow------------+------------------+---------------------+------------------+
| Язык программирования | Найдено вакансий | Обработано вакансий | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Python                | 330              | 0                   | N/A              |
| Java                  | 368              | 0                   | N/A              |
| JavaScript            | 26               | 0                   | N/A              |
| Ruby                  | 45               | 0                   | N/A              |
| PHP                   | 32               | 0                   | N/A              |
| C++                   | 41               | 0                   | N/A              |
| C#                    | 14               | 0                   | N/A              |
| CSS                   | 11               | 0                   | N/A              |
+-----------------------+------------------+---------------------+------------------+
+SuperJob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Найдено вакансий | Обработано вакансий | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Python                | 41               | 12                  | 196133           |
| Java                  | 8                | 1                   | 115000           |
| JavaScript            | 11               | 2                   | 118750           |
| Ruby                  | 0                | 0                   | N/A              |
| PHP                   | 4                | 1                   | 240000           |
| C++                   | 15               | 10                  | 628451           |
| C#                    | 1                | 0                   | N/A              |
| CSS                   | 3                | 0                   | N/A              |
+-----------------------+------------------+---------------------+------------------+
```

## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
