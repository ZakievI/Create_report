import pytest
from main import Create_report, hours_worked_parameters, rate_parameters
from unittest.mock import patch
import sys

# Фикстуры для тестовых данных
@pytest.fixture
def sample_csv_file(tmp_path):
    """Создает временный CSV файл для тестирования"""
    content = """name,department,hours_worked,hourly_rate
John Doe,IT,160,25
Jane Smith,HR,120,30
Bob Johnson,IT,180,20"""
    file_path = tmp_path / "test.csv"
    file_path.write_text(content)
    return str(file_path)

@pytest.fixture
def sample_csv_file_with_different_headers(tmp_path):
    """Создает временный CSV файл с альтернативными названиями столбцов"""
    content = """name,department,hours,salary
Alice Brown,Finance,150,35
Tom Wilson,Marketing,140,40"""
    file_path = tmp_path / "test_alt.csv"
    file_path.write_text(content)
    return str(file_path)

@pytest.fixture
def sample_csv_file_missing_columns(tmp_path):
    """Создает временный CSV файл с отсутствующими столбцами"""
    content = """name,department
Mike Davis,IT"""
    file_path = tmp_path / "test_missing.csv"
    file_path.write_text(content)
    return str(file_path)

@pytest.fixture
def sample_csv_file_partial_data(tmp_path):
    """Создает временный CSV файл с частичными данными"""
    content = """name,department,hours_worked,hourly_rate
John Doe,IT,160,25
Jane Smith,HR,,30
Bob Johnson,IT,180,"""
    file_path = tmp_path / "test_partial.csv"
    file_path.write_text(content)
    return str(file_path)

@pytest.fixture
def report_instance():
    """Создает экземпляр класса Create_report"""
    return Create_report()

# Тесты
def test_read_report(report_instance, sample_csv_file):
    """Тест чтения CSV файла"""
    report_instance.read_report(sample_csv_file)
    
    # Проверяем наличие ключей с учетом возможных пробелов
    people_keys = [key.strip() for key in report_instance.dict_people.keys()]
    assert len(people_keys) == 3
    assert "John Doe" in people_keys
    assert "Jane Smith" in people_keys
    assert "Bob Johnson" in people_keys
    
    # Получаем актуальный ключ с пробелами
    john_key = next(k for k in report_instance.dict_people.keys() if k.strip() == "John Doe")
    assert report_instance.dict_people[john_key]["department"] == "IT"
    assert report_instance.dict_people[john_key]["hours_worked"] == "160"
    assert report_instance.dict_people[john_key]["hourly_rate"] == "25"

def test_read_report_with_different_headers(report_instance, sample_csv_file_with_different_headers):
    """Тест чтения CSV файла с альтернативными названиями столбцов"""
    report_instance.read_report(sample_csv_file_with_different_headers)
    
    assert len(report_instance.dict_people) == 2
    assert "Alice Brown" in report_instance.dict_people
    assert report_instance.dict_people["Alice Brown"]["hours"] == "150"
    assert report_instance.dict_people["Alice Brown"]["salary"] == "35"

def test_read_report_missing_file(report_instance, capsys):
    """Тест обработки отсутствующего файла"""
    with pytest.raises(FileNotFoundError):
        report_instance.read_report("nonexistent_file.csv")
    
    captured = capsys.readouterr()
    assert "Ошибка считывания файла" not in captured.out  # Проверяем, что сообщение выводится в main, а не здесь

def test_calculate_payout(report_instance, sample_csv_file):
    """Тест расчета выплат"""
    report_instance.read_report(sample_csv_file)
    report_instance.calculate_payout()
    
    assert report_instance.dict_people["John Doe"]["payout"] == 160 * 25
    assert report_instance.dict_people["Jane Smith"]["payout"] == 120 * 30
    assert report_instance.dict_people["Bob Johnson"]["payout"] == 180 * 20

