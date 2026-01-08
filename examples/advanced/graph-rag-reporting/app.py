import streamlit as st
from dotenv import load_dotenv
import asyncio
from report import retrieve_graph_data, generate_report_from_data
import streamlit.components.v1 as components
from pyvis.network import Network

load_dotenv()

# Initialize session state variables
if "data" not in st.session_state:
    st.session_state.data = None
if "report_text" not in st.session_state:
    st.session_state.report_text = None
if "query_processed" not in st.session_state:
    st.session_state.query_processed = False

st.title("Graph RAG Reporting")

query = st.text_input("Enter your query:")

with st.container():
    col1, col2, _ = st.columns([0.1, 0.2, 0.55])

    with col1:
        if st.button("Query"):
            if query:
                with st.spinner("Retrieving graph data..."):
                    st.session_state.data = asyncio.run(retrieve_graph_data(query))
                    st.session_state.report_text = None  # Clear previous report
                    st.session_state.query_processed = True
            else:
                st.warning("Please enter a query.")

    with col2:
        if st.button("Generate Report"):
            if query:
                with st.spinner("Retrieving data and generating report..."):
                    data = asyncio.run(retrieve_graph_data(query))
                    st.session_state.data = data
                    if data:
                        st.session_state.report_text = asyncio.run(
                            generate_report_from_data(query, data)
                        )
                    else:
                        st.session_state.report_text = None
                    st.session_state.query_processed = True
            else:
                st.warning("Please enter a query.")

    if st.session_state.query_processed:
        data = st.session_state.data
        report_text = st.session_state.report_text

        if not data:
            st.warning("No data found for your query.")
        else:
            st.write(
                f"Found {len(data.nodes)} nodes and {len(data.relationships)} relationships."
            )

            # Define tabs based on whether a report was generated
            if report_text:
                tab_definitions = ["Report", "Context (JSON)", "Graph Visualization"]
                tab1, tab2, tab3 = st.tabs(tab_definitions)

                with tab1:
                    st.markdown(report_text)

                with tab2:
                    st.json(data.json())

                with tab3:
                    # (Graph visualization logic remains the same)
                    net = Network(notebook=True, directed=True)
                    for node in data.nodes:
                        net.add_node(
                            node.element_id, label=node.label, title=str(node.label)
                        )
                    for rel in data.relationships:
                        net.add_edge(
                            rel.start_node_element_id,
                            rel.end_node_element_id,
                            label=rel.type,
                        )
                    net.show("graph.html")
                    components.html(
                        open("graph.html", "r").read(), width=700, height=500
                    )

            else:
                # Only show context and graph tabs if no report was generated
                tab2, tab3 = st.tabs(["Context (JSON)", "Graph Visualization"])

                with tab2:
                    st.json(data.json())

                with tab3:
                    # (Graph visualization logic remains the same)
                    net = Network(notebook=True, directed=True)
                    for node in data.nodes:
                        net.add_node(
                            node.element_id, label=node.label, title=str(node.label)
                        )
                    for rel in data.relationships:
                        net.add_edge(
                            rel.start_node_element_id,
                            rel.end_node_element_id,
                            label=rel.type,
                        )
                    net.show("graph.html")
                    components.html(
                        open("graph.html", "r").read(), width=700, height=500
                    )
