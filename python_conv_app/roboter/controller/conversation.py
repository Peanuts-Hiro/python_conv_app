"""Controller for speaking with robot"""
from roboter.models import robot

#2. talk_about_restaurant関数が呼び出されたことで、配下の各メソッドが順番に呼び出される
def talk_about_restaurant():
    """Function to speak with robot"""
    # RestaurantRobotクラスのオブジェクトを生成
    restaurant_robot = robot.RestaurantRobot()
    # RestaurantRobotクラスのメソッドを順番に呼び出す → robot.pyへ
    restaurant_robot.hello()
    restaurant_robot.recommend_restaurant()
    restaurant_robot.ask_user_favorite()
    restaurant_robot.thank_you()

