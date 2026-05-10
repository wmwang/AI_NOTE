# 12 檢索增強生成與 Text-to-SQL

本章與本書其餘部分有所不同，因為我們不是介紹讓程式設計更輕鬆的實用技術和工具，而是開發一個使用 AI 來達成結果的程式。當然，仍然有關聯：本章範例的程式碼同樣是在 AI 的支援下建立的。因此，本章再次包含大量的提示，以及一些關於我們為什麼以特定方式表述提示，以及為什麼之前的一些嘗試失敗了的說明。

以下 AI 應用的問題在於使用大型語言模型（LLM）分析來自不同來源的資料。我們使用 PDF 文件、HTML 格式的網頁和 SQL 資料庫作為基礎資料。此外，還使用了兩種不同的技術來實現這些需求：檢索增強生成（RAG）和 Text-to-SQL。其想法是利用這些技術讓沉睡的資料寶庫變得可搜尋。

在許多專案中，對已歸檔的 PDF 和其他文件進行關鍵字搜尋是不夠的，更不用說 SQL 資料庫中的資料了。用自然語言提出問題並用這些資料的內容來回答，在某些領域確實可以成為改變遊戲規則的關鍵。

檢索增強生成（RAG）是當前 AI 熱潮中的流行語之一。因為無法以可管理的工作量將自己的資訊添加到現成的 LLM 中，所以在一個大型通用語言模型之前放置了一個額外的小型自訂語言模型——嵌入模型。當進行查詢時，該模型的結果被轉送到 LLM，然後 LLM 為使用者生成回應。

嵌入模型將非結構化資料（如文字或圖片）轉換為多維向量。就像描述地球上各個點的地理座標系統一樣，這些向量提供了關於資訊之間相對位置的資訊。然而，這些向量不像地理座標系統那樣僅限於三維，而是可以擁有數百或數千個維度。

使用 Text-to-SQL，LLM 從自然語言的查詢中生成 SQL 查詢。為了使其運作，資料庫結構的資訊連同請求一起被傳送給 LLM。正如你可以想像的，只有當表格和欄位名稱具有有意義的命名時，LLM 才有機會制定出合理的 SQL 查詢。

為了開發以下範例中的 AI 應用，我們使用開源函式庫 LlamaIndex（www.llamaindex.ai）。這個函式庫提供了 Python 程式語言以及 TypeScript 的連接。我們在這個範例中選擇了 Python。

## 12.1 RAG 快速入門

作為該主題的介紹，我們想展示如果讓 AI 自己編寫，你能多快得到一個可執行的 AI 應用。我們想要對儲存在硬碟上 pdfs 資料夾中的文件提出關於 HTML 頁面的問題。這些是關於奧地利昆蟲普查研究計畫的年度報告和進一步資訊，我們將在本章稍後更詳細地討論。我們對 Claude 3.5 Sonnet LLM 的提示如下：

**提示：** Generate a FastAPI backend for a LlamaIndex Q&A application and an HTML page to input questions. Data for LlamaIndex is in a folder pdfs. Don't use templating, but serve the HTML file from server root.

遺憾的是，生成的 Python 程式碼無法執行，因為 LlamaIndex 函式庫自 Claude 訓練資料截止以來已經有所更改。這是我們在本書中已經多次遇到的問題。然而，更改很小（GPTSimpleVectorIndex 已被重新命名為 VectorStoreIndex），更改三行程式碼後，應用程式就可以運行了。在這裡，我們展示整個後端腳本，它啟動網頁伺服器，使用 AI 回答問題，並以 JavaScript 物件表示法（JSON）格式返回答案：

```python
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from llama_index.core import (
  VectorStoreIndex, SimpleDirectoryReader
)
app = FastAPI()
documents = SimpleDirectoryReader("pdfs").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
class Question(BaseModel):
    text: str
@app.post("/api/ask")
async def ask_question(question: Question):
    try:
        response = query_engine.query(question.text)
        return {"answer": str(response)}
    except Exception as e:
        raise HTTPException(status_code=500, 
detail=str(e))
app.mount("/", StaticFiles(directory="static", 
html=True),
          name="static")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  
```

