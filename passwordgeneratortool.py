import tkinter as tk
import string as st
import pyperclip
import secrets
from tkinter import messagebox
import tkinter.filedialog
import os
import hashlib
import subprocess # 外部コマンドを実行するためにsubprocessモジュールをインポート
from tkinterdnd2 import DND_FILES, TkinterDnD # tkinterdnd2をインポート

# --- 7-Zip実行ファイルのフルパスをここで指定します ---
# お使いの環境に合わせて、適切なパスに修正してください。
# 例: C:\\Program Files\\7-Zip\\7z.exe
# 例: C:\\Program Files (x86)\\7-Zip\\7z.exe
# Windows以外のOSの場合は、それぞれのOSでの7zコマンドのフルパスを指定してください。
SEVEN_ZIP_EXE_PATH = r"C:\Program Files\7-Zip\7z.exe" 
# もし上記のパスで見つからない場合は、7z.exeがインストールされている実際のパスに置き換えてください。
# 例えば、64bit OSで32bit版の7-Zipをインストールしている場合は、
# SEVEN_ZIP_EXE_PATH = r"C:\Program Files (x86)\7-Zip\7z.exe" となることがあります。
# --- ここまで ---

def main():

    # メニューバーのcloseをクリックした際の処理
    def on_version():
        # versionを表示する
        messagebox.showinfo("バージョン","Ver:1.0.9") 

    # メニューバーのHelpをクリックした際の処理
    def on_help():
        # 使い方を表示
        messagebox.showinfo("ヘルプ","・パスワード生成ツールの使い方 \n 1.入力フィールドに1〜30の数値を入力できます。 \n 2.更新ボタンで表示されているパスワードを更新できます。 \n 3.コピーボタンでクリップボードにコピーされます。 \n 4.入力条件の変更ができます。(英字, 英字と数字 \n 先頭大文字,数字と記号)が選択できます。\n 5.デフォルトの設定に戻すには「リセット」ボタンを押してください。\n 6.ハッシュ値元を入力後、ハッシュ生成ボタンを入力するとハッシュ値が生成されます。\n\n・ZIPファイル生成機能 \n 1.「ファイルを選択」または「フォルダを選択」ボタンで圧縮したい対象を選択すると、自動的にZIPファイル生成ダイアログが開きます。\n 2. **ファイルをドラッグ＆ドロップすることでも、自動的にZIPファイル生成ダイアログが開きます。**\n 3.保存先とファイル名を指定（デフォルトで選択したファイル/フォルダ名が表示されます）し、「保存」をクリックすると、現在のパスワードでパスワード付きZIPファイルが作成されます。\n 4.生成されたZIPファイルのファイル名とパスワードは、下部の「ZIP生成履歴」に最新10件まで表示されます。\n 5. **ZIPファイル生成後、パスワードは自動的にクリップボードにコピーされます。**\n ") 

    # LettersOnlyのボタンが選択された際の処理
    def chk1():
        global checkFlg
        checkFlg = 1
        check2["state"] = "disable"
        check3["state"] = "disable"
        check4["state"] = "disable"
        return checkFlg
    
    # LettersAndNumbersOnlyのボタンが選択された際の処理
    def chk2():
        global checkFlg
        checkFlg = 2
        check1["state"] = "disable"
        check3["state"] = "disable"
        check4["state"] = "disable"
        return checkFlg
    
    # FirstCapitalLetterのボタンが選択された際の処理
    def chk3():
        global checkFlg
        checkFlg = 3
        check1["state"] = "disable"
        check2["state"] = "disable"
        check4["state"] = "disable"
        return checkFlg
    
    # SymbolsAndNumbersOnlyのボタンが選択された際の処理
    def chk4():
        global checkFlg
        checkFlg = 4
        check1["state"] = "disable"
        check2["state"] = "disable"
        check3["state"] = "disable"
        return checkFlg

    # Clearボタンがクリックされた際の処理 (リセット)
    def btn4_click():
        global checkFlg
        global selected_source_path 
        global zip_history # zip_historyもグローバル宣言

        check1["state"] = "normal" 
        check2["state"] = "normal"
        check3["state"] = "normal"
        check4["state"] = "normal"
        checkFlg = 0
        
        # 選択されたファイル/フォルダパスをクリアし、初期メッセージを表示
        selected_source_path = ""
        selected_path_entry.config(state='normal') # 一時的に編集可能にする
        selected_path_entry.delete(0, tk.END)
        selected_path_entry.insert(0, "ファイルまたはフォルダが選択されていません") # リセット後のメッセージ
        selected_path_entry.config(state='readonly') # 読み取り専用に戻す
        
        # ZIP履歴をクリアして表示を更新
        zip_history = []
        update_history_display()

        return checkFlg
    
    # パスワードをクリップボードにコピーする処理
    def copy_password_to_clipboard():
        # 1行目にあるパスワードをコピー
        copyin = text.get("1.0","end"+"-1c")

        # クリップボードに貼り付ける
        pyperclip.copy(copyin)
        messagebox.showinfo("メッセージ", "パスワードがクリップボードにコピーされました。(WindowsキーとVでコピー等の履歴が確認できます。)") 

    # ハッシュ生成ボタンがクリックされた際の処理
    def btn7_click():
        inputText2 = inpt2.get()
        if not inputText2:
            messagebox.showwarning("警告", "ハッシュ値元となる文字列を入力してください。")
            return
        hashre = hashlib.sha256(inputText2.encode()).hexdigest()
        pyperclip.copy(hashre)
        messagebox.showinfo("メッセージ","ハッシュ値" + "("+ hashre + ")" +"がクリップボードにコピーされました。") 

    # Entry入力ボックスの数値を判定
    def inputevent(event):
        try:
            inputText = inpt.get()
            # ''は無視
            if inputText == '':
                pass
            # 3桁以上はエラーメッセージを表示
            elif len(inputText) >= 3:
                messagebox.showinfo("エラーメッセージ", "正しい文字を入力してください。 (例 1 ～ 30)")
                inpt.delete(0, tk.END)
                # テキストの入力を有効
                text.configure(state='normal')
                # テキストをClear
                text.delete("1.0","end")
            
            # 最初に0が入力されたらエラーメッセージを表示
            elif int(inputText) == 0:
                messagebox.showinfo("エラーメッセージ", "正しい文字を入力してください。 (例 1 ～ 30)")
                inpt.delete(0, tk.END)
                # テキストの入力を有効
                text.configure(state='normal')
                # テキストをClear
                text.delete("1.0","end")
            
            # 31以上はエラーメッセージを表示
            elif int(inputText) >= 31:
                messagebox.showinfo("エラーメッセージ", "30字以内を入力してください。") 
                inpt.delete(0, tk.END)
                text.configure(state='disabled')
                # テキストの入力を有効
                text.configure(state='normal')
                # テキストをClear
                text.delete("1.0","end")
            
        except ValueError: # 数字以外が入力された場合
            messagebox.showinfo("エラーメッセージ", "正しい文字を入力してください。 (例 1 ～ 30)") 
            inpt.delete(0, tk.END)
            text.configure(state='disabled')
            # テキストの入力を有効
            text.configure(state='normal')
            # テキストをClear
            text.delete("1.0","end")

    # PasswordReloadクリック時の処理
    def btn_click():
        try:
            # テキストの入力を有効
            text.configure(state='normal')
            # テキストをClear
            text.delete("1.0","end")
            n = inpt.get()
    
            # 入力ボックスが空の場合エラーメッセージを表示
            if n == '':
                messagebox.showinfo("エラーメッセージ", "正しい文字を入力してください。 (例 1 ～ 30)") 
                inpt.delete(0, tk.END)
                text.configure(state='disabled')
            
            # 入力ボックスが31以上の場合エラーメッセージを表示
            elif int(n) >= 31:
                messagebox.showinfo("エラーメッセージ", "30字以内を入力してください。") 
                inpt.delete(0, tk.END)
                text.configure(state='disabled')
            
            # ランダムに文字を出力
            else:
                # Flgが1だったら文字だけ出力させる
                if checkFlg == 1:
                    text.insert('1.0', ''.join([secrets.choice(st.ascii_letters ) for i in range(int(n))]))
                # Flgが2だったら文字と数字のみ
                elif checkFlg == 2:
                    text.insert('1.0', ''.join([secrets.choice(st.ascii_letters + st.digits ) for i in range(int(n))]))
                    # テキストの入力を無効
                    text.configure(state='disabled')
                # Flgが3だったら先頭文字だけ大文字にする
                elif checkFlg == 3:
                    n_int = int(n)
                    if n_int > 0:
                        text.insert('1.0', secrets.choice(st.ascii_uppercase))
                        if n_int > 1:
                            text.insert('1.1', ''.join([secrets.choice(st.ascii_letters + st.digits + '!' + '#'+ '$' + '%' + '&' + ')' + '(' ) for i in range(n_int - 1)]))
                    # テキストの入力を無効
                    text.configure(state='disabled')
                # Flgが4だったら数字と記号だけにする
                elif checkFlg == 4:
                    text.insert('1.0', ''.join([secrets.choice(st.digits + '!' + '#'+ '$' + '%' + '&' + ')' + '(' ) for i in range(int(n))]))
                    # テキストの入力を無効
                    text.configure(state='disabled')
                else:
                    # 入力ボックスに入力された回数をランダムに格納された文字列を出力
                    text.insert('1.0', ''.join([secrets.choice(st.ascii_letters + st.digits + '!' + '#'+ '$' + '%' + '&' + ')' + '(' ) for i in range(int(n))]))
                    # テキストの入力を無効
                    text.configure(state='disabled')
        except ValueError: # 不正な文字列が入力された場合
            messagebox.showinfo("エラーメッセージ", "正しい文字を入力してください。 (例 1 ～ 30)") 
            inpt.delete(0, tk.END)
            text.configure(state='disabled')

    ## PasswordCopyのボタンのエンター押下イベント処理
    def Enter_hand2(event):
        copy_password_to_clipboard()
    
    ## PasswordReloadのボタンのエンター押下処理
    def Enter_hand(event):
        btn_click()
    
    # 各オプションボタンのEnter押下処理
    def Enter_hand3(event):
        chk1()
    def Enter_hand4(event):
        chk2()
    def Enter_hand5(event):
        chk3()
    def Enter_hand6(event):
        chk4()
    def Enter_hand7(event):
        btn4_click()
    def Enter_hand9(event):
        btn7_click()

    # 選択されたファイル/フォルダのパスを保持する変数
    selected_source_path = ""

    # ZIP生成履歴表示を更新する関数
    def update_history_display():
        history_text_widget.config(state='normal') # 編集可能にする
        history_text_widget.delete('1.0', tk.END) # 既存のテキストをクリア
        if not zip_history:
            history_text_widget.insert(tk.END, "履歴はありません。")
        else:
            # 最新の10件を逆順（最新が上）で表示
            for i, entry in enumerate(reversed(zip_history)): 
                history_text_widget.insert(tk.END, f"{i+1}. ファイル: {entry['filename']}\n   パスワード: {entry['password']}\n\n")
        history_text_widget.config(state='disabled') # 編集不可に戻す

    # パスワード付きZIPファイルを生成する処理 (subprocessを使用)
    def generate_password_protected_zip():
        global selected_source_path 
        if not selected_source_path:
            messagebox.showwarning("警告", "圧縮するファイルまたはフォルダを選択してください。")
            return

        # 追加: 選択されたパスが存在するか確認
        if not os.path.exists(selected_source_path):
            messagebox.showerror("エラー", f"選択されたファイルまたはフォルダが存在しません:\n{selected_source_path}\n\nパスをクリアして再選択してください。")
            # Clear the invalid path from the entry and variable
            selected_source_path = ""
            selected_path_entry.config(state='normal')
            selected_path_entry.delete(0, tk.END)
            selected_path_entry.insert(0, "ファイルまたはフォルダが選択されていません")
            selected_path_entry.config(state='readonly')
            return

        password = text.get("1.0", "end-1c")
        if not password:
            messagebox.showwarning("警告", "パスワードが生成されていません。先にパスワードを生成してください。")
            return
        
        # パスワードが短すぎる場合の警告（任意）
        if len(password) < 8: # 例えば8文字未満を短いと判断
            messagebox.showwarning("警告", "生成されたパスワードが短すぎます。セキュリティのため、より長いパスワードを推奨します。")


        # 選択されたファイル/フォルダの名前をデフォルトのファイル名として設定 (拡張子なし)
        initial_filename_without_ext = os.path.splitext(os.path.basename(selected_source_path))[0]

        # ZIPファイルの保存先とファイル名を選択
        output_zip_path = tkinter.filedialog.asksaveasfilename(
            title="ZIPファイルを保存",
            defaultextension=".zip", # デフォルト拡張子を.zipに変更
            filetypes=[("Zipファイル", "*.zip")], # ファイルタイプをZipファイルに変更
            initialfile=initial_filename_without_ext # デフォルトのファイル名を拡張子なしで指定
        )

        if not output_zip_path:
            messagebox.showwarning("キャンセル", "ZIPファイルの保存がキャンセルされました。")
            return # キャンセルされた場合はここで終了

        try:
            # 7zコマンドのパスを、定義したフルパスの変数から取得
            seven_zip_command = SEVEN_ZIP_EXE_PATH 

            # 7zコマンドの引数を構築
            # 'a' はアーカイブに追加、'-p' はパスワード、'-tzip' はZIP形式を指定
            command_args = [
                seven_zip_command,
                "a",
                "-tzip", # ZIP形式を指定
                "-p" + password,
                output_zip_path,
                selected_source_path
            ]
            
            # デバッグ用にコマンド引数を出力
            print(f"Executing command: {command_args}")

            # subprocess.runで外部コマンドを実行
            # capture_output=True: 標準出力と標準エラーをキャプチャ
            # text=True: 出力をテキストとしてデコード
            # check=True: ゼロ以外の終了コードでCalledProcessErrorを発生させる
            result = subprocess.run(command_args, capture_output=True, text=True, check=True)

            # 成功メッセージを簡素化
            messagebox.showinfo("成功", "パスワード付きzipファイルが生成されました。")

            # ZIP生成履歴に追加
            if len(zip_history) >= 10:
                zip_history.pop(0) # 最も古いエントリを削除
            zip_history.append({"filename": os.path.basename(output_zip_path), "password": password})
            update_history_display() # 履歴表示を更新

            # 生成されたパスワードをクリップボードにコピー
            pyperclip.copy(password)
            # messagebox.showinfo("コピー完了", "生成されたパスワードがクリップボードにコピーされました。") # この行を削除

        except FileNotFoundError:
            messagebox.showerror("エラー", f"7zコマンドが見つかりません。\n指定されたパス '{SEVEN_ZIP_EXE_PATH}' に7-Zipの実行ファイルが存在するか確認してください。")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("エラー", f"7zコマンドの実行中にエラーが発生しました。\nエラーコード: {e.returncode}\n標準出力:\n{e.stdout}\n標準エラー:\n{e.stderr}")
        except Exception as e:
            messagebox.showerror("エラー", f"予期せぬエラーが発生しました:\n{e}")

    # ファイル選択ダイアログを表示し、選択されたパスを更新
    def select_file():
        global selected_source_path 
        filepath = tkinter.filedialog.askopenfilename(
            title="ファイルを選択",
            filetypes=[("すべてのファイル", "*.*")]
        )
        if filepath:
            selected_source_path = filepath
            selected_path_entry.config(state='normal') # 一時的に編集可能にする
            selected_path_entry.delete(0, tk.END)
            selected_path_entry.insert(0, selected_source_path)
            selected_path_entry.config(state='readonly') # 読み取り専用に戻す
            generate_password_protected_zip() # ファイル選択後、自動的にZIP生成を開始
        else:
            messagebox.showwarning("キャンセル", "ファイルの選択がキャンセルされました。")

    # フォルダ選択ダイアログを表示し、選択されたパスを更新
    def select_folder():
        global selected_source_path 
        folderpath = tkinter.filedialog.askdirectory(
            title="フォルダを選択"
        )
        if folderpath:
            selected_source_path = folderpath
            selected_path_entry.config(state='normal') # 一時的に編集可能にする
            selected_path_entry.delete(0, tk.END)
            selected_path_entry.insert(0, selected_source_path)
            selected_path_entry.config(state='readonly') # 読み取り専用に戻す
            generate_password_protected_zip() # フォルダ選択後、自動的にZIP生成を開始
        else:
            messagebox.showwarning("キャンセル", "フォルダの選択がキャンセルされました。")

    # ドラッグ＆ドロップイベントハンドラ
    def handle_drop(event):
        global selected_source_path
        # ドロップされたパスは { } で囲まれている場合があるため、除去する
        # また、複数のファイルがドロップされた場合、スペースで区切られるため、最初のパスのみを処理
        dropped_path_raw = event.data
        
        # Windowsのパスは通常 "C:/path/to/file" のようにスラッシュ区切りで、
        # ドロップされたデータは "{C:/path/to/file}" のように中括弧で囲まれていることがある。
        # また、複数のファイルがドロップされた場合は "{path1} {path2}" のようになる。
        # ここでは最初のパスのみを抽出し、中括弧があれば除去する。
        if dropped_path_raw.startswith('{') and dropped_path_raw.endswith('}'):
            dropped_path = dropped_path_raw[1:-1] # 中括弧を除去
        else:
            dropped_path = dropped_path_raw

        # 複数のパスがスペースで区切られている場合、最初のパスのみを取得
        if ' ' in dropped_path and os.path.exists(dropped_path.split(' ')[0]):
            selected_source_path = dropped_path.split(' ')[0]
        else:
            selected_source_path = dropped_path

        # パスがファイルまたはフォルダとして存在するか最終確認
        if os.path.exists(selected_source_path):
            selected_path_entry.config(state='normal')
            selected_path_entry.delete(0, tk.END)
            selected_path_entry.insert(0, selected_source_path)
            selected_path_entry.config(state='readonly')
            generate_password_protected_zip()
        else:
            messagebox.showwarning("エラー", f"無効なパスがドロップされました: {selected_source_path}")


    # オプション用のグローバル変数
    global checkFlg
    checkFlg = 0
    
    # ZIP履歴を保持するグローバル変数
    global zip_history
    zip_history = []

    # TKクラスのインスタンス化 (tkinterdnd2を使用)
    window = TkinterDnD.Tk() # ここを修正

    # ウィンドウの変更を無効
    window.resizable(False, False)

    # フレームのタイトルを決める
    window.title("PasswordGeneratorTool") # タイトルも変更

    # フレームの幅を選択する (新しい機能に合わせてサイズを調整)
    window.geometry("700x400") # ウィンドウの高さを400に拡張

    # ドラッグ＆ドロップのターゲットとしてウィンドウを設定
    window.drop_target_register(DND_FILES)
    window.dnd_bind('<<Drop>>', handle_drop)

    # menの変数にtk.Menuをインスタンス化し代入
    men = tk.Menu(window)
    window.config(menu=men)

    # メニューバーにVersion,Helpの項目を追加
    men.add_command(label='バージョン',command=on_version)
    men.add_command(label='ヘルプ',command=on_help)

    # 入力できるテキストの生成 (パスワード表示用)
    text = tk.Text()
    
    # ウイジェットの生成
    text.place(width=350,height=19,x=2,y=2)

    # フレーム内に入力テキストを生成 (パスワード長入力用)
    inpt = tk.Entry(width=4)

    # 入力ボックスのボタン配置設定
    inpt.place(x=10, y=30)

    # 入力ボックスに15を表示する
    inpt.insert(0,"15")

    # ハッシュ値専用:フレーム内に入力テキストを生成
    inpt2 = tk.Entry(width=50)

    # ハッシュ値専用:入力ボックスのボタン配置設定
    inpt2.place(x=370, y=2)

    # ハッシュ値専用:入力ボックスにハッシュ値元を入力を表示する
    inpt2.insert(0,"ハッシュ値元を入力")
    
    # 入力ボックスに入力された文字を判定
    inpt.bind("<KeyRelease>",inputevent)

    # テキストに15回ランダムに格納された文字列を出力
    text.insert('1.0', ''.join([secrets.choice(st.ascii_letters + st.digits + '!' + '#'+ '$' + '%' + '&' + ')' + '(' ) for i in range(15)]))

    # フレーム内にパスワード更新ボタンを生成
    btn = tk.Button(window, text='更新', command=btn_click)

    # PasswordReloadのボタン配置設定
    btn.place(x=45, y=30)

    # フレーム内にコピーボタンを生成
    btn2 = tk.Button(window, text='コピー', command=copy_password_to_clipboard)

    # PasswordCopyのボタン配置設定
    btn2.place(x=85, y=30)

    # オプションボタンを生成
    check1 = tk.Button(window, text='英字', command=chk1)
    check1.place(x=10,y=72)

    check2 = tk.Button(window, text='英字と数字', command=chk2)
    check2.place(x=50,y=72)

    check3 = tk.Button(window, text='先頭大文字', command=chk3)
    check3.place(x=122,y=72)

    check4 = tk.Button(window, text='記号と数字', command=chk4)
    check4.place(x=196,y=72)

    # Resetボタンを生成
    btn4 = tk.Button(window, text='リセット', command=btn4_click)
    btn4.place(x=268, y=72)

    # ハッシュ生成ボタン生成
    btn7 = tk.Button(window, text='ハッシュ値生成', command=btn7_click)
    btn7.place(x=370, y=30)

    # --- 新しいZIP機能のUI要素 ---
    # 選択されたファイル/フォルダパス表示用Entry
    selected_path_label = tk.Label(window, text="選択パス:")
    selected_path_label.place(x=10, y=120)
    selected_path_entry = tk.Entry(window, width=80)
    selected_path_entry.place(x=70, y=120)
    selected_path_entry.config(state='normal') # 一時的に編集可能にする
    selected_path_entry.insert(0, "ファイルまたはフォルダが選択されていません") # 初期メッセージ
    selected_path_entry.config(state='readonly') # 読み取り専用に戻す

    # ファイル選択ボタン
    select_file_btn = tk.Button(window, text='ファイルを選択', command=select_file)
    select_file_btn.place(x=10, y=150)

    # フォルダ選択ボタン
    select_folder_btn = tk.Button(window, text='フォルダを選択', command=select_folder)
    select_folder_btn.place(x=100, y=150)

    # ZIP生成ボタン (手動トリガーとして残す)
    #generate_zip_btn = tk.Button(window, text='ZIP生成 (手動)', command=generate_password_protected_zip) 
    #generate_zip_btn.place(x=200, y=150)

    generate_zip_btn2 = tk.Button(window, text='【フォルダまたはファイルをドラック＆ドロップでもzipファイルを生成できます。】', command="") 
    generate_zip_btn2.place(x=200, y=150)
    # --- 新しいZIP機能のUI要素ここまで ---

    # ZIP生成履歴表示エリア
    history_label = tk.Label(window, text="ZIP生成履歴 (最新10件):")
    history_label.place(x=10, y=190)
    history_text_widget = tk.Text(window, width=80, height=10, state='disabled', wrap='word')
    history_text_widget.place(x=10, y=210)
    
    # 初期履歴表示
    update_history_display()

    # PasswordReload,PasswordCopyと各オプションボタンのEnter押下時のバインド処理
    btn.bind("<Return>",Enter_hand)
    btn2.bind("<Return>",Enter_hand2)
    check1.bind("<Return>",Enter_hand3)
    check2.bind("<Return>",Enter_hand4)
    check3.bind("<Return>",Enter_hand5)
    check4.bind("<Return>",Enter_hand6)
    btn4.bind("<Return>",Enter_hand7)
    btn7.bind("<Return>",Enter_hand9)
    # 新しいボタンのEnter押下処理
    select_file_btn.bind("<Return>", lambda event: select_file())
    select_folder_btn.bind("<Return>", lambda event: select_folder())
    #generate_zip_btn.bind("<Return>", lambda event: generate_password_protected_zip())


    # テキストの入力を無効
    text.configure(state='disabled')

    # ウィンドウを開いたままにして待機
    window.mainloop()

if __name__ == '__main__':
    main()
