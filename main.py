import streamlit as st
import pandas as pd
import numpy as np
import pickle
   
import sqlite3
import rdkit

from PIL import Image
from rdkit import Chem
from rdkit.Chem import Descriptors 
from rdkit.Chem import Draw
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem import AllChem
from rdkit import DataStructs

# ye yaha pe conda wali command save ki hai rdkit k liye
# conda install -c conda-forge -n My-rdkit rdkit

# All user data related functions (login,signup,view users)
# 13 - 31
conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS usertable(name TEXT,username TEXT,password TEXT)')

def add_userdata(name,username,password):
    c.execute('INSERT INTO usertable(name,username,password) VALUES (?,?,?)',(name,username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM usertable WHERE username = ? AND password = ?' , (username,password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM usertable')
    data = c.fetchall()
    return data

#Calculating molecular descriptors
# 34 - 77

def AromaticProportion(m):
    aromatic_atoms = [m.GetAtomWithIdx(i).GetIsAromatic() for i in range(m.GetNumAtoms())]
    aa_count = []
    for i in aromatic_atoms:
        if i==True:
            aa_count.append(1)
    AromaticAtom = sum(aa_count)
    HeavyAtom = Descriptors.HeavyAtomCount(m)
    AR = AromaticAtom/HeavyAtom
    return AR

def Generate(smiles,verbose = False):
    moldata = []
    for elem in smiles:
        mol = Chem.MolFromSmiles(elem)
        moldata.append(mol)

    baseData = np.arange(1,1)
    i=0;
    for mol in moldata:

        desc_MolLogP = Descriptors.MolLogP(mol)
        desc_MolWt = Descriptors.MolWt(mol)
        desc_NumRotatableBonds = Descriptors.NumRotatableBonds(mol)
        desc_AromaticProportion = AromaticProportion(mol)

        row = np.array([desc_MolLogP,
                        desc_MolWt,
                        desc_NumRotatableBonds,
                        desc_AromaticProportion])

        if(i==0):
            baseData = row
        else:
            baseData = np.vstack([baseData,row])
        
        i=i+1

    columnNames = ["Mol LogP","Molecular Weight","No. of Rotatable Bonds","Aromatic Proportion"]
    descriptors = pd.DataFrame(data = baseData,columns = columnNames)

    return descriptors



def main():

    st.title("Molecular Solubility Predictor")

    logo = Image.open("logo.jpeg")
    st.image(logo, width = 375)

    st.write("This app predicts the **_Solubility (LogS)_** values of molecules! ")
    st.write("**_ > Please Login/Create new account to use the application._**")

    menu = ["Home","Login","Sign Up"]
    st.sidebar.header("Menu")
    
    choice = st.sidebar.selectbox("", menu)

    if choice == "Home":
        st.title("Home")
        #st.text(" This is our B.Tech project.")
        st.write("**> Welcome to our Web Application for Solubility prediction of chemicals ! We calculate the most accurate expected value of Solubility for every drug and compound.**")
        st.write("**> What is Solubility ?**")
        st.write(">**Solubility** is the ability of a solid, liquid, or gaseous chemical substance (referred to as the solute) to dissolve in solvent (usually a liquid) and form a solution. The solubility of a substance fundamentally depends on the solvent used, as well as temperature and pressure.")
        st.write("**> How does it works ?**")
        st.write("> We have used a Machine learning model at the backend that has been trained over thousands of different chemicals. First we take **SMILES** of the chemical as input and calculate **Mol logP, Aromatic Proportion, No. of rotatable bonds and Molecular weight** of the compound at the backend. Using these values we predict the solubility of given compound.")

        #Tutorial video section
        st.header("**Watch our tutorial here**")
        video_file = open('tutorial.mp4','rb')
        video_bytes = video_file.read()
        st.video(video_bytes)
        
        #Developers section
        st.write("  ")
        st.header("**About us**")
        st.markdown("### **_Developers_**")

        #Prateek profile
        pk = Image.open("pk.JPEG")
        st.image(pk,width = 150) 
        st.subheader("**> Prateek Khare**")
        st.write("Undergrad from **Delhi Technological University** (CSE)")
        st.write("[**Linkedin**](https://in.linkedin.com/in/prateek-khare-9b69b4137?trk=people-guest_people_search-card)")
        st.write("Mail here : prateek2992000@gmail.com")
        st.write(" ")

        #Rohan profile
        ro = Image.open("rohan.JPEG")
        st.image(ro,width = 150)
        st.subheader("**> Rohan Shekhar Paunikar**")
        st.write("Undergrad from **Delhi Technological University** (CSE)")
        st.write("[**Linkedin**](https://www.linkedin.com/in/rohan-paunikar-a16b001b2)")
        st.write("Mail here : rohanpounikar@gmail.com")
        st.write(" ")

        #Praveen profile
        pkt = Image.open("pkt.JPEG")
        st.image(pkt,width = 150)
        st.subheader("**> Praveen Kumar Tiu**")
        st.write("Undergrad from **Delhi Technological University** (CSE)")
        st.write("Mail here : praveentiu@gmail.com")
        st.write(" ")

        #Privacy policy
        st.header("**Privacy Policy**")
        st.write("We respect the privacy of our users and by signing up you agree to our privacy policy. We collect information to provide better services to all our users. Your data is completely secure at our databases and is not shared at any cost to anyone.")

        #Research paper used
        st.header("**References**")
        st.write("""
            Research paper used   [Polysaccharides: Structure and Solubility](https://www.intechopen.com/books/solubility-of-polysaccharides/polysaccharides-structure-and-solubility).
                """)
        st.write("""
            Data obtained from the John S. Delaney. [ESOL:  Estimating Aqueous Solubility Directly from Molecular Structure](https://pubs.acs.org/doi/10.1021/ci034243x). ***J. Chem. Inf. Comput. Sci.*** .
                """)


    elif choice == "Sign Up":
        st.title("Sign Up")
        st.write("**_ > Use the sidebar to create a new account._**")
        st.sidebar.header("Create Account")
        st.sidebar.markdown(" ")

        name = st.sidebar.text_input("Full Name")
        username = st.sidebar.text_input("Email Id")
        password = st.sidebar.text_input("Password",type = 'password')
        if st.sidebar.button("Sign Up"):
            create_usertable()
            add_userdata(name,username,password)

            st.success("Account Created Successfully !")
            st.info("Go to Login Menu to Login")


    elif choice == "Login":
        st.title("Login")
        st.write("**_ > Use the sidebar to Login to your account._**")
        st.sidebar.subheader("Login to your Account")
        st.sidebar.subheader(" ")
        
        st.sidebar.markdown("**User Name**")
        username = st.sidebar.text_input("",value = "Enter Here")
        st.sidebar.markdown("**Password**")
        password = st.sidebar.text_input("" , type = 'password')

        if st.sidebar.checkbox("Login"):
            create_usertable()
            result = login_user(username,password)
            if result:

                # Here I have to write options for logged in users.
                # Main functionality for solubility
                # Developers functionality
                # Data viewing functionality
                
                st.success("Logged In as {} .".format(username))
                
                SMILES_input = "CCC\nNCNC\nNNCC"
                #st.title("SMILES Input")
                st.header("**SMILES Input**")
                st.subheader("Please Enter *SMILES* Notation of Molecules")
                #st.markdown("Please Enter **SMILES** Notation of Molecules")
                SMILES = st.text_area("",SMILES_input)

                SMILES = "C\n" + SMILES #Adds C as a dummy , first item
                SMILES = SMILES.split('\n')

                SMILES[1:]  #Dummy item removed

                st.button("Predict")

                #structure = Chem.MolFromSmiles(SMILES)
                #mol_list = []
                #for smile in SMILES:
                #    struc = Chem.MolFromSmiles(smile)
                #    mol_list.append(struc)

                #img = Draw.MolsToGridImage(mol_list)
                #img
                X = Generate(SMILES)
                st.header("**Calculated Molecular Descriptors**")
                X[1:]

                load_model = pickle.load(open('solubility model.pkl','rb'))
                prediction = load_model.predict(X)
                st.header("**Predicted Solubility**")
                prediction[1:]
                
                #view database
                #user_result = view_all_users()
                #clean_db = pd.DataFrame(user_result, columns = ["Name","User Id","Password"])
                #st.dataframe(clean_db)

                delaney_with_descriptors_url = 'https://raw.githubusercontent.com/dataprofessor/data/master/delaney_solubility_with_descriptors.csv'
                dataset = pd.read_csv(delaney_with_descriptors_url)
                st.write("**> Dataset used**")
                st.dataframe(dataset)

                st.subheader("**Line charts for the dataset**")
                st.line_chart(dataset)
                #st.area_chart(dataset)
                #st.bar_chart(dataset)
                
                newdataset = dataset.drop(['MolWt'],axis = 1)
                st.line_chart(newdataset)

            else:
                st.error("Invalid Username or Password !")

if __name__ == "__main__":
    main()