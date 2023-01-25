import streamlit as st


def auth():
    user_id = st.sidebar.text_input('Input Username')
    user_pw = st.sidebar.text_input('Input Password', type='password')

    # You can call this auth info from DB or somewhere safe.
    if user_id == 'siu2388' and user_pw == 'siu1234':
        auth_result = True
    else:
        auth_result = False

    return auth_result


def create_layout():
    auth_result = auth()

    if auth_result:
        st.sidebar.success('Welcome SiU :)')
        st.title("SiU's Library")
        st.header('Header')
        st.subheader('Sub Header')
    else:
        st.sidebar.warning('Wrong Authentication !!!')


def main():
    create_layout()


if __name__ == '__main__':
    main()
