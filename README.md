# python_conv_app
pythonでMVCモデルに則った開発その１

[実装概要]
ターミナル上で実行する前提。
ユーザーの入力内容を、CSVファイルで保持・更新する流れを学習したため、デモアプリとして追記。
具体的な体験としては、以下の流れです。
1. (初回のみ)ユーザーにお勧めのレストランを聞き、そのデータを【レストラン名：回数】の形式で、回数の降順でCSVファイルに保存
2. 同じもしくは他のユーザーがこのアプリを利用する際、CSVファイルに保持されている回数が最も多い（＝最もお勧めの）レストランをユーザーに提案
3. 提案したレストランをユーザーが気に入った場合は回数を１つ追加、気に入らなかった場合は次に回数の多いレストランを提案
4. 提案したレストランのいずれも気に入らなかった場合、お勧めのレストランをヒアリングし、CSVファイルに同じ形式でレコード追加
