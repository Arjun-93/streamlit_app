import streamlit as st
import pandas as pd
import os
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from http.cookies import SimpleCookie

st.set_page_config(layout="wide")

# Constants
USER_DATA_FILE = 'users.csv'
VERIFICATION_CODES = {}

# Initialize session state
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = 'landing'

# Load user data from CSV file
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        try:
            return pd.read_csv(USER_DATA_FILE)
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=['Name', 'Phone', 'Email', 'Password'])
    else:
        return pd.DataFrame(columns=['Name', 'Phone', 'Email', 'Password'])

# Save user data to CSV file
def save_user_data(df):
    df.to_csv(USER_DATA_FILE, index=False)

# Function to validate login
def validate_login(email, password, user_data):
    email = email.strip().lower()
    password = password.strip()

    user_data['Email'] = user_data['Email'].astype(str).str.strip().str.lower()
    user_data['Password'] = user_data['Password'].astype(str).str.strip()
    
    user = user_data[(user_data['Email'] == email) & (user_data['Password'] == password)]
    return not user.empty

# Function to check if email exists
def email_exists(email, user_data):
    email = email.strip().lower()
    user_data['Email'] = user_data['Email'].astype(str).str.strip().str.lower()
    return not user_data[user_data['Email'] == email].empty

# Function to add a new user
def add_user(name, phone, email, password, user_data):
    new_user = pd.DataFrame([[name, phone, email, password]], columns=user_data.columns)
    user_data = pd.concat([user_data, new_user], ignore_index=True)
    save_user_data(user_data)

# Function to send verification code
def send_verification_code(email):
    code = random.randint(100000, 999999)
    VERIFICATION_CODES[email] = code

    # Email setup (replace with your email configuration)
    sender_email = "arjunmehra0000@gmail.com"
    sender_password = "Arjun$2000"
    subject = "Your verification code"
    body = f"Your verification code is: {code}"

    # Creating the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, email, text)
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to render landing page
# def filter_products_by_category(category, data):
#     # Dummy implementation, replace with actual filtering logic
#     return [item for item in data['products']['data']['items'] if item['category'] == category]4

# Create the word cloud
def render_word_cloud(feedback_df):
    text = " ".join(feedback_df['Feedback'])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def render_emoji_chart(feedback_df):
    emojis = {1: '😠', 2: '😞', 3: '😐', 4: '😊', 5: '😍'}
    rating_counts = feedback_df['Rating'].value_counts(normalize=True) * 100
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(rating_counts.index.map(emojis), rating_counts.values, color=['red', 'orange', 'yellow', 'lightgreen', 'green'])
    ax.set_xlabel('Percentage of Users')
    ax.set_ylabel('Rating')
    ax.set_title('Percentage of Users by Rating')
    for bar, (emoji, percentage) in zip(bars, zip(rating_counts.index.map(emojis), rating_counts.values)):
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height() / 2, f'{percentage:.1f}%', va='center', fontsize=12, weight='bold')
        ax.text(width / 2, bar.get_y() + bar.get_height() / 2, emoji, ha='center', va='center', fontsize=40)
    plt.xlim(0, max(rating_counts.values) + 10)
    plt.gca().invert_yaxis()
    plt.show()

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import calendar
from datetime import datetime
feedback_df = pd.read_csv("generated_feedback_dataset_large.csv")

# Filter products by category
def filter_products_by_category(category):
    return [item for item in data['products']['data']['items'] if item['category'] == category]

# Product component
def product_component():
    # Render selectbox
    category = st.selectbox('Select Category', sorted(set(item['category'] for item in data['products']['data']['items'])))
    
    # Filter products by selected category
    filtered_products = filter_products_by_category(category)
    
    # Render products container
    product_container = st.container()
    with product_container:
        for product in filtered_products:
            st.write(f"**ID:** {product['id']}")
            st.write(f"**Name:** {product['name']}")
            st.write(f"**Description:** {product['description']}")
            st.write(f"**Price:** ${product['price']}")
            st.write("---")

# Render bar chart page
def render_bar_chart_page():
    # Placeholder data for bar chart
    categories = [item['category'] for item in data['products']['data']['items']]
    counts = pd.Series(categories).value_counts()

    st.bar_chart(counts)

# Render cloud image page
def render_cloud_image_page():
    # Placeholder data for word cloud
    text = " ".join(item['name'] for item in data['products']['data']['items'])
    wordcloud = WordCloud(width=800, height=400).generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

