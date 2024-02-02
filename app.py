import streamlit as st

import os

from SPARQLWrapper import SPARQLWrapper, JSON
from streamlit_agraph import agraph, TripleStore, Node, Edge, Config
from layout import footer
import json

import google.generativeai as genai

# Tool import
from crewai.tools.gemini_tools import GeminiSearchTools

from crewai.tools.phi2_tools import Phi2SearchTools

# Google Langchain
from langchain_google_genai import GoogleGenerativeAI

# Crew imports
from crewai import Agent, Task, Crew, Process

# Retrieve API Key from Environment Variable
GOOGLE_AI_STUDIO = os.environ.get('GOOGLE_API_KEY')

# Ensure the API key is available
if not GOOGLE_AI_STUDIO:
    st.error("API key not found. Please set the GOOGLE_AI_STUDIO environment variable.")
else:
    # Set gemini_llm
    gemini_llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_AI_STUDIO)

    # Base Example with Gemini Search

    TITLE1 = """<h1 align="center">Phi-2 Geneation</h1>"""




# CrewAI Code Start ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def crewai_process(research_topic):
    # Define your agents with roles and goals
    Sam = Agent(
        role='Data Analyst specializing in network structures and graph theory.',
        goal="""To uncover hidden structures and patterns within complex networks and to detect connection 
        patterns that might indicate fraudulent activities.""",
        backstory=""" Sam has a background in computer science with a focus on data analysis. 
        Having worked in cybersecurity, Sam developed a keen eye for detecting anomalies in network traffic, 
        which translates well into analyzing complex graphs for irregular and overly connected patterns.""",
        verbose=True,
        allow_delegation=True,
        llm = gemini_llm,
        tools=[
                Phi2SearchTools.phi2_search
      ]

    )

    Donna = Agent(
        role='Behavioral Analyst with expertise in pattern recognition in data.',
        goal="""To detect atypical behavior patterns that might indicate fraudulent activities.""",
        backstory="""Donna's background in behavioral science and her experience in financial fraud detection have equipped 
        her with a unique perspective on spotting unusual patterns in data. She excels in interpreting complex behaviors 
        and identifying deviations from the norm. """,
        verbose=True,
        llm = gemini_llm,
        tools=[
                GeminiSearchTools.gemini_search
      ]

    )

    Henry = Agent(
        role='Graph Visualization Specialist.',
        goal="""To create clear, comprehensible visual representations of complex data, particularly focusing on fraudulent networks. """,
        backstory="""YHenry has a background in graphic design and computer science. He found his niche in data visualization, 
        where he combines his artistic skills with technical knowledge to make complex data easily understandable. 
        Over the years, Henry has specialized in visualizing criminal networks, using his skills to aid law enforcement 
        and fraud detection teams. """,
        verbose=True,
        allow_delegation=True,
        llm = gemini_llm,
        tools=[
                GeminiSearchTools.gemini_search
      ]

    )



    # Create tasks for your agents
    task1 = Task(
        description=f""" Sam will focus on the structural analysis of the network {research_topic}. 
        This includes: Identifying nodes or groups of nodes with unusually high numbers of connections. 
        Look for connections of multiple parties among same accidents that could indicate a fraud ring. 
        use ROLE and NAME to do your analysis. Analyzing the network for the formation of densely connected 
        subgraphs or communities. OUTPUT RESULT, GIVE DETAILS OF THE NODES AND CONNECTION THAT MAY BE FRAUD
        Use Phi2_search to analyze the graph.
        """,
        agent=Sam
    )

    task2 = Task(
        description="""Donna cleans up Sam's work ensuring that the cases presented are valid""",
        agent=Donna
    )  

    task3 = Task(
        description="""
        Henry's task is to take the fraudulent nodes identified by Sam and Donna and construct a detailed visual graph. 
        This graph should highlight the relationships and interactions within the fraud ring. His output should be a JSON 
        structure with the following characteristics:
        DON'T EXPLAIN WHAT TO DO, OUTPUT THE RESULTS IN THE FOLLOWING GRAPH FORMAT EXAMPLE:

        {
    "name": "Claims Center",
    "img": "https://www.svgrepo.com/show/448123/scope-expense-claims-read.svg",
    "children": [
        {
          "name": "Accident 1",
          "children": [
            {
              "role": "Driver 1",
              "name": "Person 1",
              "link": "http://accidentnetwork.chart/person_1",
              "img": "https://www.svgrepo.com/show/214436/driving-license.svg",
              "size": 50000
            },
            {
              "role": "Witness 2",
              "name": "Person 2",
              "link": "http://accidentnetwork.chart/person_2",
              "img": "https://www.svgrepo.com/show/85131/witness.svg",
              "size": 45000
            },
            {
              "role": "Lawyer 4",
              "name": "Person 4",
              "link": "http://accidentnetwork.chart/person_4",
              "img": "https://www.svgrepo.com/show/492976/lawyer-explaining.svg",
              "size": 40000
            }
          ]
        },
        {
          "name": "Accident 2",
          "children": [
            {
              "role": "Passenger 3",
              "name": "Person 3",
              "link": "http://accidentnetwork.chart/person_3",
              "img": "https://www.svgrepo.com/show/340795/passenger-plus.svg",
              "size": 50000
            },
            {
              "role": "Driver 5",
              "name": "Person 5",
              "link": "http://accidentnetwork.chart/person_5",
              "img": "https://www.svgrepo.com/show/214436/driving-license.svg",
              "size": 45000
            },
            {
              "role": "Adjuster 6",
              "name": "Person 6",
              "link": "http://accidentnetwork.chart/person_6",
              "img": "https://www.svgrepo.com/show/223812/insurance-user.svg",
              "size": 40000
            },
        
            {
              "role": "Lawyer 4",
              "name": "Person 4",
              "link": "http://accidentnetwork.chart/person_4",
              "img": "https://www.svgrepo.com/show/492976/lawyer-explaining.svg",
              "size": 40000
            }
            
          ]
        }

    ]
}

      
        """,
        agent=Henry
    )  

    

    # Instantiate your crew with a sequential process
    crew = Crew(
        agents=[Sam],
        tasks=[task1],
        process=Process.sequential
    )

    # Get your crew to , work!
    result = crew.kickoff()
    
    return result




