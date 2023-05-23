import streamlit as st
import streamlit.components.v1 as stc
import os
import glob
import shutil
from datetime import datetime
import subprocess

class FileService:
    def create_directory(self, path, directory_name):
        # Create the subdirectory inside the given path
        sub_dir = os.path.join(path, directory_name)
        os.makedirs(sub_dir, exist_ok=True)

        # Return the path of the created subdirectory
        return sub_dir

    def organize_recorded_files(self, path):
        # Define the source directory where the recorded files are located
        source_dir_path = "/home/jarvis/Videos"  # Replace with the actual directory path where the recorded files are stored
        source_dir = self.create_directory(source_dir_path, "VLC_recordings")
        print("path passed is "+path)
        # Create the destination directory path based on patient ID and date
        # destination_dir = "/home/jarvis/projects/Hospital_app/Recordings/"+patient_id+"/"+date
        destination_dir = path

        # Get a list of recorded files in the source directory
        recorded_files = glob.glob(os.path.join(source_dir, "*.mp4"))

        # Sort the recorded files based on their creation time
        recorded_files.sort(key=os.path.getctime)

        # Get the highest file number already present in the destination directory
        existing_files = glob.glob(os.path.join(destination_dir, "*.mp4"))
        highest_number = len(existing_files)

        # Move and rename the recorded files to the destination directory
        for i, file_path in enumerate(recorded_files):
            new_file_name = str(highest_number + i + 1) + ".mp4"  # Rename the file with the next available number
            new_file_path = os.path.join(destination_dir, new_file_name)
            shutil.move(file_path, new_file_path)

# # Example usage:
# file_service = FileService()

# # # Get user input for patient_id and date
# patient_id = input("Enter patient ID: ")
# date = datetime.now().strftime("%Y-%m-%d")
# # # date = #input("Enter date (format: YYYY-MM-DD): ")

# # Call the function to create the directory structure
# base_path = "/home/jarvis/projects/Hospital_app/Recordings"
# pIDdirectory_path = file_service.create_directory(base_path, patient_id)
# dateDirectory_path = file_service.create_directory(pIDdirectory_path, date)


# # Print the path of the created subdirectory
# print("Directory created:", pIDdirectory_path)

# file_service.organize_recorded_files(dateDirectory_path)
# #  organize_recorded_files(patient_id, date)

def main():
    st.title("MediRecorda")
    file_service = FileService()
    base_path = "/home/jarvis/projects/Hospital_app/Recordings"
    menu = ["Recording Session", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Recording Session":
        st.subheader("Recording Session")
        departments = ["Cardiology", "Neurology", "General surgery", "Radiology", "Orthopedics", "Urology", "Surgery", "Outpatient department", "Internal medicine", ]
        dep_dir = st.selectbox("Select Department", departments)
        patient_id = st.text_input("Enter the Patient's ID")
        video_categories = ["Surgery Videos", "Patient Education Videos", "Patient Testimonial Videos", "Medical Training Videos","Medical Device Demonstration Videos"]
        vid_category = st.selectbox("Select Video Category", video_categories)
        # vid_category = st.text_input("Enter the Video Category")
        date = datetime.now().strftime("%Y-%m-%d")
        global dateDirectory_path  # Use the global variable
        if st.button("Start Session"):
            #  global dateDirectory_path  # Use the global variable
             if patient_id is not None:
                    # st.text("VLC Opens and Recording Starts")
                    try:
                        subprocess.Popen(["vlc"])  # Open VLC media player
                        st.success("VLC Media Player opened successfully!")
                    except Exception as e:
                        st.error("Error occurred while opening VLC Media Player: " + str(e))
        if st.button("End Session"): 
                 dep_path = file_service.create_directory(base_path, dep_dir)
                 pIDdirectory_path = file_service.create_directory(dep_path, patient_id)
                 dateDirectory_path = file_service.create_directory(pIDdirectory_path, date)
                 category_path = file_service.create_directory(dateDirectory_path,vid_category)
                 st.text("Directoy path "+category_path)
                 st.text("All recorded files of the session is oraganized and put into the above directory")
                 file_service.organize_recorded_files(category_path)

        



    # elif choice == "End Session":
    #     st.subheader("End")
        

    else:
        st.subheader("About")
        st.text("Built with Streamlit")


if __name__ == '__main__':
    main()