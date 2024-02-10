# Necessary imports
import customtkinter
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import os


# Import algorithms
from algorithms.affinity_propogation import call_affinity
from algorithms.db_scan import call_dbscan
from algorithms.k_means import call_kmeans

from misc.random_generator import random_data
from output_generator.video_generator import call_video_generator


# Import file_readers
from file_readers.csv_to_ndarray import read_csv
from file_readers.xlsx_to_ndarray import read_xlsx
from file_readers.xls_to_ndarray import read_xls


# Default theme
theme = "dark"

# Global variables
FOLDER_PATH = "./Outputs/"


##############################################################################################################
############################ MAIN GUI ########################################################################

def display_ui():
    global filename
    ############################ HELPER FUNCTIONS ################################################################

    def browseFiles():
        global filename
        filename = filedialog.askopenfilename(
            # initialdir=os.path.expanduser("~"),  # Start at user home directory
            initialdir=os.getcwd(),  # Start at current directory
            title="Select a File",
            filetypes=(
                ("CSV files", "*.csv"),
                ("Text files", "*.txt"),
                ("Excel (Current) files", "*.xlsx"),
                ("Excel (Legacy) files", "*.xls")
                
            ))
        print(filename)
        print(algo_clicked.get())
        browse_button.configure(text=filename.split("/")[-1])
        ret_arr.append(filename)
        print(ret_arr)
        return filename

    def submit():
        global filename
        global input_data
        plot_dimension_choice = int(dimensions.get()[:1])
        error_label.place_forget()
        if file_radio_choice.get() == "select_file":
            if (str(filename) == ""):
                # add a label to show that file is not uploaded, print in red
                error_label.configure(text="Error: File not uploaded. Try again.")
                error_label.place(relx=0.30, rely=0.85)
                return
            else:
                error_label.place_forget()
                

            # Extract file extension
            temp_arr = filename.split(".")
            extension = temp_arr[1]

            # call appropriate file reader

            if extension == "csv":
                input_data = read_csv(filename, has_header,
                                    True, plot_dimension_choice)
            elif extension == "xlsx":
                input_data = read_xlsx(filename, None,  has_header,
                                    True, plot_dimension_choice)
                print(input_data)
            elif extension == "xls":
                input_data = read_xls(filename, has_header,
                                     plot_dimension_choice)
                print(input_data)
            
        else:
            input_data = random_data_generated

        # call the appropriate algorithms
        
        executing_label.place(relx=0.30, rely=0.85)
        if algo_clicked.get() == "affinity clustering":
            call_affinity(input_data, float(entry1.get()), int(entry2.get()))
        elif algo_clicked.get() == "dbscan":
            call_dbscan(input_data, float(entry1.get()), int(entry2.get()))
        elif algo_clicked.get() == "kmeans":
            call_kmeans(input_data, int(entry1.get()), int(entry2.get()))
        algorithm = algo_clicked.get()
        executing_label.place_forget()
        
        if video_required.get() == 1:
            call_video_generator(algorithm, "output.avi")
        if slideshow_required.get() == 0 and video_required.get() == 0:
            error_label.configure(text="Error: No output selected. Try again.")
            error_label.place(relx=0.30, rely=0.85)
        if slideshow_required.get() == 1: # Handle this case at last because infinite loop
            root.destroy()
            slideshow(algorithm)
            



    def change_theme():
        global num  # add this line
        if num == 0:
            customtkinter.set_appearance_mode("light")
            theme_button.configure(image=sun_icon)
            theme_button.image = sun_icon
            num = 1
        else:
            customtkinter.set_appearance_mode("dark")
            theme_button.configure(image=moon_icon)
            theme_button.image = moon_icon
            num = 0

    def generate_random_dataset():
        global random_data_generated
        num_points = int(num_points_input.get())
        num_clusters = int(num_clusters_input.get())
        plot_dimension_choice = int(dimensions.get()[:1])
        random_data_generated = random_data(num_points, num_clusters, plot_dimension_choice)
        submit()

    def video(algorithm):
        pass

    def select_file_handler():
        num_points_label.place_forget()
        num_points_input.place_forget()
        num_clusters_input.place_forget()
        num_clusters_label.place_forget()  
        generate_button.place_forget() 
        browse_button.place(relx=0.35, rely=0.4)
        labelNum3.place(relx=0.33, rely=0.45)
        submit_button.place(relx=0.35, rely=0.8) 

    def create_random_handler():
        num_points_label.place(relx=0.05, rely=0.4)
        num_points_input.place(relx=0.35, rely=0.4)
        num_clusters_input.place(relx=0.35, rely=0.45)
        num_clusters_label.place(relx=0.05, rely=0.45)
        generate_button.place(relx=0.35, rely=0.8)
        browse_button.place_forget()
        labelNum3.place_forget()
        submit_button.place_forget()
        
        
    def file_or_random_creator():
        if file_radio_choice.get() == "select_file":
            select_file_handler()
        else:
            create_random_handler()
            
    def update_parameters(something):
        if algo_clicked.get() == "affinity clustering":
            Parameter1.configure(text="Damping")
            Parameter2.configure(text="Max Iterations")
            entry1.configure(placeholder_text="> 0 , < 1")
            entry2.configure(placeholder_text="> 0 , < 1000")
        elif algo_clicked.get() == "dbscan":
            Parameter1.configure(text="Epsilon")
            Parameter2.configure(text="Min Points")
            entry1.configure(placeholder_text="Example: 3")
            entry2.configure(placeholder_text="> 0 , < 1000")
        elif algo_clicked.get() == "kmeans":
            Parameter1.configure(text="Number of Clusters")
            Parameter2.configure(text="Max Iterations")
            entry1.configure(placeholder_text=">0 , < num_points")
            entry2.configure(placeholder_text="> 0 , < 1000")
        load_info()
          
    def load_info():
        global info_file
        # read the corresponding file and display the information
        if algo_clicked.get() == "affinity clustering":
            info_file = open("assets/info/AffinityPropogation.txt", "r")
        elif algo_clicked.get() == "dbscan":
            info_file = open("assets/info/DBscan.txt", "r")
        elif algo_clicked.get() == "kmeans":
            info_file = open("assets/info/Kmeans.txt", "r")
        
        # add the information to the text box
        info_text.delete("0.0", "end")
        info_text.insert("0.0", info_file.read())
        info_file.close()    
    
    def close_handler():
        root.destroy()
        exit(0)    
    ############################ BUILDING UI ###################################################################
       
    customtkinter.set_appearance_mode("dark")
    global has_header, plot_dimension_choice, num_clusters_entry, num_points_entry, file_radio_choice, ret_arr, num
    num = 0 # means currently dark mode is on
    ret_arr = []

    global root
    root = customtkinter.CTk()
    root.geometry('500x300+100+200')
    
    # use full screen
    root.attributes('-fullscreen', True)
    customtkinter.set_appearance_mode("dark")
    root.title('PLL')

    # algorithm type dropdown

    labelNum1 = customtkinter.CTkLabel(root, text="Choose algorithm")
    labelNum1.place(relx=0.05, rely=0.1)

    algo_clicked = customtkinter.StringVar(value="affinity clustering")

    drop2 = customtkinter.CTkOptionMenu(master=root,
                                        values=["affinity clustering",
                                                "dbscan", "kmeans"],
                                        variable=algo_clicked, command=update_parameters)
    drop2.place(relx=0.35, rely=0.1)

    DimensionLabel = customtkinter.CTkLabel(root, text="Choose plot dimension")
    DimensionLabel.place(relx=0.05, rely=0.15)

    dimensions = customtkinter.StringVar(value="3-D")

    drop3 = customtkinter.CTkOptionMenu(master=root,
                                        values=["2-D", "3-D"],
                                        variable=dimensions)
    drop3.place(relx=0.35, rely=0.15)

    HeaderLabel = customtkinter.CTkLabel(root, text="Data Headers:")
    HeaderLabel.place(relx=0.05, rely=0.2)

    header = customtkinter.StringVar(value="No")

    drop4 = customtkinter.CTkOptionMenu(master=root,
                                        values=["No", "Yes"],
                                        variable=header)
    drop4.place(relx=0.35, rely=0.2)

    if (header.get() == "True"):
        has_header = True
    else:
        has_header = False
    # convert string to int

    plot_dimension_choice = int(dimensions.get()[:1])
    
    
    # browse files button
    labelNum2 = customtkinter.CTkLabel(root, text="Input Data File:")
    labelNum2.place(relx=0.05, rely=0.3)

    file_radio_choice = customtkinter.StringVar(value="select_file")

    file_radio_select = customtkinter.CTkRadioButton(root, text="Select a File", variable=file_radio_choice, value="select_file", command=file_or_random_creator)
    file_radio_select.place(relx=0.20, rely=0.3)

    file_radio_create = customtkinter.CTkRadioButton(root, text="Create Random Dataset", variable=file_radio_choice, value="create_random", command=file_or_random_creator)
    file_radio_create.place(relx=0.35, rely=0.3)

    browse_button = customtkinter.CTkButton(
        root, text="Browse Files", command=browseFiles)

    labelNum3 = customtkinter.CTkLabel(
        root, text="Only .csv, .xlsx, .xls files allowed")
    

    num_points_label = customtkinter.CTkLabel(root, text="Number of points:")
    num_points_input = customtkinter.CTkEntry(root)
    num_clusters_label = customtkinter.CTkLabel(root, text="Number of clusters:")
    num_clusters_input = customtkinter.CTkEntry(root)



    customtkinter.CTkLabel(root, text="Output Format:").place(relx=0.05, rely=0.5)
    
    slideshow_required = customtkinter.IntVar(value=1)
    slideshow_switch = customtkinter.CTkSwitch(root, text="Slideshow", 
                                 variable=slideshow_required, onvalue=1, offvalue=0)
    slideshow_switch.place(relx=0.35, rely=0.5)
    
    video_required = customtkinter.IntVar(value=0)
    video_switch = customtkinter.CTkSwitch(root, text="Video", variable=video_required, onvalue=1, offvalue=0)
    video_switch.place(relx=0.35, rely=0.55)

    generate_button = customtkinter.CTkButton(
        root, text="Generate", command=generate_random_dataset)

    submit_button = customtkinter.CTkButton(
        root, text="Submit", command=submit)
    
    error_label = customtkinter.CTkLabel( root, text="ERROR: File not uploaded. Try again", text_color="red" )
    error_label.place_forget()
    
    executing_label = customtkinter.CTkLabel( root, text="Running the clustering algorithm. Please wait.", text_color="green" )
    executing_label.place_forget()

    file_or_random_creator()
    
    # add a label parameters
    parameters_label = customtkinter.CTkLabel(root, text="Parameters:")
    parameters_label.place(relx=0.05, rely=0.6)
    
    Parameter1 = customtkinter.CTkLabel(root, text="Damping Factor:")
    Parameter1.place(relx=0.05, rely=0.65)

    Parameter2 = customtkinter.CTkLabel(root, text="Max Iterations:")
    Parameter2.place(relx=0.05, rely=0.7)

    entry1 = customtkinter.CTkEntry(master=root,
                                    placeholder_text="> 0 , < 1",
                                    width=120,
                                    height=25,
                                    border_width=2,
                                    corner_radius=10)
    
    entry1.place(relx=0.35, rely=0.65)
    entry2 = customtkinter.CTkEntry(master=root,
                                    placeholder_text="> 0 , < 1000",
                                    width=120,
                                    height=25,
                                    border_width=2,
                                    corner_radius=10)
    entry2.place(relx=0.35, rely=0.7)

    # Adding the information frame
    info_frame = customtkinter.CTkFrame(root)
    info_frame.place(relx=0.55, rely=0.1, relwidth=0.4, relheight=0.8)
    info_label = customtkinter.CTkLabel(info_frame, text="Information About Algorithm")
    info_label.place(relx=0.00, rely=0.00)
    info_text = customtkinter.CTkTextbox(info_frame)
    info_text.place(relx=0.05, rely=0.05, relwidth=0.90, relheight=0.90)
    
    load_info()
    
    
    # Adding the theme button    
    sun_icon = PhotoImage(file="assets/img/sun.png")
    moon_icon = PhotoImage(file="assets/img/moon.png")
    # moon_icon = ImageOps.invert(moon_icon_black)
    
    # resize the image
    sun_icon = sun_icon.subsample(50, 50)
    moon_icon = moon_icon.subsample(50, 50)
        
    theme_button = customtkinter.CTkButton(root, image=moon_icon, command=change_theme, bg_color="transparent", border_width=0, text="" , fg_color="white" )
    theme_button.image = moon_icon
    theme_button.place(relx=0.9, rely=0.05, relwidth=0.05, relheight=0.05)

    
    
    #Adding the close button
    close_button = customtkinter.CTkButton(root, text="Close", command=close_handler)
    close_button.place(relx=0.9, rely=0.9, relwidth=0.05, relheight=0.05)
    
    root.mainloop()