# CrewAI Code End ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



    

# Data Start ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# Data End   ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if 'fraud_topic' not in st.session_state:
    st.session_state['fraud_topic'] = ''

# Strealit Agraph Start +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def get_inspired():
  sparql = SPARQLWrapper("http://dbpedia.org/sparql")

  query_string = """
  SELECT ?name_pe1_en ?rel_en ?name_pe2_en
  WHERE {
    {
         SELECT ?name_p1 ?rel ?name_p2
         WHERE {
             ?p1 a foaf:Person .
             ?p1 dbo:influencedBy ?p2 .
             ?p2 a foaf:Person .
             ?p1 foaf:name ?name_p1 .
             ?p2 foaf:name ?name_p2 .
            dbo:influencedBy rdfs:label ?rel .
            }
         LIMIT 100
    }
    UNION
    {
         SELECT ?name_p1 ?rel ?name_p2
         WHERE {
            ?p1 a foaf:Person .
            ?p1 dbo:influenced ?p2 .
            ?p2 a foaf:Person .
            ?p1 foaf:name ?name_p1 .
            ?p2 foaf:name ?name_p2 .
            dbo:influenced rdfs:label ?rel .
        }
     LIMIT 100
    }
    FILTER ( LANG(?name_p1) = "en" && LANG(?rel) = "en" && LANG(?name_p2) = "en" )
    BIND ( STR(?name_p1) AS ?name_pe1_en )
    BIND ( STR(?rel) AS ?rel_en )
    BIND ( STR(?name_p2) AS ?name_pe2_en )
  }
  """

  sparql.setQuery(query_string)
  sparql.setReturnFormat(JSON)
  results = sparql.query().convert()
  store = TripleStore()
  for result in results["results"]["bindings"]:
    node1 = result["name_pe1_en"]["value"]
    link = result["rel_en"]["value"]
    node2 = result["name_pe2_en"]["value"]
    store.add_triple(node1, link, node2)
  return store

