import roboter.controller.conversation

#1. talk_about_restaurant関数を実行する → conversation.pyへ

def main():
    roboter.controller.conversation.talk_about_restaurant()

if __name__ == '__main__':
    main()
    
#読む順番
#1. main.pyがconversation.pyのtalk_about_restaurant関数を実行する
#2. talk_about_restaurant関数には、処理の順番が記述されている ←役割：コントローラー
#   処理の順番 : hello関数、recommend_restaurant関数、ask_favorite_food関数、thank_you関数 ←役割：モデル
#3. 具体的な処理について書いてある上記の関数たちの内容を理解する
#4. console.pyでユーザーが実際に見ている画面について理解する ←役割：ビュー