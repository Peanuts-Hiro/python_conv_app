"""Generates ranking model to write to CSV
"""
import collections
import csv
import os
import pathlib


RANKING_COLUMN_NAME = 'NAME'
RANKING_COLUMN_COUNT = 'COUNT'
RANKING_CSV_FILE_PATH = 'ranking.csv'

# CSVモデルの基本クラス
class CsvModel(object):
    """Base csv model."""
    # 引数csv_fileで、RankingModelクラスのコンストラクタからCSVファイルのパスを受け取る
    def __init__(self, csv_file):
        self.csv_file = csv_file
        if not os.path.exists(csv_file): # 受け取ったパスにCSVファイルが存在しない場合
            pathlib.Path(csv_file).touch() # 空のファイルを作成

# CsvModelクラスを継承し、ランキングデータの読み書きを行う
class RankingModel(CsvModel):
    """Definition of class that generates ranking model to write to CSV"""
    def __init__(self, csv_file=None, *args, **kwargs):
        # csv_file がNone（何も渡されていない）の場合、次のステップへ
        # csv_file に値が渡されている場合は、その値をそのままCSVファイルのパスとして使用
        if not csv_file: # csv_file がNoneの場合
            csv_file = self.get_csv_file_path() # self.get_csv_file_path() メソッドが呼び出され、CSVファイルのパスを取得
        # 取得されたcsv_fileの値を、親クラスであるCsvModelのコンストラクタに渡して呼び出す
        super().__init__(csv_file, *args, **kwargs)
        self.column = [RANKING_COLUMN_NAME, RANKING_COLUMN_COUNT] # self.column に、CSV ファイルのカラム名 (名前とカウント) をリスト形式で代入
        self.data = collections.defaultdict(int) # キー(NAME)が存在しない場合に、デフォルト値として0が設定される辞書
        self.load_data() # CSV ファイルからランキングデータを読み込み、self.data に格納

    def get_csv_file_path(self):
        """Set csv file path.

        Use csv path if set in settings, otherwise use default
        """
        csv_file_path = None
        # try-except ブロックを使用して、settings モジュールをインポートすることを試みる
        try:
            import settings
            # settings モジュールのインポートに成功し、settings.CSV_FILE_PATH が設定されている場合
            if settings.CSV_FILE_PATH:
                csv_file_path = settings.CSV_FILE_PATH # 設定されている値を csv_file_path に代入
        except ImportError:
            pass

        # settings モジュールのインポートに失敗した場合、もしくはsettings.CSV_FILE_PATH が設定されていない場合
        if not csv_file_path:
            csv_file_path = RANKING_CSV_FILE_PATH # RANKING_CSV_FILE_PATH というデフォルトのパスを csv_file_path に代入
        return csv_file_path

    # CSVファイルからランキングデータを読み込み、辞書型 (dict) として返却する
    def load_data(self):
        """Load csv data.

        Returns:
            dict: Returns ranking data of dict type.
        """
        # self.csv_file (コンストラクタで取得したCSVファイルのパス) を 'r+' モードで開く
        with open(self.csv_file, 'r+') as csv_file:
            # CSV 読み込みのため csv.DictReader の利用
            reader = csv.DictReader(csv_file) # DictReader は、CSV ファイルを辞書型のオブジェクトとして扱うための機能を提供
            for row in reader: # row は、各行のデータを辞書型で保持している
                # 現在の行の NAME カラムと、COUNT カラムの値を取得し、self.data 辞書に格納
                self.data[row[RANKING_COLUMN_NAME]] = int(
                    row[RANKING_COLUMN_COUNT])
        return self.data

    # self.data 辞書に格納されているランキングデータを、CSV ファイルに保存する
    def save(self):
        """Save data to csv file."""
        # self.csv_file (コンストラクタで取得したCSVファイルのパス) を 'w+' モードで開く
        with open(self.csv_file, 'w+') as csv_file:
            # CSV 書き込みのため csv.DictWriter の利用
            # DictWriter は、辞書型のデータを CSV ファイルに書き込むための機能を提供
            writer = csv.DictWriter(csv_file, fieldnames=self.column) # fieldnames 引数には、ヘッダー行の列名リスト (self.column) を指定
            writer.writeheader() # CSV ファイルのヘッダー行を書き込む

            for name, count in self.data.items():
                # 辞書型のオブジェクトを作成し、writer.writerow メソッドに渡すことで、現在の行のデータを CSV ファイルに書き込む
                writer.writerow({
                    RANKING_COLUMN_NAME: name,
                    RANKING_COLUMN_COUNT: count
                })

    # ランキングデータの中から 最も人気のある データを取得
    def get_most_popular(self, not_list=None): # not_list :除外したい項目名のリストを渡す(初期値はNone)
        """Fetch the data of the top most ranking.

        Args:
            not_list (list): Excludes the name on the list.

        Returns:
            str: Returns the data of the top most ranking
        """
        if not_list is None: # not_list が渡されなかった場合
            not_list = [] # デフォルトで空のリスト [] が設定

        # ランキングデータが空の場合は、None を返す
        if not self.data:
            return None

        # ランキングデータを 降順 にソート
        # ソート基準を self.data.get メソッドによって取得される値に設定
        sorted_data = sorted(self.data, key=self.data.get, reverse=True)
        # ソートされたデータの中から、除外リスト not_list に含まれている名前はスキップ
        for name in sorted_data:
            if name in not_list:
                continue
            return name # 除外リストに含まれていない、一番目のデータを返す

    # 特定のレストランのカウントを１上げる
    def increment(self, name):
        """Increase rank for the give name."""
        # data(NAME,COUNT)の特定の NAME の COUNT を１上げる
        self.data[name.title()] += 1
        self.save()
