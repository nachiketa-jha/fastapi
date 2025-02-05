import streamlit as st
import requests

st.title('FastAPI server')

BASE_URL = "http://127.0.0.1:8000/"

def fetch_data(endpoint):
    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Error fetching data: {e}")

def post_data(endpoint, data):
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", params=data)
        if response.status_code in [200, 201]:
            st.success("Action completed successfully!")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Error posting data: {e}")

def update_data(endpoint, data):
    try:
        response = requests.put(f"{BASE_URL}{endpoint}", params=data)
        if response.status_code in [200, 201]:
            st.success("Action completed successfully!")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Error posting data: {e}")

def delete_data(endpoint):
    try:
        response = requests.delete(f"{BASE_URL}{endpoint}")
        if response.status_code == 204 or response.status_code == 200:
            st.success("Deleted successfully!")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Error deleting data: {e}")

def login(userid, password):
    try:
        response = requests.get(f"{BASE_URL}/user/login/{userid}",params={"password":password})
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Invalid credentials. Please try again.")
            return None
    except Exception as e:
        st.error(f"Login error: {e}")
        return None

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user_info" not in st.session_state:
    st.session_state["user_info"] = {}

if not st.session_state["logged_in"]:
    st.title("Login")
    user_id = st.text_input("user_id")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user_info = login(user_id, password)
        if user_info:
            st.session_state["logged_in"] = True
            st.session_state["user_info"] = user_info
            st.success("Login successful!")
            st.session_state["rerun"] = True