# Render gauge charts page
def render_gauge_charts_page():
    # Placeholder emoji chart for feedback
    st.write("### Feedback Emoji Chart")
    st.date_input("Select Date Range", [])
    feedback_agg = feedback_df.groupby('Rating').size().reset_index(name='counts')

    emojis = {1: '😠', 2: '😞', 3: '😐', 4: '😊', 5: '😍'}
    for _, row in feedback_agg.iterrows():
        st.write(f"{emojis.get(row['Rating'], '')} {row['counts']} reviews")

def product_component():
    # Render selectbox
    category = st.selectbox('Select Category', sorted(set(item['category'] for item in data['products']['data']['items'])))
    
    # Filter products by selected category
    filtered_products = filter_products_by_category(category)
    
    # Render products container
    # st.write("### Products")
    product_container = st.container(height=500)
    with product_container:
        for product in filtered_products:
            st.write(f"**ID:** {product['id']}")
            st.write(f"**Name:** {product['name']}")
            st.write(f"**Description:** {product['description']}")
            st.write(f"**Price:** ${product['price']}")
            st.write("---")
    

def render_landing_page():
    with st.container():
        # Header
        st.markdown("""
        <style>
            .dashboard-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background-color: black;
                color: white;
                padding: 10px;
            }
            .dashboard-header img {
                width: 50px;
            }
            .dashboard-sidebar {
                padding: 20px;
                background-color: #605958;
                height: 100vh;
            }
            .dashboard-content {
                padding: 20px;
                background-color: #3c3e56;
                height: 100vh;
                flex-grow: 1;
            }
            .nav-buttons {
                display: flex;
                gap: 10px;
            }
            .nav-buttons button {
                background-color: #444;
                color: white;
                border: none;
                padding: 10px;
                cursor: pointer;
            }
            .nav-buttons button:hover {
                background-color: #666;
            }
            .row {
                display: flex;
            }
            .column {
                flex: 50%;
                padding: 10px;
            }
        </style>
        <div class="dashboard-header">
            <div><img src="https://www.streamlit.io/images/brand/streamlit-mark-color.png"></div>
            <div style="font-size: 24px; font-weight: bold;">SecondMain</div>
            <div class="nav-buttons">
                <button>Notification</button>
                <button>About</button>
                <button>Settings</button>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Sidebar and main content
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Sidebar
            st.markdown("### Feed By")
            if st.button("Categories"):
                st.session_state.selected_page = 'bar_chart'
            if st.button("Brands"):
                st.session_state.selected_page = 'cloud_image'
            if st.button("Products"):
                st.session_state.selected_page = 'gauge_charts'
            
            st.markdown("### Reports")
            st.markdown("- Categories\n- Brands\n- Products")
            st.markdown("### Competitors")
            st.markdown("- Products\n- Prices")
            st.markdown("### Insights")
            st.markdown("- Keywords\n- Sentiments")
        
        with col2:
            # Main content
            product_component()

# Function to render bar chart page
def render_bar_chart_page():
    st.markdown("""
        <div class="dashboard-content">
            <h2>Bar Chart Page</h2>
            <div id="chart">
                st.bar_chart({"A":1, "B":2, "C":3})
            </div>
            <div class="row">
                <div class="column">
                    <img src="https://www.streamlit.io/images/brand/streamlit-mark-color.png" alt="Snow" style="width:100%">
                </div>
                <div class="column">
                    <img src="https://www.streamlit.io/images/brand/streamlit-mark-color.png" alt="Forest" style="width:100%">
                </div>
                <div class="column">
                    <img src="https://www.streamlit.io/images/brand/streamlit-mark-color.png" alt="Mountains" style="width:100%">   
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Function to render cloud image page
def render_cloud_image_page():
    st.markdown("""
        <div class="dashboard-content">
            <h2>Cloud Image Page</h2>
            <!-- Cloud image rendering goes here based on dynamic data -->
            <!-- You can use libraries like wordcloud to generate dynamic cloud images -->
        </div>
    """, unsafe_allow_html=True)

# Function to render gauge charts page
def render_gauge_charts_page():
    st.markdown("""
        <div class="dashboard-content">
            <h2>Gauge Charts Page</h2>
            <!-- Gauge charts rendering goes here based on dynamic data -->
        </div>
    """, unsafe_allow_html=True)


# Load JSON data from file
import json
with open('products.json', 'r') as file:
    data = json.load(file)

# Function to filter products by category
def filter_products_by_category(category):
    filtered_products = [item for item in data['products']['data']['items'] if item['category'] == category]
    return filtered_products

# Main function
def main():
    st.title('Streamlit Authentication App')

    # Load user data
    user_data = load_user_data()

    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    # Function to set cookies
    def set_cookie(key, value):
        st.session_state[key] = value
        cookie = SimpleCookie()
        cookie[key] = value
        st.markdown(f"<script>document.cookie = '{cookie.output(header='')}'</script>", unsafe_allow_html=True)

    # Function to get cookies
    def get_cookie(key):
        cookie = SimpleCookie(os.environ.get('HTTP_COOKIE', ''))
        return cookie[key].value if key in cookie else None

    # Check cookies to maintain session
    if not st.session_state.authenticated and get_cookie('authenticated') == 'True':
        st.session_state.authenticated = True
        st.session_state.page = 'dashboard'

    # Back button
    if st.session_state.page != 'login':
        if st.button('Back'):
            st.session_state.page = 'login'

    # Login/Signup/Forgot Password logic
    if st.session_state.page == 'login':
        st.subheader('Login')

        email = st.text_input('Email')
        password = st.text_input('Password', type='password')

        if st.button('Login'):
            if validate_login(email, password, user_data):
                st.success('Logged in successfully!')
                st.session_state.authenticated = True
                set_cookie('authenticated', 'True')
                st.session_state.page = 'dashboard'
            else:
                st.error('Invalid email or password')

        if st.button('Forgot Password'):
            st.session_state.page = 'forgot_password'

        st.markdown('Don\'t have an account? [Signup Here](#)', unsafe_allow_html=True)
        st.button('signup', on_click=lambda: st.session_state.update(page='signup'))
    elif st.session_state.page == 'signup':
        st.subheader('Signup')

        name = st.text_input('Name')
        phone = st.text_input('Phone Number')
        email = st.text_input('Email')
        password = st.text_input('Password', type='password')
        confirm_password = st.text_input('Confirm Password', type='password')

        if st.button('Signup'):
            if password != confirm_password:
                st.error('Passwords do not match')
            elif email_exists(email, user_data):
                st.error('Email already exists')
            else:
                add_user(name, phone, email, password, user_data)
                st.success('Account created successfully!')
                st.session_state.page = 'login'

        st.markdown('Already have an account? [Login Here](#)', unsafe_allow_html=True)
        st.button('login', on_click=lambda: st.session_state.update(page='login'))
    elif st.session_state.page == 'forgot_password':
        st.subheader('Forgot Password')

        email = st.text_input('Enter your email')

        if st.button('Send Verification Code'):
            if email_exists(email, user_data):
                send_verification_code(email)
                st.session_state.page = 'verify_code'
                st.session_state.forgot_password_email = email
                st.success('Verification code sent to your email!')
            else:
                st.error('Email does not exist')

    elif st.session_state.page == 'verify_code':
        st.subheader('Verify Code')

        code = st.text_input('Enter the 6-digit code sent to your email')

        if st.button('Verify'):
            email = st.session_state.forgot_password_email
            if VERIFICATION_CODES.get(email) == int(code):
                st.success('Code verified! Enter your new password.')
                st.session_state.page = 'reset_password'
            else:
                st.error('Invalid verification code')

    elif st.session_state.page == 'reset_password':
        st.subheader('Reset Password')

        new_password = st.text_input('New Password', type='password')
        confirm_new_password = st.text_input('Confirm New Password', type='password')

        if st.button('Reset Password'):
            if new_password != confirm_new_password:
                st.error('Passwords do not match')
            else:
                email = st.session_state.forgot_password_email
                user_data.loc[user_data['Email'] == email, 'Password'] = new_password
                save_user_data(user_data)
                st.success('Password reset successfully! Please log in.')
                st.session_state.page = 'login'

    elif st.session_state.page == 'dashboard' and st.session_state.authenticated: 
        if st.session_state.selected_page == 'landing':
            render_landing_page()
        elif st.session_state.selected_page == 'bar_chart':
            render_bar_chart_page()
        elif st.session_state.selected_page == 'cloud_image':
            render_cloud_image_page()
        elif st.session_state.selected_page == 'gauge_charts':
            render_gauge_charts_page()
    else:
        # Handle authentication or redirect to login page
        st.session_state.authenticated = False
        set_cookie('authenticated', 'False')
        

if __name__ == "__main__":
    main()
