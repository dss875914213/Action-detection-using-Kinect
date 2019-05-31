import tensorflow as tf
import numpy as np
from CNN_Train.preprocess import preprocessing as pre

class cnn():
    def __init__(self):
        self.sess = tf.Session()
        # import model
        saver = tf.train.import_meta_graph('CNN_Train/Model2/model.ckpt.meta')
        saver.restore(self.sess,tf.train.latest_checkpoint('CNN_Train/Model2'))
        
        graph = tf.get_default_graph()     
        # initialize input
        self.x_skeleton = graph.get_tensor_by_name("input/x_skeleton:0")
        self.x_motion = graph.get_tensor_by_name("input/x_motion:0")
        self.keep_prob = graph.get_tensor_by_name("input/keep_prob:0")
        # initialize output
        self.output = graph.get_tensor_by_name("accuracy/ArgMax:0")

        self.label_dict = {0:'falling',1:'waving',2:'kicking',3:'throw'}

        self.Data = np.array([])

    def data_input(self,data):

        self.Data = np.append(self.Data,data)

        label = ''

        if self.Data.shape == 30 * 75:
            skeleton,motion = pre(pos=self.Data).run()
            self.Data = np.array([])

            y_pred = self.sess.run(self.output,feed_dict={self.x_skeleton:skeleton,\
                self.x_motion:motion,self.keep_prob:1})

            label = self.label_dict[y_pred]

        return label
        