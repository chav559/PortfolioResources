import streamlit as st
import pandas as pd
import pydeck as pdk
from PIL import Image
from functionality2 import location_description
from functionality1 import update_availability
from functionality3 import parking_list




# '''
# Homepage/Mission Statement
# '''

# This function loads the homepage of our application, which displays our mission statement, functionality, and boundaries
# of the application's functionality.
def homepage():
    st.title("Park It: Safe and Simple")
    st.write("Search for parking spots within Los Angeles based on **proximity**, **price**, and **safety metrics**.")
    st.subheader("Our Mission Statement:")
    st.write(
        "Our motivation for Park It is two-fold. The first is simple utility, to make the parking process simpler "
        "for drivers. Parking can often be one of the more troublesome aspects for drivers. This includes finding an "
        "available and appropriate spot (near your destination) – as well as understanding if the various policies and "
        "restrictions apply to you at that specific date and time.")
    st.write(
        "Our other goal, which we believe is more significant, is to tackle the issue of safety. The FBI has found "
        "that approximately one third of assaults and murders (in recent years) occurred in parking facilities. "
        "According to the FBI’s Crime Data Explorer (database), in the last 5 years there were 157,092 violent crimes "
        "in parking lots/garages (FBI). Unfortunately, these statistics don’t even account for the risks of walking to "
        "and from street parking – which is another common location for crimes of opportunity.")
    st.write("Our current area of operation for the application is approximately the 90038 and 90028 zip codes, "
             "whose boundaries are displayed below:")
    image = Image.open("Database_Limit.png")
    st.image(image,use_column_width=True)
    st.subheader("Specific Parking Information:")
    st.write("Users can look up information on a parking spot (price, hours, valet, rate hours, safety score) by "
             "entering the location's address. Users can further narrow down results by specifying the type of parking "
             "(garage, lot, street).")
    st.subheader("Availability Updates")
    st.write("Realtime updates on the availability of a user's specified parking spot are shown in the form of a "
             "true/false value. Furthermore, a user can update the status of a location if in real-time if the "
             "spot(s) are vacant or full. ")
    st.subheader("Locate Nearby Parking")
    st.write("Based on the user's current location, the user will be displayed the closest n parking spots to them. "
             "This will be available in the form of an interactive map as well as a sorted list containing general "
             "location data. Users can click on a hypertext link of a specific location they are interested in to "
             "redirect them back to the 'Specific Parking Information' page, displaying the details for that location.")

# This function is tied to availability updates functionality present in the Specific Parking Information page.
# By passing in an index value of the location's position in Firebase, a user is able to then click either on a
# checkbox to clear the query result, or instead to update availability. If the latter occurs, they are able to select
# if a location is occupied or available, and their input is passed as a parameter to the backend function
# update_availability to update the value in Firebase for the availability attribute.
def Availability(loc_id):
    if st.checkbox("Click to clear the query result"):
        st.checkbox("Are you sure you want to start a new search? (Click checkbox to proceed)")
        st.session_state["button"] = False
    st.write("OR")
    if st.checkbox("Click here if you would like to update the availability of the location's parking"):
        isaval = st.selectbox("Input availability", ["", "Available", "Occupied"])
        if isaval == "Available":
            update_availability(loc_id, True)
            st.write("The availability of this parking location has been updated")
            st.session_state["button"] = False
            st.checkbox("Click to clear query result", key="clear query 1")
        elif isaval == "Occupied":
            update_availability(loc_id, False)
            st.write("The availability of this parking location has been updated")
            st.session_state["button"] = False
            st.checkbox("Click to clear the query result", key="clear query 2")
        else:
            st.write("Please select an option from above")

# This function loads the Specific Parking Information page, which includes the form and drop-down boxes for the user
# to enter their search parameters, address and parking type, and then click search. Their parameter inputs are then
# passed to the location_description function, where String variables for information and an int variable for the
# retrieved location's index are returned. The strings are sent as output to the UI for the user to view, and then the
# previously described Availability() function is called to load the options to clear the query and update availability.
def Specific_Parking_Information():

    col1, col2, col3= st.columns(3)
    with col1:
        street_number = st.text_input("Street #", key="street_number")
        state = st.text_input("State", key="state")
    with col2:
        street_name = st.text_input("Street Name", key="street_name")
        zip_code  = st.text_input("Zip Code", key="zip_code")
    with col3:
        city = st.text_input("City", key="city")
    type_given = st.selectbox("Would you like to specify the type of parking (street, garage, etc.)?", ["","Yes", "No"])
    if type_given=="Yes":
        type = st.selectbox("Please select the type of parking the location has:",["","Street parking", "Garage", "Lot"])
        if len(type)>1:
            search = st.button("Search", key="search_button")
            if st.session_state.get('button') != True:
                st.session_state['button'] = search
            if st.session_state['button'] == True:
                message = "Please wait..."
                with st.spinner(message):
                    output_str, rel_incidents_str, output2_str, loc_id = location_description(street_number, street_name, zip_code,
                                                                                      city, type)

                    st.header("Parking Information For '"+ street_number+" "+street_name+" "+city+" "+state+" "+zip_code+"'")
                    st.markdown(output_str)
                    st.markdown(rel_incidents_str)
                    st.markdown(output2_str)
                    st.write("")
                    st.write("")
                    Availability(loc_id)
    elif type_given=="No":
        search = st.button("Search", key="search_button")
        if st.session_state.get('button')!=True:
            st.session_state['button'] = search
        if st.session_state['button'] == True:
            message="Please wait..."
            with st.spinner(message):
                output_str, rel_incidents_str, output2_str, loc_id = location_description(street_number, street_name, zip_code,
                                                                                  city, None)
                st.header("Parking Information For '"+ street_number+" "+street_name+" "+city+" "+state+" "+zip_code+"'")
                st.markdown(output_str)
                st.markdown(rel_incidents_str)
                st.markdown(output2_str)
                st.write("")
                st.write("")
                Availability(loc_id)

