import os
from matplotlib import pyplot as plt
from ipywidgets import widgets,Layout

class ImageViewer:
    def __init__(self, img_dir):
        self.img_dir = img_dir
        self.img_paths = [os.path.join(self.img_dir,name) for name in os.listdir(self.img_dir)]
        self._iterator = 0
        self._max_iterator = len(self.img_paths)
        self._create_layout()
    
    def _create_layout(self):
        self.button_layout = Layout(width="40px",height="30px")
        
    def create_widgets(self):
        self.slider = widgets.IntSlider(min=0, max=self._max_iterator-1)
        self.play = widgets.Play(
                value=0,
                min=0,
                max=self._max_iterator-1,
                step=1,
                interval=500,
                description="Press play",
                disabled=False
            )

        widgets.jslink((self.play, 'value'), (self.slider, 'value'))
        self.slider.observe(self.handle_slider_change, names="value")
        
        image_base = self.read_image(0)
        self.image_viewer = widgets.Image(
                    value=image_base,
                    format='jpg',
                    width=640,
                    height=320,
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
        self.vbox = widgets.VBox([self.image_viewer,self.seek_bar,self.buttons])
        return self.vbox
    
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
        
        if ind >= self._max_iterator:
            ind = 0
            self.play.send_state()
        image = self.read_image(ind)
        self.image_viewer.value = image
        
    def plot_img(self, path):
        plt.figure(figsize=(10,10))
        plt.axis("off")
        im = plt.imread(path)
        plt.imshow(im)
    
        
