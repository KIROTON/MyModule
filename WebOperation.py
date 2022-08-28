import configparser
import os
import glob

import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome import service as fs

from tkinter import messagebox

class SeleniumOperation:
    def __init__(self, DownloadPath):
        self.DownloadPath = DownloadPath
        #コンフィグ読み取り
        config = configparser.ConfigParser()
        config.read('./config.ini')

        #ChromeDriveのPathを読み込み₍Configにて記載)
        chrome_service = fs.Service(executable_path=config['Chrome']['DriverPath'])
        #オプション記述
        options = webdriver.ChromeOptions()
        # ヘッドレスモード
        if config['Chrome']['Headless'] == 'True':
            options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # print(os.getcwd())
        options.add_experimental_option("prefs",{"download.default_directory": self.DownloadPath})
        
        self.driver = webdriver.Chrome(service=chrome_service,options=options)

    #指定されたURLへ移動₍ページ移動待機付き)
    def GetUrlLoadAll(self,URL):
        self.driver.get(URL)
        #  ページ上のすべての要素が読み込まれるまで待機（15秒でタイムアウト判定）
        WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located)
    
    #クリックするボタンがNameなしでValueのみの場合
    def ClickValueButton(self,Value):
        self.driver.find_element(By.XPATH,"//input[@value='"+Value+"']").click()
        WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located)

    def CheckDownloadComplete(self):
        # 待機タイムアウト時間(秒)設定
        timeout_second = 10
        # 指定時間分待機
        for i in range(timeout_second + 1):
            # ファイル一覧取得
            CheckFileName = os.getcwd()+'\download1\*.*'
            download_fileName = glob.glob(CheckFileName)

            # ファイルが存在する場合
            if download_fileName:
                # 拡張子の抽出
                extension = os.path.splitext(download_fileName[0])

                # 拡張子が '.crdownload' ではない ダウンロード完了 待機を抜ける
                if ".crdownload" not in extension[1]:
                    time.sleep(2)
                    break

            # 指定時間待っても .crdownload 以外のファイルが確認できない場合 エラー
            if i >= timeout_second:
                # == エラー処理をここに記載 ==
                # 終了処理
                self.driver.close
                messagebox.showinfo("DL異常", "DLに異常がありました。\nプログラムを終了します。")
                exit()

        # 一秒待つ
        time.sleep(1)

    def __del__(self):
        self.driver.close()

