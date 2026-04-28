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
Run analysis for all supported languages (Python, Java, JavaScript, Ruby, PHP, C++, C#, CSS)
python main.py
```

## Output Example

```
Habr Moscow
+--------------------+----------------+-------------------+----------------+
| Язык программирования | Найдено вакансий | Обработано вакансий | Средняя зарплата |
+--------------------+----------------+-------------------+----------------+
| Python             | 338            | 32                | 158926         |
| Java               | 367            | 15                | 122146         |
| JavaScript         | 28             | 14                | 100707         |
| Ruby               | 51             | 12                | 135075         |
| PHP                | 33             | 12                | 138614         |
| C++                | 41             | 6                 | 262000         |
| C#                 | 14             | 4                 | 247750         |
| CSS                | 13             | 6                 | 153250         |
+--------------------+----------------+-------------------+----------------+


SuperJob Moscow
+--------------------+----------------+-------------------+----------------+
| Язык программирования | Найдено вакансий | Обработано вакансий | Средняя зарплата |
+--------------------+----------------+-------------------+----------------+
| Python             | 41             | 13                | 189123         |
| Java               | 7              | 1                 | 115000         |
| JavaScript         | 9              | 2                 | 118750         |
| Ruby               | 0              | 0                 | N/A            |
| PHP                | 2              | 1                 | 240000         |
| C++                | 15             | 10                | 628451         |
| C#                 | 1              | 0                 | N/A            |
| CSS                | 1              | 0                 | N/A            |
+--------------------+----------------+-------------------+----------------+
```

## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
