# B223586 津田 陸斗

class Food:
    def __init__(self, name, calorie_per_100g):
        self.name = name
        self.calorie_per_100g = calorie_per_100g

    def __str__(self):
        return f"{self.name}: {self.calorie_per_100g} kcal/100g"


class CalorieCalculator:
    def __init__(self):
        self.foods = []

    def print_foods(self):
        print("--食品名一覧--")
        for food in self.foods:
            print(food)

    def register_food(self):
        name = input("食品名を入力してください: ")
        calorie = float(input("その食品のカロリーを入力してください [kcal/100g]: "))
        new_food = Food(name, calorie)
        self.foods.append(new_food)

    def calculate_total_calorie(self):
        selected_foods = []
        grams = []
        while True:
            self.print_foods()
            food_name = input("食品名（endで計算）: ")
            if food_name == "end":
                break
            gram = float(input("グラム数: "))
            selected_foods.append(food_name)
            grams.append(gram)

        total_calorie = 0.0
        for i in range(len(selected_foods)):
            for food in self.foods:
                if food.name == selected_foods[i]:
                    total_calorie += food.calorie_per_100g * (grams[i] / 100.0)
        print(f"総カロリーは {total_calorie} kcalです．")


def main():
    calculator = CalorieCalculator()
    initial_foods = [("米飯", 150.0), ("中華麺", 57.1), ("そば", 133.3), ("うどん", 100.0), ("素麺", 133.3), ("食パン", 250.0), ("いちご", 33.0)]
    
    for name, calorie in initial_foods:
        calculator.foods.append(Food(name, calorie))

    while True:
        mode = int(input("登録は1を，計算は2を，終了は0を入力してください: "))
        if mode == 1:
            calculator.print_foods()
            calculator.register_food()
        elif mode == 2:
            calculator.calculate_total_calorie()
        elif mode == 0:
            break

if __name__ == "__main__":
    main()
