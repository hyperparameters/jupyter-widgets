import os
from matplotlib import pyplot as plt
from ipywidgets import widgets,Layout
import logging
from PIL import Image
import io

class ImageViewer:
    def __init__(self, img_dir):
        self.img_dir = img_dir
        self.img_paths, self._max_iterator = self._get_image_paths(self.img_dir)
        self.sub_directory_options = self._get_sub_directories(self.img_dir)
        self._iterator = 0
        self._create_layout()
        self._logger = logging.getLogger("ImageViewer")
        
    def _get_image_paths(self, directory):
        image_paths=[os.path.join(directory,name) for name in os.listdir(directory) if name.split(".")[-1] in ["jpg","jpeg","png"]]
        return image_paths, len(image_paths)
    
    def _get_sub_directories(self, directory):
        s = [w for w in os.walk(directory)][0][1]
        s.insert(0,"..")
        sub_directories = []
        for i, name in enumerate(s):
            sub_directories.append((name,name))
        #print(sub_directories)
        return sub_directories
    
    def _create_layout(self):
        self.button_layout = Layout(width="40px",height="30px")
        
    def create_widgets(self):
        max_value = max(self._max_iterator-1,0)
        self.slider = widgets.IntSlider(min=0, max=max_value)
        self.play = widgets.Play(
                value=0,
                min=0,
                max=max_value,
                step=1,
                interval=500,
                description="Press play",
                disabled=False
            )

        widgets.jslink((self.play, 'value'), (self.slider, 'value'))
        self.slider.observe(self.handle_slider_change, names="value")
        
        #folder selector
        self.folder_selector = widgets.Dropdown(
            options=self.sub_directory_options,
            value=None,
            description='folder:',layout=Layout(width="45%")
        )
        self.folder_selector.observe(self.handle_folder_selector_change, names="value")
        
        #image viewer
        image_base = self._get_blank_img()
        self.image_viewer = widgets.Image(
                    value=image_base,
                    format='jpg',
                    width=640,
                    height=320,layout=Layout(width="45%",height="640px")
                )

        self.next_button = widgets.Button(description='',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='next',
            icon='step-forward',layout=self.button_layout)
        self.next_button.on_click(self._next)
        
        self.previous_button = widgets.Button(description='',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='previous',
            icon='step-backward',layout=self.button_layout)
        self.previous_button.on_click(self._prev)

        self.seek_bar = widgets.HBox([self.play,self.previous_button,self.next_button,self.slider])
        self.buttons = widgets.HBox([])
        self.vbox = widgets.VBox([self.folder_selector,self.image_viewer,self.seek_bar,self.buttons])
        return self.vbox
    
    def _get_blank_img(self):
        img = Image.new('RGB', (25, 25))
        imgByteArr = io.BytesIO()
        img.save(imgByteArr, format='PNG')
        imgByteArr = imgByteArr.getvalue()
        return imgByteArr
    
    def read_image(self, ind):
        path = self.img_paths[ind]
        file = open(path, "rb")
        image = file.read()
        file.close()
        return image
    
    def display(self):
        w=self.create_widgets()
        return w
      
    def _next(self, e):
        self._iterator+=1
        if self._iterator==self._max_iterator:
            self._iterator = self._max_iterator-1
            
        self.slider.value = self.slider.value=self._iterator
        
    def _prev(self, e):
        self._iterator-=1
        if self._iterator<0:
            self._iterator = 0
            
        self.slider.value = self.slider.value=self._iterator
        
        
    def handle_slider_change(self, change):
        ind = change.new
        print(f"slider change {ind}, max {self._max_iterator}")
        if self._max_iterator>0:       
            if ind >= self._max_iterator:
                ind = 0
    #             self.play.send_state()
            print(f" handle slider change {ind}")
            image = self.read_image(ind)
            self.image_viewer.value = image
        
    def handle_folder_selector_change(self, change):
        folder = change.new
        print(f"folder change {folder}")
        if folder:
            if folder != "..":

                new_directory = os.path.join(self.img_dir,folder)
            else:
                new_directory = os.path.dirname(self.img_dir)

            self.img_paths, self._max_iterator = self._get_image_paths(new_directory)
            self.img_dir = new_directory
            max_value = max(self._max_iterator-1,0)
            self.slider.max = max_value
            self.play.max = max_value
            self.slider.value=1
            self.slider.value=0
            self.folder_selector.unobserve(self.handle_folder_selector_change, names="value")
            self.folder_selector.options = self._get_sub_directories(new_directory)
            self.folder_selector.observe(self.handle_folder_selector_change, names="value")
            self.folder_selector.value= None
        
    def plot_img(self, path):
        plt.figure(figsize=(10,10))
        plt.axis("off")
        im = plt.imread(path)
        plt.imshow(im)
    
        
