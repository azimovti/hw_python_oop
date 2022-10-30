class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,training_type: str,
                 duration: float,
                 distance:float,
                 speed:float,
                 calories:float):
                 
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed 
        self.calories = calories 

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration} ч.; '
                f'Дистанция: {self.distance} км; '
                f'Ср. скорость: {self.speed} км/ч; '
                f'Потрачено ккал: {self.calories}. ') 

class Training:
    """Базовый класс тренировки."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    LEN_STEP: float = 0.65                     
    M_IN_KM: int = 1000                      

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * Training.LEN_STEP) / Training.M_IN_KM 

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance()/self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories()) # Объекты класса InfoMessage создаются вызовом 
        return info_message

class Running(Training):
    """Тренировка: бег."""
    def __init__(self,action,weight,duration):
        super().__init__(action,weight,duration)     

    def get_spent_calories(self):

        return ((super().CALORIES_MEAN_SPEED_MULTIPLIER * 
        super().get_mean_speed() + super().CALORIES_MEAN_SPEED_SHIFT)
        * self.weight / super().M_IN_KM * self.duration)  
    
 

class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    F_DEF_VALUE = 0.035
    S_DEF_VALUE = 0.029

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        
        self.height = height #рост спортсмена

    def get_spent_calories(self):
        return (self.F_DEF_VALUE * self.height + (super().get_mean_speed()**2 // self.height
                * self.S_DEF_VALUE * self.weight) * self.duration)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    VAL_ONE:float = 1.1
    VAL_TWO:int = 2

    def __init__(self,action,duration,weight,length_pool,count_pool):

        super().__init__(action,duration,weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        
    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / super().M_IN_KM / self.duration)

    def get_spent_calories(self):

        return (self.get_mean_speed() + self.VAL_ONE * 
                self.VAL_TWO * self.weight * self.duration)

def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trening_type: dict[str,Training] = {
            'SWM': Swimming,
            'RUN': Running,
            'WLK': SportsWalking
    }

    return trening_type[workout_type](*data)        
    
        


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
        if training is None:
            print('Неизвестный вид тренировки')
        else:
            main(training)
