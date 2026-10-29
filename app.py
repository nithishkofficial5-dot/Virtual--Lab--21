import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw, Descriptors, Lipinski, AllChem
import py3Dmol
import streamlit.components.v1 as components
import pandas as pd
import os

# Page Configuration
st.set_page_config(
    page_title="Cheminformatics Virtual Laboratory",
    page_icon="🧪",
    layout="wide"
)

# Sidebar Navigation & Logo
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", use_container_width=True)

st.sidebar.title("🧪 Virtual Lab")
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Theory", "Molecular Visualization", "Molecular Properties Report", "Assessment", "Final Project Report"]
)

st.sidebar.markdown("---")

# Student Information Inputs in Sidebar
st.sidebar.subheader("👨‍🎓 Student Information")
student_name = st.sidebar.text_input("Student Name", placeholder="Enter your name")
reg_number = st.sidebar.text_input("Registration Number", placeholder="Enter reg number")

st.sidebar.markdown("---")

# Learning Objectives Section in Sidebar
st.sidebar.subheader("🎓 Learning Objectives")
st.sidebar.markdown("""
**Students can learn:**
- SMILES notation
- Molecular representation
- 2D visualization
- 3D visualization
- Molecular descriptors
- Structure-property relationships
""")

# Example Molecules Data
EXAMPLES = {
    "Ethanol": "CCO",
    "Benzene": "c1ccccc1",
    "Phenol": "Oc1ccccc1",
    "Acetic Acid": "CC(=O)O",
    "Aspirin": "CC(=O)Oc1ccccc1C(=O)O",
    "Caffeine": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"
}

if page == "Home":
    if os.path.exists("logo.png"):
        st.image("logo.png", width=350)
        
    st.title("🧪 Cheminformatics Virtual Laboratory")
    st.subheader("SRM Institute of Science and Technology, Tiruchirappalli")
    st.caption("Faculty of Engineering and Technology | School of Sciences | Division of Chemistry")
    
    st.markdown("---")
    st.header("Welcome to the Virtual Laboratory")
    st.write("This interactive virtual laboratory helps students understand important concepts in cheminformatics and computational chemistry.")
    
    if student_name or reg_number:
        st.info(f"👤 **Current Student Session:** {student_name if student_name else 'N/A'} | **Reg No:** {reg_number if reg_number else 'N/A'}")

    st.subheader("What can students do?")
    st.markdown("""
    - ✅ Enter any SMILES notation
    - ✅ Validate molecular structures
    - ✅ Generate 2D structures
    - ✅ Generate interactive 3D structures
    - ✅ Select different molecular visualization styles
    - ✅ Calculate complete molecular properties
    - ✅ Download molecular reports
    """)
    
    st.markdown("---")
    st.header("Example Molecules")
    
    examples_df = pd.DataFrame([
        {"Molecule": name, "SMILES": smiles} for name, smiles in EXAMPLES.items()
    ])
    st.table(examples_df)
    
    st.markdown("---")
    st.header("👨‍💻 Developed by")
    st.markdown("""
    **K. NITHISHKUMAR**  
    *CYBER SECURITY STUDENT*  
    *FIRST YEAR STUDENT*  
    *SRM Institute of Science and Technology*
    """)

elif page == "Molecular Visualization":
    st.header("🔬 Molecular Visualization")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_example = st.selectbox("Select Example Molecule", ["Custom"] + list(EXAMPLES.keys()))
        if selected_example != "Custom":
            smiles = EXAMPLES[selected_example]
        else:
            smiles = st.text_input("Enter SMILES notation", "CCO")
            
        style = st.selectbox("3D Style", ["stick", "sphere", "cartoon", "line"])

    mol = Chem.MolFromSmiles(smiles)
    
    if mol:
        st.success("Valid SMILES Code!")
        col_2d, col_3d = st.columns(2)
        
        with col_2d:
            st.subheader("2D Structure")
            img = Draw.MolToImage(mol, size=(300, 300))
            st.image(img, use_container_width=True)
            
        with col_3d:
            st.subheader("3D Interactive Structure")
            mol_3d = Chem.AddHs(mol)
            AllChem.EmbedMolecule(mol_3d)
            AllChem.MMFFOptimizeMolecule(mol_3d)
            mblock = Chem.MolToMolBlock(mol_3d)
            
            viewer = py3Dmol.view(width=400, height=350)
            viewer.addModel(mblock, 'mol')
            viewer.setStyle({style: {}})
            viewer.zoomTo()
            components.html(viewer._make_html(), height=360)
    else:
        st.error("Invalid SMILES notation. Please enter a valid one.")

elif page == "Molecular Properties Report":
    st.header("📊 Molecular Properties Report")
    smiles = st.text_input("Enter SMILES notation for calculation", "CC(=O)Oc1ccccc1C(=O)O")
    mol = Chem.MolFromSmiles(smiles)
    
    if mol:
        props = {
            "Property": ["Molecular Weight", "LogP", "H-Bond Donors", "H-Bond Acceptors", "TPSA", "Rotatable Bonds"],
            "Value": [
                round(Descriptors.MolWt(mol), 2),
                round(Descriptors.MolLogP(mol), 2),
                Lipinski.NumHDonors(mol),
                Lipinski.NumHAcceptors(mol),
                round(Descriptors.TPSA(mol), 2),
                Lipinski.NumRotatableBonds(mol)
            ]
        }
        df = pd.DataFrame(props)
        st.table(df)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Report (CSV)", csv, "molecular_properties.csv", "text/csv")

elif page == "Theory":
    st.header("📖 Theory & Concepts")
    st.markdown("""
    **SMILES (Simplified Molecular Input Line Entry System):** 
    A line notation for specifying the structure of chemical species using short ASCII strings.
    
    **Lipinski's Rule of Five:**
    - Molecular mass less than 500 daltons
    - High lipophilicity (expressed as LogP less than 5)
    - Less than 5 hydrogen bond donors
    - Less than 10 hydrogen bond acceptors
    """)

elif page == "Assessment":
    st.header("📝 Assessment")
    st.write("Test your knowledge on SMILES notation:")
    q1 = st.radio("What is the SMILES notation for Ethanol?", ["CCO", "c1ccccc1", "CC(=O)O"])
    if st.button("Submit Answer"):
        if q1 == "CCO":
            st.success("Correct!")
        else:
            st.error("Try again!")

elif page == "Final Project Report":
    st.header("📄 Final Project Report Generation")
    st.write("Generate a personalized lab report based on your student details and analysis.")
    
    if student_name and reg_number:
        st.success(f"Report ready for **{student_name}** (Reg No: **{reg_number}**)")
        report_text = f"""
=====================================================
CHEMINFORMATICS VIRTUAL LABORATORY REPORT
SRM Institute of Science and Technology, Tiruchirappalli
=====================================================

Student Name       : {student_name}
Registration Number : {reg_number}
Course             : Chemistry / Cheminformatics Lab

Status: Laboratory Module Completed Successfully.
        """
        st.code(report_text, language="text")
        st.download_button(
            label="📥 Download Lab Report",
            data=report_text,
            file_name=f"Lab_Report_{reg_number}.txt",
            mime="text/plain"
        )
    else:
        st.warning("⚠️ Please enter your **Student Name** and **Registration Number** in the sidebar to generate the report.")
