from dataclasses import asdict, dataclass
from typing import Dict, Type, ClassVar, List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE_TEMPLATE: ClassVar[str] = (
        'Тип тренировки: {training_type}; Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE_TEMPLATE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Класс {type(self).__name__} не содержит'
                                  'метод get_spent_calories')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )
        return info_message


class Running(Training):
    """Тренировка: бег."""
    CF_RUN_1: int = 18
    CF_RUN_2: int = 20
    CF_RUN_3: int = 60
    WORKOUT_CODE = 'RUN'

    def get_spent_calories(self) -> float:
        cal = (self.CF_RUN_1 * self.get_mean_speed() - self.CF_RUN_2)
        cal_1 = cal * self.weight / self.M_IN_KM * self.duration
        return cal_1 * self.CF_RUN_3


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CF_WLK_1: float = 0.035
    CF_WLK_2: int = 2
    CF_WLK_3: float = 0.029
    CF_WLK_4: int = 60
    WORKOUT_CODE: str = 'WLK'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        cal_1 = self.get_mean_speed()**self.CF_WLK_2 // self.height
        cal_2 = self.CF_WLK_1 * self.weight
        cal_3 = self.CF_WLK_3 * self.weight
        return (cal_1 * cal_3 + cal_2) * self.duration * self.CF_WLK_4


class Swimming(Training):
    """Тренировка: плавание."""
    CF_SWIMMING_1: float = 1.1
    CF_SWIMMING_2: int = 2
    LEN_STEP: float = 1.38
    WORKOUT_CODE: str = 'SWM'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed_1 = self.length_pool * self.count_pool / self.M_IN_KM
        return mean_speed_1 / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        callories_1 = self.get_mean_speed() + self.CF_SWIMMING_1
        return callories_1 * self.CF_SWIMMING_2 * self.weight


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_training : Dict[str, Type[Training]] = {
                 'SWM': Swimming,
                 'RUN': Running,
                 'WLK': SportsWalking,
        }
    if workout_type not in type_training:
        raise KeyError(f'Тренировка {workout_type} не поддерживается')             
    return type_training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)