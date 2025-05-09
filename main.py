import argparse

hours_worked_parameters = [
    "hours_worked",
    "hours",
]  # параметры, которые будут использоваться для расчета часов работы
rate_parameters = [
    "hourly_rate",
    "rate",
    "salary",
]  # параметры, которые будут использоваться для расчета ставки за час


class Create_report:
    def __init__(self):
        self.dict_people = {}

    def read_report(self, path_file):
        with open(path_file, "r") as file:
            header = file.readline().replace("\n", "").split(",")
            index_name = header.index("name")
            data = file.readlines()
            for row in data:
                row = row.replace("\n", "").split(",")
                info_person = {}
                for i, key in enumerate(header):
                    if key != "name":
                        info_person[key] = row[i]
                self.dict_people[row[index_name]] = info_person

    def calculate_payout(self):
        for person, info_person in self.dict_people.items():
            key_hours = list(
                set(hours_worked_parameters).intersection(info_person.keys())
            )
            key_rate = list(set(rate_parameters).intersection(info_person.keys()))
            if all([key_hours, key_rate]) and (
                info_person.get(key_hours[0]) != ""
                and info_person.get(key_rate[0]) != ""
            ):
                self.dict_people[person]["payout"] = int(
                    info_person.get(key_hours[0], 0)
                ) * int(info_person.get(key_rate[0], 0))
            else:
                self.dict_people[person]["payout"] = None
                print("Нет необходимых данных для расчета зарплаты")

    def show_reports(self, reports: list):
        dict_department = {}  # сортируем по отделам
        for person, info_person in self.dict_people.items():
            department = info_person.get("department", "NONE")
            dict_department[department] = dict_department.get(department, []) + [person]

        def determ_row_size() -> list:  # определение ширины строки
            width = [0]
            for key in dict_department.keys():  # пробежались по отделам
                if len(key) > width[-1]:
                    width[-1] = len(key)
            width += [0]
            for key in self.dict_people.keys():  # пробежались по именам
                if len(key) > width[-1]:
                    width[-1] = len(key)
            for report in reports:  # пробежались по параметрам
                width += [len(report)]
                for (
                    info_person
                ) in self.dict_people.values():  # пробежались по пернсоналу
                    if len(str(info_person.get(report, ""))) > width[-1]:
                        width[-1] = len(str(info_person.get(report, "")))
            return width

        width = determ_row_size()
        # формирование шапки
        header = ""
        for i, report in enumerate(reports):
            header += f"{report}" + " " + " " * (width[i + 2] - len(report))
        print(f"{' ' * width[0]} name{' ' * (width[1] - 4) + ' ' + header}")
        for key, value in dict_department.items():
            print(key)
            for person in value:
                row = f"{'-' * width[0]} {person + ' ' * (width[1] - len(person))}"
                for i, report in enumerate(reports):
                    value = str(self.dict_people[person].get(report, ""))
                    row += f" {value + ' ' * (width[i + 2] - len(value) - 1)} "
                print(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Обработка CSV-файлов и генерация отчета."
    )

    # Добавляем аргументы для входных файлов (можно передать несколько)
    parser.add_argument(
        "input_files",
        nargs="+",
    )

    # Добавляем аргумент для типа отчета
    parser.add_argument(
        "--report",
        required=True,
    )

    args = parser.parse_args()

    report = Create_report()
    for file in args.input_files:
        try:
            report.read_report(file)
        except FileNotFoundError as e:
            print(f" Ошибка считывания файла. Не смог найти файл {e.filename}")
        except Exception as e:
            print(f" Непредвиденная ошибка:{e}. Обратитесь в поддержку")

    if args.report == "payout":
        report.calculate_payout()  # расчет зарплаты
        reports = [
            "hours_worked",
            "hourly_rate",
        ]  # дополнительные параметры выводимые на экран
        reports += args.report.replace(" ", "").split(",")
        report.show_reports(reports)
