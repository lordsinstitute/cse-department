import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# loading the saved models
ddos_model = pickle.load(open('ddos.sav', 'rb'))

def home_page():
    st.title("Home Page")
    st.image("download.jpg",width=500)
    st.write("Welcome to the Distributed of denial services in SDN attacks detection using machine learning")

# DDOS in SDN prediction using ml Page
def prediction_page():
    # getting the input data from the user
    col1, col2, col3 = st.columns(3)
    
    with col1:
        switch  = st.text_input(' switch')
        pktcount = st.text_input('pktcount')
        bytecount = st.text_input('bytecount')
        dur = st.text_input(' dur')
        
    with col2:
        dur_nsec = st.text_input('dur_nsec')
        flows = st.text_input('flows')
        pktrate  = st.text_input(' pktrate')
        Pairflow= st.text_input('Pairflow')
    
    with col3:
        port_no = st.text_input('port_no')
        tx_bytes = st.text_input('tx_bytes')
        rx_bytes= st.text_input('rx_bytes')
        tx_kbps= st.text_input('tx_kbps')
        rx_kbps= st.text_input('rx_kbps')
        
    # code for Prediction
    DDOS_SDN = ''
    
    # creating a button for Prediction
    if st.button('DDOS in SDN Result'):
        DDOSinSDN_prediction = ddos_model.predict([[switch,pktcount,bytecount,dur,dur_nsec,flows,pktrate,Pairflow,port_no,tx_bytes,rx_bytes,tx_kbps,rx_kbps]])
        
        if DDOSinSDN_prediction == 0:
            output_type = "Internet Control Message Protocol (ICMP)"
            suggestion = "To mitigate ICMP-based DDoS attacks, consider implementing rate limiting or filtering rules for ICMP traffic. Additionally, network segmentation and access controls can help minimize the impact of ICMP flood attacks."
        elif DDOSinSDN_prediction == 1:
            output_type = "User Datagram Protocol (UDP)"
            suggestion = "To defend against UDP-based DDoS attacks, prioritize ingress filtering to block spoofed UDP packets. Utilizing traffic analysis tools and rate limiting mechanisms can also help identify and mitigate UDP flood attacks."
        elif DDOSinSDN_prediction == 2:
            output_type = "Transmission Control Protocol (TCP)"
            suggestion = "To protect against TCP-based DDoS attacks, consider implementing SYN flood protection mechanisms such as SYN cookies or SYN flood rate limiting. Additionally, deploying intrusion detection systems (IDS) and firewalls can help detect and block malicious TCP connections."
            
        st.success(f'The output is {output_type}')
        st.info(f'Suggestion: {suggestion}')
def about_page():
    st.title("About")
   
    st.write("Welcome to Our Distributed Denial of Service (DDoS) Detection in Software-Defined Networking (SDN) Project.")
    st.write("# **About the Project**")
    st.write("""Our project is dedicated to the detection of Distributed Denial of Service (DDoS) attacks in Software-Defined Networking (SDN) environments. We focus on ensuring the availability and reliability of network services by identifying and mitigating DDoS attacks.""")
    st.write("# **Key Objectives**")
    st.write("### **Real-time Detection**")
    st.write("""Our primary objective is to develop a system that can detect DDoS attacks in real-time within SDN environments. This proactive approach enhances the security posture of networks by preventing service disruption.""")
    st.write("### **Utilize Machine Learning**")
    st.write("""We utilize advanced Machine Learning algorithms to analyze network traffic patterns and identify anomalous behavior indicative of DDoS attacks. Machine Learning enables us to adapt to evolving attack techniques and maintain robust detection capabilities.""")
    st.write("### **Mitigate DDoS Attacks**")
    st.write("""In addition to detection, we focus on implementing effective mitigation strategies to minimize the impact of DDoS attacks on network services. By swiftly responding to detected threats, we ensure the continuous operation of SDN environments.""")
    st.write("# **Research Methodology**")
    st.write("""Our approach involves collecting and analyzing large volumes of network traffic data from SDN environments. We employ both supervised and unsupervised Machine Learning techniques to train models for DDoS detection. Additionally, we conduct extensive experiments to evaluate the performance of our detection and mitigation strategies.""")
    st.write("# **Collaboration Opportunities**")
    st.write("""We welcome collaboration with industry partners, academic institutions, and cybersecurity experts interested in advancing DDoS resilience in SDN. Collaborators can contribute domain expertise, provide access to real-world datasets, or participate in joint research projects.""")
    st.write("# **Publications and Presentations**")
    st.write("""Our project team regularly publishes research papers and presents findings at conferences and workshops related to network security, SDN, and machine learning. These publications contribute to the broader academic and industry discussions on DDoS mitigation and SDN security.""")
    st.write("# **Get Involved**")
    st.write("""Excited about the potential of securing network infrastructures against DDoS attacks? Join us on our journey as we explore innovative solutions in DDoS detection and mitigation within SDN environments. Engage with our community, share your expertise, and together, let's build more resilient network architectures.""")
    st.write("# **Contact Us**")
    st.write("""Have questions or want to learn more about our project? Contact our team at your-email@example.com and let's start a conversation about how we can collaborate to enhance DDoS resilience in SDN.""")
# Replace "your-email@example.com" with the actual email address for contact.

# Sidebar
st.sidebar.title("Distributed Denial of Service (DDoS) Detection in Software-Defined Networking (SDN)")

# Sidebar buttons

selected_page = st.sidebar.radio("Select Page", ["Home", "Prediction", "About"])

# Store the selected page in session state for automatic navigation
st.session_state.selected_page = selected_page

# Navigation based on the selected page and login status
if st.session_state.selected_page == "Home":
        home_page()
elif st.session_state.selected_page == "Prediction":
        prediction_page()
elif st.session_state.selected_page == "About":
        about_page()
  