##############################################################################################################
############################ OUTPUT VIEWER UI ################################################################


def slideshow(algorithm):
    ############################ HELPER FUNCTIONS ##############################################################

    def forward(img_no, max_image):
        submit_button.configure(text="Reset")
        global label
        global button_forward
        global button_back
        label = Label(image=List_images[img_no-1])

        label.grid(row=1, column=0, columnspan=3)

        if (img_no != 1):
            button_back = customtkinter.CTkButton(
                slideshow_root, text="Back", command=lambda: back(img_no-1, max_image))
            button_back.grid(row=5, column=0)

        if (img_no != max_image):
            button_for = customtkinter.CTkButton(
                slideshow_root, text="Next", command=lambda: forward(img_no+1, max_image))
            button_for.grid(row=5, column=2)

        # update slider value
            slider.set(img_no)

    def back(img_no, max_image):

        global label
        global button_forward
        global button_back
        label = Label(image=List_images[img_no - 1])
        label.grid(row=1, column=0, columnspan=3)
        if (img_no != 1):
            button_back = customtkinter.CTkButton(
                slideshow_root, text="Back", command=lambda: back(img_no-1, max_image))
            button_back.grid(row=5, column=0)

        if (img_no != max_image):
            button_for = customtkinter.CTkButton(
                slideshow_root, text="Next", command=lambda: forward(img_no+1, max_image))
            button_for.grid(row=5, column=2)

        # update slider value
        slider.set(img_no)

    def close_button_handler():
        slideshow_root.destroy()
        display_ui()

    ############################ BUILDING UI ###################################################################

    slideshow_root = customtkinter.CTk()
    slideshow_root.title("Image Viewer")
    slideshow_root.attributes('-fullscreen', True)

    if algorithm == "affinity clustering":
        folder_path = FOLDER_PATH + "AffinityPropogations/"
    if algorithm == "dbscan":
        folder_path = FOLDER_PATH + "DBScan/"
    if algorithm == "kmeans":
        folder_path = FOLDER_PATH + "Kmeans/"
    List_images = []
    total_image = len(os.listdir(folder_path))
    for i in range(0, len(os.listdir(folder_path))):
        img_path = folder_path + "output" + str(i) + ".png"
        # check if file exists
        if os.path.isfile(img_path):
            img = Image.open(img_path)
            List_images.append(ImageTk.PhotoImage(img))
            img.close()
        else:
            print(f"File {img_path} does not exist.")


    # print(List_images)

    submit_button = customtkinter.CTkButton(
        slideshow_root, text="Start", command=lambda: forward(1, total_image))
    submit_button.place(relx=0.35, rely=0.75)

    # add slider
    slider = Scale(slideshow_root, from_=1, to=total_image, orient=HORIZONTAL,
                    command=lambda value: forward(int(value), total_image))
    slider.place(relx=0.3, rely=0.85, relwidth=0.4)

    close_button = customtkinter.CTkButton(slideshow_root, text="Close", command=close_button_handler)
    close_button.place(relx=0.9, rely=0.9, relwidth=0.05, relheight=0.05)

    slideshow_root.mainloop()


    ##############################################################################################################
    ############################ MAIN FUNCTION ###################################################################


filename = ""
display_ui()