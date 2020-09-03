import tkinter as tk
import string as st
import pyperclip
import secrets
from tkinter import messagebox

def main():
     #Tkクラスをインスタンス化
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
        messagebox.showinfo("Version","Ver:1.0.0") 

    #メニューバーのHelpをクリックした際の処理
    def on_help():
        #使い方を表示する
        messagebox.showinfo("Help","・How to use the password generator tool \n 1.Enter a number from 0 to 30 in the input field. \n ・パスワード生成ツールの使い方 \n 1.入力欄に0〜30の数字を入力してください。") 
    
    #メニューバーにVersion,Help項目を追加
    men.add_command(label='Version',command=on_version)
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
                window2 = tk.Tk()
                window2.withdraw()
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
        copy = text.get("1.0","end")
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
