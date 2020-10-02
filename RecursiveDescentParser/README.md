### Описание 
Программа, которая парсит минимальную часть языка [Prolog](https://en.wikipedia.org/wiki/Prolog), используя [рекурсивный спуск](https://en.wikipedia.org/wiki/Recursive_descent_parser)  

### Запуск 

* Программа использует лексер из библиотеки ply. Её можно установить: 
    ```
    sudo pip install ply
    ```

* Также для тестирования я применял библиотеку pytest. Её можно установить:
    ```
    sudo pip install pytest
    ```
    
* И наконец, запуск программы:
    ```
    python parser.py filename
    ```
