"""Utils to display to be returned to the user on the console."""
import os
import string

import termcolor


# テンプレートディレクトリのパスを取得
def get_template_dir_path():
    """Return the path of the template's directory.

    Returns:
        str: The template dir path.
    """
    template_dir_path = None
    try:
        import settings
        # 設定ファイル (settings.py) から TEMPLATE_PATH が定義されている場合
        if settings.TEMPLATE_PATH:
            # 設定ファイルが存在し、TEMPLATE_PATH が定義されていれば、そのパスを返す
            template_dir_path = settings.TEMPLATE_PATH
    except ImportError:
        pass
        # 設定ファイルが存在しない、または TEMPLATE_PATH が定義されていない場合
    if not template_dir_path:
        # 現在の実行ファイルの親ディレクトリの親ディレクトリを取得して、
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # その下に templates ディレクトリがあるものとしてパスを生成する
        template_dir_path = os.path.join(base_dir, 'templates')

    return template_dir_path # 生成したパスを返す


# テンプレートファイルが見つからない場合に発生する例外クラス
class NoTemplateError(Exception):
    """No Template Error"""

# 指定されたテンプレートファイルを探す
def find_template(temp_file):
    """Find for template file in the given location.

    Returns:
        str: The template file path

    Raises:
        NoTemplateError: If the file does not exists.
    """
    # テンプレートディレクトリのパスを取得
    template_dir_path = get_template_dir_path()
    # 引数で受け取った temp_file (テンプレートファイル名) と結合してファイルパスを生成
    temp_file_path = os.path.join(template_dir_path, temp_file)
    # ファイルが存在しない場合
    if not os.path.exists(temp_file_path):
        # NoTemplateError 例外を発生させる
        raise NoTemplateError('Could not find {}'.format(temp_file))
    # ファイルが存在すれば、ファイルパスの文字列を返す
    return temp_file_path


# テンプレートファイルの内容を読み込み、string.Template オブジェクトとして返
def get_template(template_file_path, color=None):
    """Return the path of the template.

    Args:
        template_file_path (str): The template file path
        color: (str): Color formatting for output in terminal
            See in more details: https://pypi.python.org/pypi/termcolor

    Returns:
        string.Template: Return templates with characters in templates.
    """
    # 引数で受け取った template_file_path を使って、find_template 関数でファイルの存在を確認し、パスを取得
    template = find_template(template_file_path)
    # ファイルを開き、内容を読み込む
    with open(template, 'r', encoding='utf-8') as template_file:
        contents = template_file.read()
        # 改行文字 (os.linesep) を削除 (rstrip)
        contents = contents.rstrip(os.linesep)
        # 区切り文字 (等号60個 * 3行) で囲む
        contents = '{splitter}{sep}{contents}{sep}{splitter}{sep}'.format(
            contents=contents, splitter="=" * 60, sep=os.linesep) # sep=os.linesep: sep 変数に、現在のOSの改行コードを代入
        contents = termcolor.colored(contents, color)
        return string.Template(contents)


# get_templateメソッドについて
# Q. 'r'でファイルを開いているのに、文字列の操作をしている理由は？
# A. 文字列操作はメモリ上で行われるため、読み込んだファイルの内容を直接変更していない

# Q. 改行文字を削除した後に、改行文字を追加している理由は？
# A. 既存の改行文字をすべて削除することで、プラットフォームに依存しない状態にする