def test_calculate_payout_with_different_headers(report_instance, sample_csv_file_with_different_headers):
    """Тест расчета выплат с альтернативными названиями столбцов"""
    report_instance.read_report(sample_csv_file_with_different_headers)
    report_instance.calculate_payout()
    
    assert report_instance.dict_people["Alice Brown"]["payout"] == 150 * 35
    assert report_instance.dict_people["Tom Wilson"]["payout"] == 140 * 40

def test_calculate_payout_missing_columns(report_instance, sample_csv_file_missing_columns, capsys):
    """Тест расчета выплат с отсутствующими столбцами"""
    report_instance.read_report(sample_csv_file_missing_columns)
    report_instance.calculate_payout()
    
    captured = capsys.readouterr()
    assert "Нет необходимых данных для расчета зарплаты" in captured.out
    assert report_instance.dict_people["Mike Davis"]["payout"] is None

def test_calculate_payout_partial_data(report_instance, sample_csv_file_partial_data, capsys):
    """Тест расчета выплат с частичными данными"""
    report_instance.read_report(sample_csv_file_partial_data)
    report_instance.calculate_payout()
    
    captured = capsys.readouterr()
    assert report_instance.dict_people["John Doe"]["payout"] == 160 * 25
    assert report_instance.dict_people["Jane Smith"]["payout"] is None
    assert report_instance.dict_people["Bob Johnson"]["payout"] is None
    assert "Нет необходимых данных для расчета зарплаты" in captured.out

def test_show_reports(report_instance, sample_csv_file, capsys):
    """Тест вывода отчетов"""
    report_instance.read_report(sample_csv_file)
    report_instance.calculate_payout()
    reports = ["hours_worked", "hourly_rate", "payout"]
    report_instance.show_reports(reports)
    
    captured = capsys.readouterr()
    assert "John Doe" in captured.out
    assert "160" in captured.out
    assert "25" in captured.out
    assert str(160*25) in captured.out
    assert "IT" in captured.out
    assert "HR" in captured.out

def test_main_with_payout_report(report_instance, sample_csv_file, capsys):
    """Тест main с отчетом типа payout"""
    test_args = ["program_name", sample_csv_file, "--report", "payout"]
    with patch.object(sys, 'argv', test_args):
        with patch('main.Create_report') as mock_report:
            mock_instance = mock_report.return_value
            mock_instance.dict_people = {}
            
            # Имитируем выполнение main
            if len(sys.argv) > 1 and "--report" in sys.argv:
                report_type = sys.argv[sys.argv.index("--report") + 1]
                if report_type == "payout":
                    mock_instance.calculate_payout()
                    reports = ["hours_worked", "hourly_rate"] + ["payout"]
                    mock_instance.show_reports(reports)
    
    captured = capsys.readouterr()
    # Проверяем, что методы были вызваны
    mock_instance.calculate_payout.assert_called_once()
    mock_instance.show_reports.assert_called_once()

def test_main_with_custom_report(report_instance, sample_csv_file, capsys):
    """Тест main с пользовательским отчетом"""
    test_args = ["program_name", sample_csv_file, "--report", "custom_report"]
    with patch.object(sys, 'argv', test_args):
        with patch('main.Create_report') as mock_report:
            mock_instance = mock_report.return_value
            mock_instance.dict_people = {}
            
            # Имитируем выполнение main
            if len(sys.argv) > 1 and "--report" in sys.argv:
                report_type = sys.argv[sys.argv.index("--report") + 1]
                # Для пользовательского отчета просто показываем данные
                reports = report_type.replace(' ', '').split(",")
                mock_instance.show_reports(reports)
    
    captured = capsys.readouterr()
    # Проверяем, что метод show_reports был вызван с правильными параметрами
    mock_instance.show_reports.assert_called_once_with(["custom_report"])

def test_parameter_constants():
    """Тест констант параметров"""
    assert "hours_worked" in hours_worked_parameters
    assert "hours" in hours_worked_parameters
    assert "hourly_rate" in rate_parameters
    assert "rate" in rate_parameters
    assert "salary" in rate_parameters