def app():
  query_type = st.sidebar.selectbox("Fraud Investigation Tpye: ", ["Insurance", "Neo4j" ]) # could add more stuff here later on or add other endpoints in the sidebar.
  config = Config(height=600, width=700, nodeHighlightBehavior=True, highlightColor="#F7A7A6", directed=True,
                  collapsible=True)

  if query_type=="Insurance":
      
    st.title("Insurance Fraud Graph")
    #based on Insurance Fraud
    with open("data/fraud.json", encoding="utf8") as f:
      fraud_file = json.loads(f.read())
      st.session_state['fraud_topic'] = fraud_file
      fraud_store = TripleStore()
      for sub_graph in fraud_file["children"]:
        fraud_store.add_triple(fraud_file["name"], "has_subgroup", sub_graph["name"], picture=fraud_file["img"])
        for node in sub_graph["children"]:
          node1 = node["role"]
          link = "blongs_to"
          node2 = sub_graph["name"]
          pic = node["img"]
          fraud_store.add_triple(node1, link, node2, picture=pic)
      agraph(list(fraud_store.getNodes()), (fraud_store.getEdges()), config)


  if query_type=="Neo4j":
    st.title("Neo4j Fraud Ring")

    with open("data/neo4jdata.json", encoding="utf8") as f:
      fraud_file = json.loads(f.read())
      st.session_state['fraud_topic'] = fraud_file
      fraud_store = TripleStore()
      for sub_graph in fraud_file["children"]:
        fraud_store.add_triple(fraud_file["name"], "has_subgroup", sub_graph["name"], picture=fraud_file["img"])
        for node in sub_graph["children"]:
          node1 = node["role"]
          link = "blongs_to"
          node2 = sub_graph["name"]
          pic = node["img"]
          fraud_store.add_triple(node1, link, node2, picture=pic)
      agraph(list(fraud_store.getNodes()), (fraud_store.getEdges()), config)



  if query_type=="eCommerce":
    st.title("eCommerce Fraud Graph")
    #based on http://marvel-force-chart.surge.sh/
    with open("data/fraud.json", encoding="utf8") as f:
      fraud_file = json.loads(f.read())
      st.session_state['fraud_topic'] = fraud_file
      fraud_store = TripleStore()
      for sub_graph in fraud_file["children"]:
        fraud_store.add_triple(fraud_file["name"], "has_subgroup", sub_graph["name"], picture=fraud_file["img"])
        for node in sub_graph["children"]:
          node1 = node["role"]
          link = "blongs_to"
          node2 = sub_graph["name"]
          pic = node["img"]
          fraud_store.add_triple(node1, link, node2, picture=pic)
      agraph(list(fraud_store.getNodes()), (fraud_store.getEdges()), config)


# Strealit Agraph END +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# Streamlit Crew Input Start ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# input_topic = st.text_area("What Exciting Adventures Await Us", height=100, placeholder="Start Our Story...")

# st.session_state['on_topic'] = input_topic
# Button to run the process


st.title("Fraud Graph")

if st.button("Search for Fraud"):
    # Run the crewai process
    with st.spinner('Generating Content...'):
        # result = crewai_process(input_topic)
        result = crewai_process(st.session_state['fraud_topic'])
        # Display the result
        st.text_area("Output", value=result , height=300)



# Streamlit Crew Input End ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == '__main__':
    app()



