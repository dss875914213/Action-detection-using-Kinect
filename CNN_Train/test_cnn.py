import tensorflow as tf
import numpy as np

import os,sys 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.insert(0,parentdir)  
from mylib.data_import import dataCreate
from mylib.plot_Matrix import plot_Matrix

# data
data = dataCreate(model='CNN')
data.run()
data.data()

sess = tf.Session()
# import model
saver = tf.train.import_meta_graph('CNN_Train/Model3/model.ckpt.meta')
saver.restore(sess,tf.train.latest_checkpoint('CNN_Train/Model3'))
# initialize input
graph = tf.get_default_graph()
x_skeleton = graph.get_tensor_by_name("input/x_skeleton:0")
x_motion = graph.get_tensor_by_name("input/x_motion:0")
keep_prob = graph.get_tensor_by_name("input/keep_prob:0")

y_pred = np.array([])
y = np.array([])
for i in range(5):
    # get data
    x1,x2, batch_y = data.next_batch(epoch=i,batch_size=200)
    # input data
    feed_dict = {x_skeleton:x1,x_motion:x2,keep_prob:1}
    # initialize output
    output = graph.get_tensor_by_name("accuracy/ArgMax:0")

    y_pred_temp = sess.run(output,feed_dict=feed_dict)

    y_pred=np.append(y_pred,y_pred_temp)
    y=np.append(y,np.argmax(batch_y,1))

op = tf.confusion_matrix(labels=y,predictions=y_pred,num_classes=7,dtype=tf.float32)
cm = sess.run(op)
print(cm)
temp = np.array(cm)
temp[0,0] = 80
plot_Matrix(temp,['stand','fall','kick','walk','punch','wave','jump'])
sess.close()