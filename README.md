# Open Data 查詢系統

一個強大的開放資料查詢和展示系統，支援 CSV 和 JSON 格式資料。

## 功能特點

- 📊 支持多種資料格式（CSV、JSON）
- 🎨 美觀的 Web 介面
- 🔍 靈活的欄位選擇
- 📱 響應式設計，支援行動裝置
- ⚡ 快速資料載入和展示

## 檔案說明

- `app.py` — Flask Web 應用主程式
- `kaohsiung_opendata.py` — 命令列工具（可選）
- `requirements.txt` — Python 依賴套件
- `templates/` — HTML 模板目錄
- `static/` — 靜態資源目錄

## 快速開始

### 1. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 2. 執行 Web 應用

```bash
python app.py
```

應用將在 `http://localhost:5000` 啟動

### 3. 使用命令列工具（可選）

```bash
# 使用預設資料源
python kaohsiung_opendata.py

# 指定特定 URL
python kaohsiung_opendata.py "https://data.source.gov.tw/api/data"

# 指定 URL 和欄位
python kaohsiung_opendata.py "https://data.source.gov.tw/api/data" "column1,column2,column3"
```

## 預設資料來源

預設使用新北市政府開放資料：
- **URL**: `https://data.ntpc.gov.tw/api/datasets/781b822e-214a-4b9a-b4db-32c9f4626d98/csv/file`
- **內容**: 新北市文化局事件資訊

## Web 介面使用說明

### 基本步驟

1. **檢查可用欄位** - 點擊「🔍 檢查可用欄位」按鈕查看資料包含的所有欄位
2. **選擇欄位** - 在「可用欄位」區域點擊欄位標籤進行選擇
3. **取得資料** - 點擊「📥 取得資料」按鈕獲取並展示結果

### 進階功能

- **自訂 URL** - 在資料來源設定中輸入任何支援格式的 URL
- **手動輸入欄位** - 在「欄位選擇」欄位中直接輸入欄位名稱（以逗號分隔）
- **快速切換** - 點擊欄位標籤快速新增或移除選擇

## 系統需求

- Python 3.7+
- Flask 3.1+
- requests 2.34+
- tabulate 0.10+

## 環境變數

目前支援以下設定：
- 預設 URL 在 `app.py` 的 `DEFAULT_URL` 變數中定義

## 注意事項

⚠️ 某些資料來源的 SSL 憑證驗證已禁用。若需要啟用，請在 `app.py` 的 `download()` 函數中修改 `verify=False` 為 `verify=True`。

## 故障排除

### SSL 憑證錯誤
如果遇到 SSL 錯誤，這是正常的，系統已自動處理。

### 資料無法載入
- 檢查 URL 是否正確
- 確認資料來源可訪問
- 檢查網路連線

### 欄位名稱不匹配
- 使用「檢查可用欄位」功能查看正確的欄位名稱
- 欄位名稱區分大小寫
