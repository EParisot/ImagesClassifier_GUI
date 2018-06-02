# -*- coding: utf-8 -*-

import keras

class CustomModelCheckPoint(keras.callbacks.Callback):
    def __init__(self, graph=None, canvas=None, **kargs):
        super(CustomModelCheckPoint,self).__init__(**kargs)
        self.graph = graph
        self.canvas = canvas
        def on_epoch_begin(self,epoch, logs={}):
            # Things done on beginning of epoch. 
            return

        def on_epoch_end(self, epoch, logs={}):
            # things done on end of the epoch
            self.graph.plot(epoch, logs.get("acc"), "g.")
            self.graph.plot(epoch, logs.get("loss"), "r.")
            self.canvas.draw()
            print("test : " + str(epoch))
            
            

