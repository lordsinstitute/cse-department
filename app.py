from flask import Flask, render_template, request
import os
import markdown

# 🔹 Import your modules
from rag.vector_store import create_vector_store
from rag.ingestion import load_documents
from agents.orchestrator import run_pipeline
from dotenv import load_dotenv

load_dotenv()
# 🔹 Set API Key (IMPORTANT)
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

from views import app_exec_check
app = Flask(__name__)
app_exec_check(app)

# 🔹 Load documents & create vector store (runs once)
docs = load_documents()
vectorstore = create_vector_store(docs)
retriever = vectorstore.as_retriever()


# ---------------- ROUTES ---------------- #

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        query = request.form["query"]

        # 🔥 Run multi-agent pipeline
        result_raw = run_pipeline(retriever, query)

        # 🔹 Extract outputs
        comp = result_raw.get("comp", "")
        sent = result_raw.get("sent", "")
        metrics = result_raw.get("metrics", "")
        pricing = result_raw.get("pricing", "")
        trends = result_raw.get("trends", "")
        final_output = result_raw.get("final", "")

        # ✅ Convert Markdown → HTML
        result = {
            "comp": markdown.markdown(comp, extensions=["tables"]),
            "sent": markdown.markdown(sent, extensions=["tables"]),
            "metrics": markdown.markdown(metrics, extensions=["tables"]),
            "pricing": markdown.markdown(pricing, extensions=["tables"]),
            "trends": markdown.markdown(trends, extensions=["tables"]),
            "final": markdown.markdown(final_output, extensions=["tables"])
        }

        return render_template("result.html", result=result)

    return render_template("index.html")


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(debug=True)