# This version of the function from above is a more streamlined version which is implemented in the Locate Nearby
# Parking page. It simply takes an index of a location in Firebase, and passes it to the location_description
# function as the only parameter, signaling it to directly query firebase at that index. Then the parking information
# is returned and printed out to the user.
def Specific_Parking_Information2(index):
    output_str, rel_incidents_str, output2_str, loc_id = location_description(loc_id=index)
    st.header("Parking Information")
    st.markdown(output_str)
    st.markdown(rel_incidents_str)
    st.markdown(output2_str)
    st.write("")
    st.write("")

# This function loads the Locate Nearby Parking page of our application. Similar to the previous page, users are
# presented with a form to fill out an address, but in this case it is their location instead. Following this, various
# filters are presented as optional criteria a user can select to further filter a search for parking locations. Once
# completed, the user can then click a search button, and their inputs are passed to the parking_list function in the
# backend. This returns a dataframe with matching parking locations and their coordinates, which are used as parameters
# for the Map() function, which prints out an interactive map for the user. The coordinates are then dropped from the
# dataframe, and it is printed out as an interactive table to the user. Once this occurs, the user can observe locations
# and by looking at its index, can select a location to view more information on in the drop-dwon menu below the table.
# This will load specific parking information with rates and hours for that location. Once users are finished, they are
# prompted to clear their query.
def LocateNearbyParking():
    st.write("Enter your current location below to find the closest n parking spots near you.")
    col1, col2, col3 = st.columns(3)
    with col1:
        user_street_number = st.text_input("Street #", key="user_street_number")
        user_state = st.text_input("State", key="user_state")
    with col2:
        user_street_name = st.text_input("Street Name", key="user_street_name")
        user_zip_code = st.text_input("Zip Code", key="user_zip_code")
    with col3:
        user_city = st.text_input("City", key="user_city")
    st.write("")
    st.write("")
    st.write("")
    st.write("Select additional filtering/sorting criteria below (if desired):")
    type = st.selectbox("Please select the type of parking the location should have:", [None, "Street parking", "Garage", "Lot", "Not street parking"])

    has_valet = st.selectbox("Select your valet preference for parking",[None, "Offers valet", "Does not offer valet"])
    if has_valet=="Offers valet":
        valet_boolean = True
    elif has_valet=="Does not offer valet":
        valet_boolean = False
    else:
        valet_boolean = None
    safety_score = st.number_input("Input a desired minimum safety score (0-100) for locations", max_value=100,
                                   min_value=0, step=1)
    restrictions = st.checkbox("Click to only include the parking locations that have no parking restrictions(like \"Customers Only\")")
    if_available = st.checkbox("Click to only include locations that have confirmed availability (based on"
                               " most recent user inputs)")
    st.write("")
    sort_category = st.selectbox("Select criteria to sort locations by",["","safety","distance","duration"])
    quantity = st.selectbox("Limit search to first (By default first 5 locations are returned):", [5, 10, 15, 20, 25])

    search = st.button("Search", key="search_button")
    if st.session_state.get('button') != True:
        st.session_state['button'] = search
    if st.session_state['button'] == True:

        data, cord = parking_list(user_street_number, user_street_name, user_zip_code, user_city, user_state, type, if_available,
                 valet_boolean, safety_score, restrictions, quantity, sort_category)
        with st.spinner("Search in progress..."):
            Map(data, cord)
            data = data.drop(["lat", "lon"], axis=1)
            st.dataframe(data)
            selected_index = st.multiselect("Select a row's index to view its specific parking information", data["ID"])
            if len(selected_index)==0:
                st.write("")
            else:
                Specific_Parking_Information2(selected_index[0])
                if st.checkbox("Click to clear the query result"):
                    st.checkbox("Are you sure you want to start a new search? (Click checkbox to proceed)")
                    st.session_state["button"] = False

# This Map function passes in the queried locations given the user's location and criteria, as well as the user's
# location translated into longitude and latitude coordinates. The lon and lat coordinates from the queried locations
# are passed as one map layer and plotted in red, while the user's location is another layer plotted in green.
def Map(data, user_cord):
    user_lat = user_cord["lat"]
    user_lon= user_cord["long"]
    user = [[user_lon,user_lat]]
    st.success("Match(es) found!")
    st.subheader("Map of Parking Locations")
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=user_lat,
            longitude=user_lon,
            zoom=12.76,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=data,
                get_position='[lon,lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=30,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data= user,
                get_position='-',
                get_color='[76, 220, 76, 160]',
                get_radius=30,
            ),
        ],
    ))






PAGES = ["Mission Statement","Specific Parking Information & Availability Updates", "Locate Nearby Parking"]
st.sidebar.title("Park It: Safe and Simple")
selection = st.sidebar.radio("Navigation", PAGES)
if selection == PAGES[0]:
    homepage()


# '''
# Specific Parking Information/ Availability Updates
# '''

elif selection == PAGES[1]:
    st.title("Park It: Safe and Simple")
    st.write("Search for parking spots within Los Angeles based on **proximity**, **price**, and **safety metrics**.")
    st.subheader("Specific Parking Information and Availability updates")
    st.write("Enter the address of a parking location to find detailed information.")
    Specific_Parking_Information()

# '''
# Locate Nearby Parking
# '''
elif selection == PAGES[2]:
    st.title("Park It: Safe and Simple")
    st.write("Search for parking spots within Los Angeles based on **proximity**, **price**, and **safety metrics**.")
    st.subheader("Locate Nearby Parking")
    LocateNearbyParking()

