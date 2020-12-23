import tkinter as tk
import string as st
import pyperclip
import secrets
from tkinter import messagebox

def main():

    #メニューバーのcloseをクリックした際の処理
    def on_version():
        #versionを表示する
        messagebox.showinfo("バージョン","Ver:1.0.3") 

    #メニューバーのHelpをクリックした際の処理
    def on_help():
        #使い方を表示
        messagebox.showinfo("ヘルプ","・パスワード生成ツールの使い方 \n 1.入力フィールドに1〜30の数値を入力できます。 \n 2.更新ボタンで表示されているパスワードを更新できます。 \n 3.コピーボタンでクリップボードにコピーされます。 \n 4.入力条件の変更ができます。(英字, 英字と数字 \n 先頭大文字,数字と記号)が選択できます。\n 5.デフォルトの設定に戻すには「リセット」ボタンを押してください。") 

    #LettersOnlyのボタンが選択された際の処理
    def chk1():
        global checkFlg
        checkFlg = 1
        check2["state"] = "disable"
        check3["state"] = "disable"
        check4["state"] = "disable"
        return checkFlg
    
    #LettersAndNumbersOnlyのボタンが選択された際の処理
    def chk2():
        global checkFlg
        checkFlg = 2
        check1["state"] = "disable"
        check3["state"] = "disable"
        check4["state"] = "disable"
        return checkFlg
    
    #FirstCapitalLetterのボタンが選択された際の処理
    def chk3():
        global checkFlg
        checkFlg = 3
        check1["state"] = "disable"
        check2["state"] = "disable"
        check4["state"] = "disable"
        return checkFlg
    
    #SymbolsAndNumbersOnlyのボタンが選択された際の処理
    def chk4():
        global checkFlg
        checkFlg = 4
        check1["state"] = "disable"
        check2["state"] = "disable"
        check3["state"] = "disable"
        return checkFlg

    #Clearボタンがクリックされた際の処理
    def btn4_click():
        check1["state"] = "normal" 
        check2["state"] = "normal"
        check3["state"] = "normal"
        check4["state"] = "normal"
        global checkFlg
        checkFlg = 0
        return checkFlg

    #Entry入力ボックスの数値を判定
    def inputevent(event):
        try:
            inputText = inpt.get()
            #''は無視
            if inputText == '':
                pass
            #3桁以上はエラーメッセージを表示
            elif len(inputText) >= 3:
                messagebox.showinfo("エラーメッセージ", "正しい文字を入力してください。 (例 1 ～ 30)")
                inpt.delete(0, tk.END)
                #テキストの入力を有効
                text.configure(state='normal')
                #テキストをClear
                text.delete("1.0","end")
            
            #最初に0が入力されたらエラーメッセージを表示
            elif int(inputText) == 0:
                messagebox.showinfo("エラーメッセージ", "正しい文字を入力してください。 (例 1 ～ 30)")
                inpt.delete(0, tk.END)
                #テキストの入力を有効
                text.configure(state='normal')
                #テキストをClear
                text.delete("1.0","end")
            
            #3桁以上はエラーメッセージを表示
            elif int(inputText) >= 31:
                messagebox.showinfo("エラーメッセージ", "30字以内を入力してください。") 
                inpt.delete(0, tk.END)
                text.configure(state='disabled')
                #テキストの入力を有効
                text.configure(state='normal')
                #テキストをClear
                text.delete("1.0","end")
            
        except:
            #数字以外が入力された場合にエラーメッセージを表示
            messagebox.showinfo("エラーメッセージ", "正しい文字を入力してください。 (例 1 ～ 30)") 
            inpt.delete(0, tk.END)
            text.configure(state='disabled')
            #テキストの入力を有効
            text.configure(state='normal')
            #テキストをClear
            text.delete("1.0","end")

    #PasswordReloadクリック時の処理
    def btn_click():

        try:
            #テキストの入力を有効
            text.configure(state='normal')
            #テキストをClear
            text.delete("1.0","end")
            n = inpt.get()
    
            #入力ボックスが空の場合エラーメッセージを表示
            if n == '':
                messagebox.showinfo("エラーメッセージ", "正しい文字を入力してください。 (例 1 ～ 30)") 
                inpt.delete(0, tk.END)
                text.configure(state='disabled')
            
            #入力ボックスが31以上の場合エラーメッセージを表示
            elif int(n) >= 31:
                messagebox.showinfo("エラーメッセージ", "30字以内を入力してください。") 
                inpt.delete(0, tk.END)
                text.configure(state='disabled')
            
            #ランダムに文字を出力
            else:
                #Flgが1だったら文字だけ出力させる
                if checkFlg == 1:
                    text.insert('1.0', ''.join([secrets.choice(st.ascii_letters ) for i in range(int(n))]))
                #Flgが2だったら文字と数字のみ
                elif checkFlg == 2:
                    text.insert('1.0', ''.join([secrets.choice(st.ascii_letters + st.digits ) for i in range(int(n))]))
                    #テキストの入力を無効
                    text.configure(state='disabled')
                #Flgが3だったら先頭文字だけ大文字にする
                elif checkFlg == 3:
                    n = int(n) - 1
                    text.insert('1.0', ''.join([secrets.choice(st.ascii_uppercase ) for i in range(int(1))]))
                    text.insert('1.1', ''.join([secrets.choice(st.ascii_letters + st.digits + '!' + '#'+ '$' + '%' + '&' + ')' + '(' ) for i in range(int(n))]))
                    #テキストの入力を無効
                    text.configure(state='disabled')
                #Flgが4だったら数字と記号だけにする
                elif checkFlg == 4:
                    text.insert('1.0', ''.join([secrets.choice(st.digits + '!' + '#'+ '$' + '%' + '&' + ')' + '(' ) for i in range(int(n))]))
                    #テキストの入力を無効
                    text.configure(state='disabled')
                else:
                    #入力ボックスに入力された回数をランダムに格納された文字列を出力
                    text.insert('1.0', ''.join([secrets.choice(st.ascii_letters + st.digits + '!' + '#'+ '$' + '%' + '&' + ')' + '(' ) for i in range(int(n))]))
                    #テキストの入力を無効
                    text.configure(state='disabled')
        except:
            #不正な文字列が入力された場合エラーメッセージを表示
            messagebox.showinfo("エラーメッセージ", "正しい文字を入力してください。 (例 1 ～ 30)") 
            inpt.delete(0, tk.END)
            text.configure(state='disabled')

    ##PasswordCopyのボタンのエンター押下イベント処理
    def btn_click2():
        #1行目にあるパスワードをコピー
        copy = text.get("1.0","end"+"-1c")
        #クリックボードに貼り付ける
        pyperclip.copy(copy)
        #コピーされたことを表示
        messagebox.showinfo("", "クリップボードにコピーされました。") 
    
    ##PasswordReloadのボタンのエンター押下処理
    def Enter_hand(event):
        btn_click()
    
    #PasswordCopyのボタンのエンター押下処理
    def Enter_hand2(event):
        btn_click2()

        #のボタンのエンター押下処理
    def Enter_hand3(event):
        chk1()

        #のボタンのエンター押下処理
    def Enter_hand4(event):
        chk2()

        #のボタンのエンター押下処理
    def Enter_hand5(event):
        chk3()

        #のボタンのエンター押下処理
    def Enter_hand6(event):
        chk4()

        #のボタンのエンター押下処理
    def Enter_hand7(event):
        btn4_click()
    
    #オプション用のグローバル変数
    global checkFlg
    checkFlg = 0

    #TKクラスのインスタンス化
    window = tk.Tk()

    #ウィンドウの変更を無効
    window.resizable(False, False)

    #フレームのタイトルを決める
    window.title("PasswordGenerator")

    #フレームの幅を選択する
    window.geometry("355x120")

    #menの変数にtk.Menuをインスタンス化し代入
    men = tk.Menu(window)
    window.config(menu=men)

    #メニューバーにVersion,Helpの項目を追加
    men.add_command(label='バージョン',command=on_version)
    men.add_command(label='ヘルプ',command=on_help)

    #入力できるテキストの生成
    text = tk.Text()
    
    #ウイジェットの生成
    text.place(width=350,height=19,x=2,y=2)

    #フレーム内に入力テキストを生成
    inpt = tk.Entry(width=4)

    #入力ボックスのボタン配置設定
    inpt.place(x=10, y=30)
    #入力ボックスに20を表示する
    inpt.insert(0,"20")
    
    #入力ボックスに入力された文字を判定
    inpt.bind("<KeyRelease>",inputevent)

    #テキストに20回ランダムに格納された文字列を出力
    text.insert('1.0', ''.join([secrets.choice(st.ascii_letters + st.digits + '!' + '#'+ '$' + '%' + '&' + ')' + '(' ) for i in range(20)]))

    #フレーム内にパスワード更新ボタンを生成
    btn = tk.Button(window, text='更新', command=btn_click)

    #PasswordReloadのボタン配置設定
    btn.place(x=45, y=30)

    #フレーム内にコピーボタンを生成
    btn2 = tk.Button(window, text='コピー', command=btn_click2)

    #PasswordCopyのボタン配置設定
    btn2.place(x=85, y=30)

    #オプションボタンを生成
    check1 = tk.Button(window, text='英字', command=chk1)
    check1.place(x=10,y=72)

    check2 = tk.Button(window, text='英字と数字', command=chk2)
    check2.place(x=50,y=72)

    check3 = tk.Button(window, text='先頭大文字', command=chk3)
    check3.place(x=122,y=72)

    check4 = tk.Button(window, text='記号と数字', command=chk4)
    check4.place(x=196,y=72)

    #Resetボタンを生成
    btn4 = tk.Button(window, text='リセット', command=btn4_click)
    btn4.place(x=268, y=72)
  
    #PasswordReload,PasswordCopyと各オプションボタンのEnter押下時のバインド処理
    btn.bind("<Return>",Enter_hand)
    btn2.bind("<Return>",Enter_hand2)
    check1.bind("<Return>",Enter_hand3)
    check2.bind("<Return>",Enter_hand4)
    check3.bind("<Return>",Enter_hand5)
    check4.bind("<Return>",Enter_hand6)
    btn4.bind("<Return>",Enter_hand7)

    #テキストの入力を無効
    text.configure(state='disabled')
    #ウィンドウを開いたままにして待機
    window.mainloop()

if __name__ == '__main__':
    main()
