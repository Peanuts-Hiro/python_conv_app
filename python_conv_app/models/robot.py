"""Defined a robot model """
from roboter.models import ranking
from roboter.views import console


DEFAULT_ROBOT_NAME = 'Roboko'


class Robot(object):
    """Base model for Robot."""
    # ロボットの基本的な動作を定義する基底クラス。
    # 挨拶やユーザー名の設定などの共通的な機能を提供(※user_nameはユーザーによる入力内容が入るため初期値は空白)
    def __init__(self, name=DEFAULT_ROBOT_NAME, user_name='',
                 speak_color='green'):
        self.name = name # self.nameに'Roboko'を保持
        self.user_name = user_name # self.user_nameは、最初は空白
        self.speak_color = speak_color # self.speak_colorは、'green'を保持

# ロボットの名前、ユーザー名、話す際のテキストカラーを設定
    # hello.txtのベースに基づいてユーザーに挨拶し、ユーザー名を登録する処理内容を記載
    def hello(self): # ←ここのselfは上記__init__で定義したselfを引き継いでいる
        """Returns words to the user that the robot speaks at the beginning."""
        while True:
            # console.pyのget_template関数を使い、挨拶のテンプレートをオブジェクト化
            template = console.get_template('hello.txt', self.speak_color) #ユーザーに表示するテキストカラーに__init__で定義した'green'を代入
            # hello.txt内のrobot_nameに'Roboko'を代入したものをユーザーに表示
            user_name = input(template.substitute({ # substitute() :文字列テンプレート内の特定の文字列を置き換える
                'robot_name': self.name}))
            # user_nameに値が入っている場合に実行する
            if user_name:
                # user_nameをtitle()で先頭大文字にして、self_user_nameに格納
                self.user_name = user_name.title() #title() : 単語ごとの最初の文字を大文字、以降は小文字
                break


# Robotクラスを継承し、レストラン推薦に特化した機能を追加したクラス。
# ユーザーにレストランを推薦したり、ユーザーのお気に入りのレストランを登録したりする機能を提供
class RestaurantRobot(Robot): # robotクラスで定義した変数を引数として継承
    """Handle data model on restaurant."""

    def __init__(self, name=DEFAULT_ROBOT_NAME): # ←ここのself_nameは上記__init__で定義したself_nameを引き継いでいる
        # 親クラスであるRobotクラスのコンストラクタ(__init__)を呼び出し、Robotクラスの初期化処理を実行している。
        # つまり、RestaurantRobotクラスのインスタンスは、Robotクラスのインスタンスとしても動作するようになる。
        # コンストラクタ: オブジェクトが生成されるときに最初に呼ばれる特殊メソッド
        super().__init__(name=name)
        # RankingModelクラスでは、ランキングデータの読み込み、保存、上位項目の取得、カウントの更新などの機能を提供(→ranking.pyを参照)
        self.ranking_model = ranking.RankingModel() 

    # 後続のメソッド(recommend_restaurantメソッドetc)を呼び出す前に、
    # ユーザー名が設定されていない場合はhelloメソッドを呼び出すためのデコレータ
    # デコレータにしている理由は、後続のメソッドの実行前にユーザー名を指定しなければならないため
    def _hello_decorator(func):
        """Decorator to say a greeting if you are not greeting the user."""
        def wrapper(self):
            if not self.user_name: # ユーザー名が設定されていないかどうかを確認
                self.hello() #ユーザー名が設定されていない場合、self.hello() を呼び出す
            return func(self) # 元の関数 func を呼び出し、その戻り値を返す
        return wrapper

    # ランキングモデルに基づいてレストランを推薦
    # ユーザーが推薦されたレストランを気に入ったかどうかを聞き、気に入らなければ別のレストランを推薦
    @_hello_decorator # recommend_restaurant 関数が呼ばれる前に、hello_decoratorを呼び出して、ユーザー名が設定されているか確認
    def recommend_restaurant(self):
        """Show restaurant recommended restaurant to the user."""
        # ランキングモデルから最も人気のあるレストランを取得
        new_recommend_restaurant = self.ranking_model.get_most_popular()
        if not new_recommend_restaurant:
            return None

        # 取得したレストランをユーザーに提示し、気に入ったかどうかを尋ねる
        will_recommend_restaurants = [new_recommend_restaurant]
        while True:
            # console.pyのget_template関数を使い、挨拶のテンプレートをオブジェクト化
            template = console.get_template('greeting.txt', self.speak_color)
            is_yes = input(template.substitute({
                'robot_name': self.name,
                'user_name': self.user_name,
                'restaurant': new_recommend_restaurant
            }))
            # ユーザーが「はい」と答えた場合は、処理を終了
            if is_yes.lower() == 'y' or is_yes.lower() == 'yes':
                break

            # ユーザーが「いいえ」と答えた場合は、すでに推薦したレストランを除外して、
            # 再度ランキングモデルからレストランを取得し、再度ユーザーに尋ねる
            if is_yes.lower() == 'n' or is_yes.lower() == 'no': # ユーザーの入力値が「n」か「no」かを小文字に変換して比較
                # ランキングモデルから新しいレストランを取得
                new_recommend_restaurant = self.ranking_model.get_most_popular(
                    not_list=will_recommend_restaurants) # すでに推薦済みのレストランは候補から除外(ranking.pyを参照)
                # 新しいレストランが見つからなかった場合（つまり、すべてのレストランをすでに推薦済みだった場合）
                if not new_recommend_restaurant: 
                    break # 処理を終了
                # 新しいレストランが見つかった場合は、will_recommend_restaurants リストにそのレストランを追加   
                will_recommend_restaurants.append(new_recommend_restaurant)

    # ユーザーから好きなレストランを聞き、ランキングモデルに登録
    @_hello_decorator # ask_user_favorite 関数が呼ばれる前に、hello_decoratorを呼び出して、ユーザー名が設定されているか確認
    def ask_user_favorite(self):
        """Collect favorite restaurant information from users."""
        while True:
            # ユーザーに好きなレストランを尋ねるためのテンプレートを読み込み
            template = console.get_template(
                'which_restaurant.txt', self.speak_color)
            # ユーザーに入力されたレストランの名前を取得
            restaurant = input(template.substitute({
                'robot_name': self.name,
                'user_name': self.user_name,
            }))
            if restaurant: # ユーザーが入力した値が空でないことを確認
                # ユーザーが入力したレストラン名のCOUNTを１上げる(ranking.py incrementメソッドを参照)
                self.ranking_model.increment(restaurant) 
                break

    @_hello_decorator # thank you 関数が呼ばれる前に、hello_decoratorを呼び出して、ユーザー名が設定されているか確認
    # ユーザーに感謝の言葉を伝える
    def thank_you(self):
        """Show words of appreciation to users."""
        # ユーザーに感謝の言葉を伝えるためのテンプレートを読み込み
        template = console.get_template('good_by.txt', self.speak_color)
        print(template.substitute({
            'robot_name': self.name,
            'user_name': self.user_name,
        }))
