
import tensorflow as tf
import tensorflowjs as tfjs


model = tf.keras.models.load_model('model.keras')
tfjs.converters.save_keras_model(model, 'jsmodel')
