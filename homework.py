class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__ (self, training_type: str,
                duration: float,
                distance: float,
                speed: float,
                calories: float,
                ) -> None:        
        self.training_type = training_type
        self.duration = duration
        self.distance = distance 
        self.speed = speed 
        self.calories = calories

    def get_message(self) -> str: 
        return (f'Тип тренировки: {self.training_type}; ' 
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')                     
        

class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    WORKOUT_CODE = ''
    
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM 
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed =  self.get_distance() / self.duration
        return mean_speed
        
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:  # tut
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""
    cf_cal_run_1 = 18
    cf_cal_run_2 = 20
    WORKOUT_CODE = 'RUN' 
    
    def get_spent_calories(self) -> float:
        callories_1 = (self.cf_cal_run_1 * self.get_mean_speed() - self.cf_cal_run_2)
        callories =  callories_1 * self.weight / self.M_IN_KM * self.duration * 60
        return callories

class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    cf_cal_walk_1 = 0.035
    cf_cal_walk_2 = 2 
    cf_cal_walk_3 = 0.029 
    WORKOUT_CODE = 'WLK'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration,weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        callories_1 = self.get_mean_speed()**self.cf_cal_walk_2 // self.height
        callories_2 = self.cf_cal_walk_1 * self.weight
        callories_3 = self.cf_cal_walk_3 * self.weight
        callories = (callories_1 * callories_3 + callories_2) * self.duration * 60
        return callories

class Swimming(Training): 
    """Тренировка: плавание."""
    cf_swimming_1 = 1.1
    cf_swimming_2 = 2
    LEN_STEP = 1.38
    WORKOUT_CODE = 'SWM'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed_1 = self.length_pool * self.count_pool / super().M_IN_KM
        mean_speed = mean_speed_1 / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        callories_1 = self.get_mean_speed() + self.cf_swimming_1
        callories = callories_1 * self.cf_swimming_2 * self.weight
        return callories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_dict = {'SWM' : Swimming,
              'RUN' : Running,
              'WLK' : SportsWalking}
    return type_dict[workout_type](*data)


def main(training: Training) -> None: 
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages: 
        training = read_package(workout_type, data)
        main(training)

