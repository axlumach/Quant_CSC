import streamlit as st
import os

# noinspection PyUnresolvedReferences
# import str_slider
from vis_helpers import sidebar, authors, visualisation, main_page
from vis_helpers import pca, rsd, enhancement_factor

import sentry_sdk

if os.path.isfile(".streamlit/secrets.toml"):
    if 'sentry_url' in st.secrets:
        sentry_sdk.init(
            st.secrets['sentry_url'],
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=0.001,
        )
    else:        
        print('sentry not running')
else:
    print('No secrets found')


def main():
    """
    Main is responsible for the visualisation of everything connected with streamlit.
    It is the web application itself.
    """

    # Check if database secrets have been provided
    database_vars = ["user", "password", "host", "port", "database"]
    if not st.secrets.load_if_toml_exists() or \
        "database" not in st.secrets or \
        not all([key in st.secrets.database for key in database_vars]):
            st.warning("Database variables not provided!")
            st.stop()

    # # Radiobuttons in one row
    # st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    # Sets sidebar's header and logo
    sidebar.sidebar_head()

    analysis_type = st.sidebar.selectbox("Analysis type", ['Main Page', 'Uploading Adm Files', 'Visualisation'])
    # analysis_type = st.sidebar.selectbox("Analysis type", ['Main Page', 'Visualisation', 'PCA', 'EF', 'RSD'])

    if analysis_type == 'Main Page':
        main_page.main_page()
    if analysis_type == 'Uploading Adm Files':
        visualisation.visualisation()
    elif analysis_type == 'Visualization':
        pca.main()
    # elif analysis_type == 'EF':
    #     enhancement_factor.main()
    # elif analysis_type == 'RSD':
    #     rsd.main()
    authors.show_developers()


if __name__ == '__main__':
    # try:
    #     import streamlit_analytics
    #
    #     credential_file = 'tmp_credentials.json'
    #     if not os.path.exists(credential_file):
    #         with open(credential_file, 'w') as infile:
    #             infile.write(st.secrets['firebase_credentials'])
    #         print('credentials written')
    #
    #     collection = datetime.date.today().strftime("%Y-%m")
    #     with streamlit_analytics.track(firestore_key_file=credential_file,
    #                                    firestore_collection_name=collection,
    #                                    # verbose=True
    #                                    ):
    #         main()
    # except KeyError:
    #     main()

    main()

    print("Streamlit finished it's work")