大多數不多的程式碼行都與網頁伺服器有關，使用 FastAPI 和 Uvicorn 函式庫可以輕鬆設定。static 資料夾中的 HTML 文件透過網頁伺服器定期提供。在發送到 /api/ask URL 的 HTTP POST 請求的情況下，請求的內容被映射到先前定義的 Question 類別。其中包含的 text 條目被傳遞給 query_engine 呼叫。

這就是奇蹟發生的地方：只需三行程式碼，LlamaIndex 函式庫就建立了 query_engine，它可以用自然語言查詢搜尋 PDF 文件的內容。為此，SimpleDirectoryReader 讀取一個包含檔案的資料夾，在我們的案例中是 PDF 文件。然後從這些文件生成 VectorStoreIndex，再從中衍生出 query_engine。

我們將在以下各節中解釋這些步驟中詳細發生了什麼。首先，我們想試用我們的應用程式。正如 Claude 在簡短說明中解釋的那樣，我們需要安裝必要的 Python 函式庫：

```bash
pip install fastapi uvicorn llama-index pydantic  
```

HTML 前端只需要幾行 JavaScript 程式碼，不需要額外的函式庫。我們不需要對儲存為 static 資料夾中 index.html 的檔案進行任何更改。HTML 檔案的核心部分如下：

```html
<textarea id="question" placeholder="Enter your 
question here">
</textarea>
<button onclick="askQuestion()">Ask</button>
<div id="answer"></div>
<script> 
  async function askQuestion() {
    const question = 
document.getElementById("question").value;
    const answerDiv = 
document.getElementById("answer");
    answerDiv.innerHTML = "Loading...";
    try {
      const response = await fetch("/api/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: question }),

      });
      if (!response.ok) {
        throw new Error("Network response was not 
ok");
      }
      const data = await response.json();
      answerDiv.innerHTML = data.answer;
    } catch (error) {
      answerDiv.innerHTML = "Error: " + error.message;
    }
  }
</script>  
```

點擊 Ask 按鈕時執行的 askQuestion 函式，使用 HTTP POST 請求將具有 question ID 的文字欄位內容作為 JSON 字串發送到後端。如果請求成功得到回應，data.answer JSON 結構的內容會被插入到對應的 HTML DIV 區域中。

Claude 在說明中沒有提到的是，LlamaIndex 將困難的工作交給了 OpenAI。因此，只有當你擁有 OpenAI API 金鑰且帳戶中有可用額度時，應用程式才能運作。要讓應用程式存取你的帳戶，你必須在 OPENAI_API_KEY 環境變數中設定 API 金鑰。在常見的 Linux shell 中，你需要呼叫以下命令：

```bash
export OPENAI_API_KEY="sk-proj-xxxxxxxx"  
```

現在我們可以使用以下命令啟動我們的應用程式：

```bash
python main.py  
```

結果相當令人信服。10 分鐘後，第一個網頁應用程式就準備好了，可以用自然語言回答關於固態硬碟（SSD）上 PDF 文件的問題。

在你合上本書（或關掉電子閱讀器）開始實作這個範例之前，我們想指出這個應用程式的一些不足之處：

- 每次啟動網頁伺服器時，索引都會重新生成。然而，這不是必須的，因為你也可以將 VectorStoreIndex 儲存在本地。
- 預設設定要求你必須存取 OpenAI 併付費。然而，LlamaIndex 也可以與其他雲端供應商以及本地 LLM 一起使用，而且效果一點也不差。
- 你可以非常精確地設定要索引哪些類型的文件以及索引的詳細運作方式。這裡有很大的最佳化潛力。

> 圖 12.1 我們的 RAG 快速入門

閱讀以下各節時，你將更深入了解 RAG 和 LlamaIndex 函式庫的運作方式。