else:
    menu = st.sidebar.radio(
        "Navigation",
        ["Users", "Posts", "Roles", "UserRoles", "Logout"]
    )

    if menu == "Logout":
        st.session_state["logged_in"] = False
        st.session_state["user_info"] = {}
        st.success("Logged out successfully!")
        st.session_state["rerun"] = True

    if menu == "Users":
        st.title("Manage Users")
        action = st.selectbox("Action", ["Add", "Update", "Delete", "View All", "View One"])

        if action == "Add":
            st.subheader("Add User")
            user_id = st.text_input("User_id")
            uname = st.text_input("User Name")
            password = st.text_input("password")
            if st.button("Add User"):
                if user_id and uname and password:
                    post_data(f"/users/{user_id}",data={"uname": uname, "password":password})
                else:
                    st.warning("Please provide all details.")

        elif action == "Update":
            st.subheader("Update User")
            user_id = st.text_input("User ID")
            uname = st.text_input("New uname")
            password = st.text_input("New Password")
            if st.button("Update User"):
                if user_id:
                    update_data(f"/users", {"user_id":user_id,"uname": uname, "password": password})
                else:
                    st.warning("Please provide the User ID and at least one field to update.")

        elif action == "Delete":
            st.subheader("Delete User")
            user_id = st.text_input("User ID")
            if st.button("Delete User"):
                if user_id:
                    delete_data(f"/users/{user_id}")
                else:
                    st.warning("Please provide the User ID.")

        elif action == "View All":
            st.subheader("All Users")
            users = fetch_data("/users")
            if users:
                for user in users:
                    st.write(f"**ID**: {user['user_id']}, **Username**: {user['uname']}")

        elif action == "View One":
            st.subheader("View User")
            user_id = st.text_input("User ID")
            if st.button("Fetch User"):
                if user_id:
                    user = fetch_data(f"/users/{user_id}")
                    if user:
                        st.write(f"**ID**: {user['user_id']}, **Username**: {user['uname']}")
                else:
                    st.warning("Please provide the User ID.")


    if menu == "Posts":
        st.title("Manage Posts")
        action = st.selectbox("Action", ["Add", "Update", "Delete", "View All", "View all posts by one user","Delete by access"])

        if action == "Add":
            st.subheader("Add Post")
            post_id = st.text_input("Post Id")
            user_id = st.text_input("User Id")
            post_text = st.text_input("Post Text")
            if st.button("Add Post"):
                if user_id and post_id and post_text:
                    post_data(f"/posts/{user_id}",data={"post_text": post_text, "post_id":post_id})
                else:
                    st.warning("Please provide all details.")

        elif action == "Update":
            st.subheader("Update Post")
            post_id = st.text_input("Post ID")
            user_id = st.text_input("user_id")
            post_text = st.text_input("post_text")
            if st.button("Update Post"):
                if post_id:
                    update_data(f"/posts", {"post_id":post_id,"user_id": user_id, "post_text": post_text})
                else:
                    st.warning("Please provide the Post ID and at least one field to update.")

        elif action == "Delete":
            st.subheader("Delete Post by post ID")
            post_id = st.text_input("Post ID")
            if st.button("Delete Post"):
                if post_id:
                    delete_data(f"/posts?post_id={post_id}")
                else:
                    st.warning("Please provide the Post ID.")

        elif action == "View All":
            st.subheader("All Posts")
            posts = fetch_data("/posts")
            if posts:
                for post in posts:
                    st.write(f"**Post ID**: {post['post_id']}, **User ID**: {post['user_id']}, **Post Text**: {post['post_text']}")

        elif action == "View all posts by one user":
            st.subheader("View Post")
            user_id = st.text_input("User ID")
            if st.button("Fetch Post"):
                if user_id:
                    posts = fetch_data(f"/posts/{user_id}")
                    for post in posts:
                        st.write(f"**Post ID**: {post['post_id']}, **Post Text**: {post['post_text']}")
                else:
                    st.warning("Please provide the Post ID.")
        elif action == "Delete by access":
            st.subheader("Delete Post by access")
            post_id = st.text_input("Post ID")
            user_id = st.text_input("User ID")
            if st.button("Delete Post"):
                if post_id and user_id:
                    delete_data(f"posts/{user_id}")
    

    if menu == "UserRoles":
        st.title("Manage UserRoles")
        action = st.selectbox("Action", ["Add", "Update", "Delete", "View All"])

        if action == "Add":
            st.subheader("Add User Role")
            user_id = st.text_input("User_id")
            user_role_id = st.text_input("User Role ID")
            role_id = st.text_input("Role ID")
            if st.button("Add User"):
                if user_id and user_role_id and role_id:
                    post_data(f"/userrole/",data={"user_role_id": user_role_id, "user_id":user_id, "role_id":role_id})
                else:
                    st.warning("Please provide all details.")

        elif action == "Update":
            st.subheader("Update User Role")
            user_id = st.text_input("User_id")
            user_role_id = st.text_input("User Role ID")
            role_id = st.text_input("Role ID")
            if st.button("Update User Role"):
                if user_role_id and (user_id or role_id):
                    update_data(f"/userrole/",data={"user_role_id": user_role_id, "user_id":user_id, "role_id":role_id})
                else:
                    st.warning("Please provide all details.")

        elif action == "Delete":
            st.subheader("Delete User Role")
            user_id = st.text_input("User ID")
            if st.button("Delete User"):
                if user_id:
                    delete_data(f"/userrole?user_id={user_id}")
                else:
                    st.warning("Please provide the User ID.")

        elif action == "View All":
            st.subheader("All User Roles")
            userRoles = fetch_data("/userRole")
            if userRoles:
                for userRole in userRoles:
                    st.write(f"**User Role ID**: {userRole['user_role_id']}, **User ID**: {userRole['user_id']}, **Role ID**: {userRole['role_id']}")


    if menu == "Roles":
        st.title("Manage Roles")
        action = st.selectbox("Action", ["Add", "Update", "Delete", "View All","View One"])

        if action == "Add":
            st.subheader("Add Role")
            role_id = st.text_input("Role ID")
            role_name = st.text_input("Role Name")
            menu_is_admin = st.radio("Admin", ["True","False"])
            if menu_is_admin == "True":
                is_admin = True
            elif menu_is_admin == "False":
                is_admin = False
            if st.button("Add Role"):
                if role_id and role_name:
                    post_data(f"/role/",data={"role_id": role_id, "role_name":role_name, "is_admin":is_admin})
                else:
                    st.warning("Please provide all details.")

        elif action == "Update":
            st.subheader("Update Role")
            role_id = st.text_input("role_id")
            role_name = st.text_input("role_name")
            menu_is_admin = st.radio("Admin", ["True","False"])
            if menu_is_admin == "True":
                is_admin = True
            elif menu_is_admin == "False":
                is_admin = False
            if st.button("Update Role"):
                if role_id and role_name:
                    update_data(f"/role/",data={"role_id": role_id, "role_name":role_name, "is_admin":is_admin})
                else:
                    st.warning("Please provide all details.")

        elif action == "Delete":
            st.subheader("Delete Role")
            role_id = st.text_input("Role ID")
            if st.button("Delete Role"):
                if role_id:
                    delete_data(f"/Role?role_id={role_id}")
                else:
                    st.warning("Please provide the Role ID.")

        elif action == "View All":
            st.subheader("All Roles")
            roles = fetch_data("/role")
            if roles:
                for role in roles:
                    st.write(f"**Role ID**: {role['role_id']}, **Role Name**: {role['role_name']}, **Is Admin**: {role['is_admin']}")

        elif action == "View One":
            st.subheader("View Role")
            role_id = st.text_input("Role ID")
            if st.button("Fetch Role"):
                if role_id:
                    role = fetch_data(f"/role/{role_id}")
                    if role:
                        st.write(f"**Role ID**: {role['role_id']}, **Role Name**: {role['role_name']}, **Is Admin**: {role['is_admin']}")
                else:
                    st.warning("Please provide the Role ID.")