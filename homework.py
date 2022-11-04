from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность:{self.duration: .3f} ч.; '
                f'Дистанция:{self.distance: .3f} км; '
                f'Ср. скорость:{self.speed: .3f} км/ч; '
                f'Потрачено ккал:{self.calories: .3f}.')


class Training:
    """Базовый класс тренировки."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        '''Принимает несколько показателей:
        1. action - число шагов или гребков
        2. LEN_STEP - расстояние шага или гребка
        3. weight - вес пользователя
        '''
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = (self.action * self.LEN_STEP) / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения, км/ч."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег.

    Средняя скорость (get_mean_speed) - км/ч
    Расстояние       (get_distance) - км.
    Время тренировки (duration) - ч.
    Вес              (weight) - кг.
    """
    def __init__(self, action, weight, duration) -> None:
        super().__init__(action, weight, duration)
        '''Принимает несколько показателей:
        1. action - число шагов или гребков
        2. LEN_STEP - расстояние шага или гребка
        3. weight - вес пользователя
        '''

    def get_spent_calories(self) -> float:
        run_calor = ((super().CALORIES_MEAN_SPEED_MULTIPLIER
                     * super().get_mean_speed()
                     + super().CALORIES_MEAN_SPEED_SHIFT)
                     * (self.weight / super().M_IN_KM)
                     * self.duration * super().MIN_IN_H)
        return run_calor


class SportsWalking(Training):
    """Тренировка: спортивная ходьба.

    Средняя скорость (get_mean_speed) - км/ч
    Расстояние       (get_distance) - км.
    Время тренировки (duration) - ч.
    Вес              (weight) - кг.
    Рост             (height) - см.
    """
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100
    H_IN_MIN: int = 60

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)

        self.height = height

    def get_spent_calories(self) -> float:
        '''Расчет потраченных калорий.'''
        calories = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                    + ((super().get_mean_speed() * self.KMH_IN_MSEC) ** 2
                        / (self.height / self.CM_IN_M))
                    * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                    * self.weight) * self.duration * self.H_IN_MIN)
        return calories


class Swimming(Training):
    """Тренировка: плавание.

    Средняя скорость (get_mean_speed) - км/ч
    Расстояние       (get_distance) - км.
    Время тренировки (duration) - ч.
    Вес              (weight) - кг.
    """
    LEN_STEP: float = 1.38
    CALORIES_WEIGHT_MULTIPLIER: int = 2
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1

    def __init__(self, action, duration, weight,
                 length_pool, count_pool) -> None:
        '''Помимо основных данных принмает дополнительные:
        1. Длина бассейна (length_pool)
        2. Сколько раз пользователь переплыл бассейн(count_pool)
        Так же переопределен показатель LEN_STEP
        '''

        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        '''Средняя скорость'''
        return (self.length_pool * self.count_pool / super().M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        '''Расчет потраченных калорий.'''
        return ((self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trening_type: dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in trening_type:
        raise ValueError('Неизвестный вид тренировки')
    return trening_type[workout_type](*data)


def main(trening_type: Training,) -> None:
    """Главная функция."""
    info = trening_type.show_training_info()
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
