import streamlit as st
import requests
import json

API_URL = "http://localhost:8000/api/v1/parse"

st.set_page_config(
    page_title="Lucene Query Parser",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Lucene Query Parser")
st.markdown("Parse and understand your Lucene queries with ease")

st.markdown("---")

query_input = st.text_area(
    "Enter your Lucene query:",
    height=100,
    placeholder='Example: ("H.B. Fuller" OR "Arkema") NOT "Albemarle County"',
    help="Enter any valid Lucene query. The parser supports AND, OR, NOT operations, field-specific searches, and more."
)

col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    parse_button = st.button("🔍 Parse Query", type="primary", use_container_width=True)
with col2:
    clear_button = st.button("🗑️ Clear", use_container_width=True)

if clear_button:
    st.rerun()

if parse_button:
    if not query_input or query_input.strip() == "":
        st.error("⚠️ Please enter a query to parse")
    else:
        with st.spinner("Parsing your query..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"query": query_input},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.success("✅ Query parsed successfully!")
                    
                    st.markdown("---")
                    
                    col_left, col_right = st.columns(2)
                    
                    with col_left:
                        st.subheader("📝 Narrative Explanation")
                        st.info(data.get("narrative_text", "N/A"))
                        
                        st.subheader("🔧 Technical Interpretation")
                        st.code(data.get("deterministic_text", "N/A"), language=None)
                    
                    with col_right:
                        st.subheader("🌳 Abstract Syntax Tree (AST)")
                        st.json(data.get("ast_json", {}))
                    
                elif response.status_code == 422:
                    error_detail = response.json()
                    st.error(f"⚠️ Validation Error: {error_detail}")
                else:
                    st.error(f"❌ Error {response.status_code}: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the API. Make sure the FastAPI backend is running on http://localhost:8000")
                st.info("💡 Start the backend with: `poetry run fastapi dev app/main.py`")
            except requests.exceptions.Timeout:
                st.error("❌ Request timed out. The API took too long to respond.")
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {str(e)}")

st.markdown("---")

with st.expander("ℹ️ About This Tool"):
    st.markdown("""
    
    This tool helps you understand and validate Lucene queries by:
    - **Parsing** your query into an Abstract Syntax Tree (AST)
    - **Converting** the AST to human-readable text
    - **Normalizing** the output into narrative form
    
    - Simple word queries: `test`
    - Phrase queries: `"H.B. Fuller"`
    - Boolean operations: `("Apple" OR "Google") AND "Technology"`
    - Exclusions: `"Python" NOT "Snake"`
    - Field-specific searches: `headline:("Breaking News")`
    
    1. `"H.B. Fuller" OR "Arkema"`
    2. `("Company A" OR "Company B") NOT "Location"`
    3. `headline:("Gallery" OR "Research and markets")`
    4. `category:technology AND status:published`
    
    **Note:** The FastAPI backend must be running for this tool to work.
    """)

with st.expander("🚀 Getting Started"):
    st.markdown("""
    
    1. **Start the FastAPI Backend:**
    ```bash
    cd lucene-api
    poetry run fastapi dev app/main.py
    ```
    
    2. **Start the Streamlit App (in a new terminal):**
    ```bash
    poetry run streamlit run streamlit_app.py
    ```
    
    3. **Enter your query** in the text box above and click "Parse Query"!
    """)

st.sidebar.title("📊 Quick Stats")
st.sidebar.info("API Endpoint: `http://localhost:8000/api/v1/parse`")
st.sidebar.success("Ready to parse queries!")

if st.sidebar.button("🔄 Check API Health"):
    try:
        health_response = requests.get("http://localhost:8000/healthz", timeout=5)
        if health_response.status_code == 200:
            st.sidebar.success("✅ API is healthy!")
        else:
            st.sidebar.error("❌ API returned an error")
    except:
        st.sidebar.error("❌ API is not responding")
