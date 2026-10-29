import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw, Descriptors, Lipinski, AllChem
import py3Dmol
import streamlit.components.v1 as components
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Cheminformatics Virtual Laboratory",
    page_icon="🧪",
    layout="wide"
)

# Sidebar Navigation
st.sidebar.title("🧪 Virtual Lab")
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Theory", "Molecular Visualization", "Molecular Properties Report", "Assessment"]
)

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
    st.title("🧪 Cheminformatics Virtual Laboratory")
    st.subheader("SRM Institute of Science and Technology, Tiruchirappalli")
    st.caption("Faculty of Engineering and Technology | School of Sciences | Division of Chemistry")
    
    st.markdown("---")
    st.header("Welcome to the Virtual Laboratory")
    st.write("This interactive virtual laboratory helps students understand important concepts in cheminformatics and computational chemistry.")
    
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
    
    # Table for Example Molecules
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
