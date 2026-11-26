 УВМ — Ассемблер (Вариант №1, Этап 1)

Общее описание
CLI-приложение, транслирующее программу на языке ассемблера (JSON)
во внутреннее представление — список объектов `Instruction`.

 Язык ассемблера
Программа — JSON-массив. Поддерживаемые команды:

| op | Операнды | Поля |
|---|---|---|
| load_const | addr, value | B, C |
| read_mem   | dst, src    | B, C |
| write_mem  | src, addr_reg | B, C |
| mul        | dst, a, b   | C, D, B |

 Команды запуска
- Сборка (нет, Python): `./run.sh --help`
- Ассемблирование: `python -m src.assembler input.json output.bin`
- Режим тестирования: `python -m src.assembler input.json output.bin --test`

 Пример
`python -m src.assembler tests/programs/spec_test.json out.bin --test`

 Тесты
`python -m unittest discover tests`
