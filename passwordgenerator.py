import tkinter as tk
import string as st
import pyperclip
import secrets
from tkinter import messagebox

def main():
    #チェックボックス用のグローバル変数
    global checkFlg
    checkFlg = 0
    #TKクラスのインスタンス化
    window = tk.Tk()
    #ウィンドウの変更を無効
    window.resizable(False, False)
    #フレームのタイトルを決める
    window.title("PasswordGenerator")
    #フレームの幅を選択する
    window.geometry("280x60")
    #menの変数にtk.Menuをインスタンス化し代入
    men = tk.Menu(window)
    window.config(menu=men)
    #メニューバーのcloseをクリックした際の処理
    def on_version():
        #versionを表示する
        messagebox.showinfo("Version","Ver:1.0.2") 

    #メニューバーのHelpをクリックした際の処理
    def on_help():
        #使い方を表示する
        messagebox.showinfo("Help","・パスワード生成ツールの使い方 \n 1.入力フィールドに1〜30の数値を入力できます。 \n 2.PasswordReloadで表示されているパスワードを更新できます。 \n 3.PasswordCopyでコピーされます。 \n 4.入力条件の変更ができます。設定を選択する(文字のみ, 文字と数字のみ,先頭大文字,数字と記号のみ)が選択できます。 \n 5.チェックボックスを選択後に反映をクリック \n 6.最初の画面に戻るので入力フィールドに数値を入力。 \n 7.デフォルトの設定に戻す場合は設定のチェックボックスが選択されていない状態で反映を選択してください。") 

    #チェックボックスが選択された際の処理
    def chk1(event):
        global checkFlg
        checkFlg = 1
        return checkFlg

    def chk2(event):
        global checkFlg
        checkFlg = 2
        return checkFlg

    def chk3(event):
        global checkFlg
        checkFlg = 3
        return checkFlg
    
    def chk4(event):
        global checkFlg
        checkFlg = 4
        return checkFlg
    #フラグの初期化処理
    def FlgReSet():    
        global checkFlg
        checkFlg = 0
        return checkFlg

    #メニューバーのConfigをクリックした際の処理
    def on_config():
        window = tk.Tk()
        window.title("PasswordSetConfig")
        window.geometry("280x90")
        window.resizable(False, False)

        #チェックボックスを生成
        check1 = tk.Checkbutton(window,text="LettersOnly")
        check1.place(x=10,y=1)
        check1.bind("<1>",chk1)

        check2 = tk.Checkbutton(window,text="LettersAndNumbersOnly")
        check2.place(x=10,y=20)
        check2.bind("<1>",chk2)

        check3 = tk.Checkbutton(window,text="FirstCapitalLetter")
        check3.place(x=10,y=40)
        check3.bind("<1>",chk3) 

        check4 = tk.Checkbutton(window,text="SymbolsAndNumbersOnly")
        check4.place(x=10,y=60)
        check4.bind("<1>",chk4) 

        #Reflectボタンがクリックされた際の処理
        def btn3_click():
            window.destroy()
        btn3 = tk.Button(window, text='Reflect', command=btn3_click)
        btn3.place(x=200, y=30)
        #Configが開かれた場合フラグを初期化する
        FlgReSet()

    #メニューバーにVersion,Help,Configの項目を追加
    men.add_command(label='Version',command=on_version)
    men.add_command(label='Config',command=on_config)
    men.add_command(label='Help',command=on_help)

    #入力できるテキストの生成
    text = tk.Text()
    #ウイジェットの生成
    text.place(width=275,height=18,x=2,y=2)

    #フレーム内に入力テキストを生成
    inpt = tk.Entry(width=4)

    #入力ボックスのボタン配置設定
    inpt.place(x=6, y=25)
    #入力ボックスに25を表示する
    inpt.insert(0,"20")
    
    #Entry入力ボックスの数値を判定
    def inputevent(event):
        try:
            inputText = inpt.get()
            #''は無視
            if inputText == '':
                pass
            #3桁以上はエラーメッセージを表示
            elif len(inputText) >= 3:
                messagebox.showinfo("Error message", "Please enter the correct characters (Example 1 to 30)")
                inpt.delete(0, tk.END)
                #テキストの入力を有効
                text.configure(state='normal')
                #テキストをClear
                text.delete("1.0","end")
            
            #最初に0が入力されたらエラーメッセージを表示
            elif int(inputText) == 0:
                messagebox.showinfo("Error message", "Please enter the correct characters (Example 1 to 30)")
                inpt.delete(0, tk.END)
                #テキストの入力を有効
                text.configure(state='normal')
                #テキストをClear
                text.delete("1.0","end")
            
            #3桁以上はエラーメッセージを表示
            elif int(inputText) >= 31:
                messagebox.showinfo("Error message", "Please enter a number within 30 characters") 
                inpt.delete(0, tk.END)
                text.configure(state='disabled')
                #テキストの入力を有効
                text.configure(state='normal')
                #テキストをClear
                text.delete("1.0","end")
            
        except:
            #数字以外が入力された場合にエラーメッセージを表示
            messagebox.showinfo("Error message", "Please enter the correct characters (Example 1 to 30)") 
            inpt.delete(0, tk.END)
            text.configure(state='disabled')
            #テキストの入力を有効
            text.configure(state='normal')
            #テキストをClear
            text.delete("1.0","end")
    
    #入力ボックスに入力された文字を判定
    inpt.bind("<KeyRelease>",inputevent)

    #テキストに20回ランダムに格納された文字列を出力
    text.insert('1.0', ''.join([secrets.choice(st.ascii_letters + st.digits + '!' + '#'+ '$' + '%' + '&' + ')' + '(' ) for i in range(20)]))

    #更新ボタンクリック時の処理
    def btn_click():

        try:
            #テキストの入力を有効
            text.configure(state='normal')
            #テキストをClear
            text.delete("1.0","end")
            n = inpt.get()
    
            #入力ボックスが空の場合エラーメッセージを表示
            if n == '':
                messagebox.showinfo("Error message", "Please enter the correct characters (Example 1 to 30)") 
                inpt.delete(0, tk.END)
                text.configure(state='disabled')
            
            #入力ボックスが31以上の場合エラーメッセージを表示
            elif int(n) >= 31:
                messagebox.showinfo("Error message", "Please enter a number within 30 characters") 
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
            messagebox.showinfo("Error message", "Please enter the correct characters (Example 1 to 30)") 
            inpt.delete(0, tk.END)
            text.configure(state='disabled')

    def btn_click2():
        #1行目にあるパスワードをコピー
        #int(inputText)
        copy = text.get("1.0","end"+"-1c")
        #クリックボードに貼り付ける
        pyperclip.copy(copy)
    
    #フレーム内にパスワード更新ボタンを生成
    btn = tk.Button(window, text='PasswordReload', command=btn_click)
    #PasswordReloadのボタン配置設定
    btn.place(x=37, y=25)
    #フレーム内にコピーボタンを生成
    btn2 = tk.Button(window, text='PasswordCopy', command=btn_click2)
    
    #PasswordCopyのボタン配置設定
    btn2.place(x=145, y=25)
    ##PasswordReloadのボタンのエンター押下処理
    def Enter_hand(event):
        btn_click()
    #PasswordCopyのボタンのエンター押下処理
    def Enter_hand2(event):
        btn_click2()
    #PasswordReload,PasswordCopyのボタンのバインド処理
    btn.bind("<Return>",Enter_hand)
    btn2.bind("<Return>",Enter_hand2)

    #テキストの入力を無効
    text.configure(state='disabled')
    #ウィンドウを開いたままにして待機
    window.mainloop()
if __name__ == '__main__':
    main()
